from __future__ import annotations

import argparse
import copy
import json
import os
import random
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch

from arc_e004.actions import CandidateAction, available_action_ids, execute
from arc_e004.common import latest_grid, seed_everything
from arc_e004.envs import make_env
from arc_e005.tournament import load_fold_model, state_model_outputs

from .action_bank import ActionKey
from .agent import DQNAgent
from .exploration import D14Explorer, load_selector

ROOT = Path(__file__).resolve().parents[2]


def load_cfg() -> dict:
    cfg = json.loads((ROOT / "configs/e012.json").read_text())
    for key, env in [
        ("e004_root", "E004_ROOT"),
        ("e005d_root", "E005D_ROOT"),
        ("e008_root", "E008_ROOT"),
        ("e009_root", "E009_ROOT"),
        ("e011_root", "E011_ROOT"),
    ]:
        cfg[key] = os.environ.get(env, cfg[key])
    return cfg


def safe_dump(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True))
    tmp.replace(path)


def completion_cap(levels_completed: int, n_levels: int = 5) -> float:
    k = max(0, min(int(levels_completed), int(n_levels)))
    return float(k * (k + 1) / (n_levels * (n_levels + 1)))


def materialize_system(spec: dict, cfg: dict) -> dict:
    b = cfg["backbone_defaults"]
    out = {
        "learn": bool(b["learn"]),
        "n_step": int(b["n_step"]),
        "per": bool(b["per"]),
        "distributional": bool(b["distributional"]),
    }
    out.update(copy.deepcopy(spec))
    return out


def systems(cfg: dict) -> list[dict]:
    return [materialize_system(s, cfg) for s in cfg["systems"]]


def tasks(cfg: dict):
    ev = cfg["evaluation"]
    return [(s, int(f), int(seed)) for s in systems(cfg) for f in ev["folds"] for seed in ev["seeds"]]


def action_key_to_candidate(a: ActionKey, click_action_id: int) -> CandidateAction:
    if int(a.action_id) == int(click_action_id):
        return CandidateAction(int(a.action_id), int(a.x), int(a.y))
    return CandidateAction(int(a.action_id))


def representation_outputs(model, grid, prev, available, level: int, high_water: int, cfg: dict, device: torch.device):
    with torch.no_grad():
        emb, simple, simple_logits, a6_logits = state_model_outputs(model, grid, prev, available, device)
    e = np.asarray(emb, dtype=np.float32).reshape(-1)
    if cfg["representation"].get("progress_context", True):
        denom = max(1, int(cfg["representation"].get("max_levels", 5)))
        e = np.concatenate([e, np.asarray([level / denom, high_water / denom], dtype=np.float32)])
    return e, emb, simple, simple_logits, a6_logits


def run_game(game: str, game_idx: int, fold: int, seed: int, system: dict, budget: int, prior_template, selector: dict, device, cfg: dict) -> dict:
    run_seed = int(seed) * 100003 + game_idx * 9173
    seed_everything(run_seed)

    _, env, obs = make_env(game, int(seed))
    grid = latest_grid(obs)
    prev = grid.copy()
    model = copy.deepcopy(prior_template).to(device).eval()
    for p in model.parameters():
        p.requires_grad_(False)

    available = available_action_ids(obs, env)
    level = int(getattr(obs, "levels_completed", 0))
    high_water = level
    s0, _, _, _, _ = representation_outputs(model, grid, prev, available, level, high_water, cfg, device)
    agent = DQNAgent(len(s0), system, cfg, run_seed + 17, device)
    explorer = D14Explorer(selector, cfg["click_action_id"], cfg["click_size"])

    used = action_steps = resets = deaths = progress_events = won = 0
    first_progress = None
    reward_total = 0.0
    rewarded_transitions = 0
    noops = changed_n = action6_n = repeats = 0
    since_progress = 0
    seen_states: set[bytes] = set()
    state_action_counts = Counter()
    decision_labels = Counter()
    label_action6 = Counter()
    run_start = time.perf_counter()

    while used < budget:
        available = available_action_ids(obs, env)
        if not available:
            break
        level_before = int(getattr(obs, "levels_completed", high_water))
        state, emb, simple, simple_logits, a6_logits = representation_outputs(
            model, grid, prev, available, level_before, high_water, cfg, device
        )

        explore_fn = None
        if system.get("exploration_policy") != "uniform":
            def explore_fn(rng, action_index, _grid=grid, _emb=emb, _simple=simple, _sl=simple_logits, _a6=a6_logits, _available=list(available), _since=since_progress):
                return explorer.choose(
                    system=system,
                    rng=rng,
                    action_index=action_index,
                    since_progress=_since,
                    available=_available,
                    grid=_grid,
                    emb=_emb,
                    simple=_simple,
                    prior_simple_logits=_sl,
                    prior_a6_logits=_a6,
                )

        a, decision_label = agent.act(state, list(available), explore_fn=explore_fn)
        cand = action_key_to_candidate(a, cfg["click_action_id"])
        if int(cand.action_id) not in {int(x) for x in available}:
            raise AssertionError(("illegal_action", cand, available, decision_label))

        decision_labels[decision_label] += 1
        label_action6[decision_label] += int(a.action_id == cfg["click_action_id"])
        explorer.observe(grid, a)

        raw = grid.tobytes()
        key = (hash(raw), int(a.action_id), int(a.x), int(a.y))
        repeats += int(state_action_counts[key] > 0)
        state_action_counts[key] += 1
        seen_states.add(raw)
        action6_n += int(a.action_id == cfg["click_action_id"])

        before = grid.copy()
        used += 1
        action_steps += 1
        nxt = execute(env, cand)
        if nxt is None:
            break
        after = latest_grid(nxt, before)
        level_after = int(getattr(nxt, "levels_completed", level_before))
        state_name = getattr(getattr(nxt, "state", None), "name", str(getattr(nxt, "state", "")))
        changed = bool(np.any(after != before))
        noops += int(not changed)
        changed_n += int(changed)
        danger = bool(state_name == "GAME_OVER")
        win = bool(state_name == "WIN")
        terminal = bool(danger or win)

        old_high = high_water
        new_high = max(high_water, level_after)
        progress_delta = max(0, new_high - old_high)
        reward = float(cfg["reward"]["progress_scale"]) * progress_delta
        if win and progress_delta == 0:
            reward += float(cfg["reward"].get("win_bonus_if_no_progress", 0.0))
        if danger:
            reward += float(cfg["reward"].get("death_penalty", 0.0))
        high_water = new_high
        progress = bool(progress_delta > 0 or win)
        if progress:
            progress_events += 1
            since_progress = 0
            if first_progress is None:
                first_progress = used
        else:
            since_progress += 1
        if reward != 0.0:
            rewarded_transitions += 1
        reward_total += reward

        next_available = tuple(available_action_ids(nxt, env)) if not terminal else tuple()
        if not terminal and next_available:
            next_state, _, _, _, _ = representation_outputs(
                model, after, before, list(next_available), level_after, high_water, cfg, device
            )
        else:
            next_state = state.copy()
        agent.observe(state, tuple(int(x) for x in available), a, reward, next_state, next_available, terminal)

        if win:
            won = 1
            prev, grid, obs = before, after, nxt
            break

        if danger:
            deaths += 1
            # Death/reset is not progress. Preserve the stagnation counter so
            # the stagnation-gated explorer can activate across repeated deaths.
            if used >= budget:
                break
            reset_obs = env.reset()
            used += 1
            resets += 1
            if reset_obs is None:
                break
            prev = latest_grid(reset_obs, after).copy()
            grid = prev.copy()
            obs = reset_obs
            continue

        prev, grid, obs = before, after, nxt

    agent.finish()
    elapsed = time.perf_counter() - run_start
    denom = max(1, action_steps)
    summary = agent.summary()
    eps_n = max(1, decision_labels["uniform"] + decision_labels["type_prior"] + decision_labels["d14"])
    return {
        "game": game,
        "game_idx": game_idx,
        "fold": fold,
        "seed": seed,
        "system_id": system["id"],
        "family": system.get("family", "structured"),
        "exploration_policy": system.get("exploration_policy", "uniform"),
        "budget": budget,
        "commands_used": used,
        "action_steps": action_steps,
        "resets": resets,
        "progress_events": progress_events,
        "levels_completed": high_water,
        "completion_cap": completion_cap(high_water, int(cfg["representation"].get("max_levels", 5))),
        "first_progress": first_progress,
        "progress_by_50": int(first_progress is not None and first_progress <= 50),
        "progress_by_100": int(first_progress is not None and first_progress <= 100),
        "progress_by_250": int(first_progress is not None and first_progress <= 250),
        "progress_by_600": int(first_progress is not None and first_progress <= 600),
        "won": won,
        "reward_total": reward_total,
        "rewarded_transitions": rewarded_transitions,
        "deaths": deaths,
        "death_per_100": 100.0 * deaths / denom,
        "noop_rate": noops / denom,
        "changed_rate": changed_n / denom,
        "repeat_action_state_rate": repeats / denom,
        "action6_rate": action6_n / denom,
        "unique_raw_states": len(seen_states),
        "d14_calls": int(decision_labels["d14"]),
        "typeprior_calls": int(decision_labels["type_prior"]),
        "uniform_calls": int(decision_labels["uniform"]),
        "d14_fraction_of_epsilon": decision_labels["d14"] / eps_n,
        "d14_action6_rate": label_action6["d14"] / max(1, decision_labels["d14"]),
        "typeprior_action6_rate": label_action6["type_prior"] / max(1, decision_labels["type_prior"]),
        "elapsed_seconds": elapsed,
        "actions_per_second": action_steps / max(elapsed, 1e-9),
        **summary,
    }


def run_task(system: dict, fold: int, seed: int, cfg: dict, device: torch.device, selector: dict) -> dict:
    prior, spec, checkpoint = load_fold_model(fold, device, seed)
    games = cfg["folds"][fold]
    budget = int(cfg["evaluation"]["budget"])
    rows = []
    for game in games:
        gi = cfg["all_public_games"].index(game)
        rows.append(run_game(game, gi, fold, seed, system, budget, prior, selector, device, cfg))
    out = {
        "experiment_id": cfg["experiment_id"],
        "stage": "final_ablation",
        "system": system,
        "fold": fold,
        "seed": seed,
        "representation_id": cfg["representation"]["id"],
        "e004_spec_id": spec["id"],
        "e004_checkpoint": str(checkpoint),
        "e005_selector_id": selector["id"],
        "device": str(device),
        "rows": rows,
    }
    outdir = ROOT / "results" / "runs"
    safe_dump(out, outdir / f"{system['id']}__f{fold}__s{seed}.json")
    return out


def task_path(system: dict, fold: int, seed: int) -> Path:
    return ROOT / "results" / "runs" / f"{system['id']}__f{fold}__s{seed}.json"


def resolve_device(name: str) -> torch.device:
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device(name)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    return device


def run_task_index(task_index: int, device_name: str = "cpu") -> dict:
    cfg = load_cfg()
    all_tasks = tasks(cfg)
    if not (0 <= int(task_index) < len(all_tasks)):
        raise ValueError((task_index, len(all_tasks)))
    system, fold, seed = all_tasks[int(task_index)]
    outpath = task_path(system, fold, seed)
    if outpath.exists():
        print(f"skip_existing task={task_index} system={system['id']} fold={fold} seed={seed}", flush=True)
        return json.loads(outpath.read_text())
    device = resolve_device(device_name)
    selector = load_selector(cfg["e005d_root"], cfg["d14_selector_id"])
    print(f"task={task_index} system={system['id']} fold={fold} seed={seed} device={device}", flush=True)
    return run_task(system, fold, seed, cfg, device, selector)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task-index", type=int, required=True)
    ap.add_argument("--device", choices=["cpu", "cuda", "auto"], default="cpu")
    args = ap.parse_args()
    run_task_index(args.task_index, args.device)


if __name__ == "__main__":
    main()
