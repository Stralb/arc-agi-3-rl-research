from __future__ import annotations

import json
import random
from collections import defaultdict

import numpy as np

from .tournament import ROOT, load_cfg, safe_dump, systems, tasks


def load_runs() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted((ROOT / "results" / "runs").glob("*.json"))]


def flatten(runs: list[dict]) -> list[dict]:
    return [row for run in runs for row in run["rows"]]


def mean_or_none(xs):
    vals = [float(x) for x in xs if x is not None]
    return float(np.mean(vals)) if vals else None


def summarize(rows: list[dict]) -> dict:
    keys = [
        "progress_by_50", "progress_by_100", "progress_by_250", "progress_by_600",
        "completion_cap", "levels_completed", "reward_total", "death_per_100",
        "noop_rate", "changed_rate", "repeat_action_state_rate", "action6_rate",
        "unique_raw_states", "updates", "parameter_delta_l2", "mean_loss",
        "mean_abs_td", "epsilon_action_fraction", "epsilon_structured_fraction",
        "d14_fraction_of_epsilon", "d14_action6_rate", "elapsed_seconds", "actions_per_second",
    ]
    out = {"n_game_runs": len(rows)}
    for k in keys:
        out[k] = mean_or_none([r.get(k) for r in rows])
    out["first_progress_when_seen"] = mean_or_none([r.get("first_progress") for r in rows])
    return out


def paired_game_deltas(rows: list[dict], a: str, b: str, metric: str) -> dict:
    xa = {(r["game"], int(r["seed"])): float(r[metric]) for r in rows if r["system_id"] == a and r.get(metric) is not None}
    xb = {(r["game"], int(r["seed"])): float(r[metric]) for r in rows if r["system_id"] == b and r.get(metric) is not None}
    keys = sorted(set(xa) & set(xb))
    by_game = defaultdict(list)
    for g, s in keys:
        by_game[g].append(xa[(g, s)] - xb[(g, s)])
    game_delta = {g: float(np.mean(v)) for g, v in by_game.items()}
    return {
        "mean": float(np.mean(list(game_delta.values()))) if game_delta else 0.0,
        "game_deltas": game_delta,
        "n_games": len(game_delta),
    }


def bootstrap_ci(game_deltas: dict[str, float], reps: int, seed: int) -> list[float]:
    vals = list(game_deltas.values())
    if not vals:
        return [0.0, 0.0]
    rng = random.Random(seed)
    n = len(vals)
    sims = [float(np.mean([vals[rng.randrange(n)] for _ in range(n)])) for _ in range(reps)]
    return [float(np.quantile(sims, 0.025)), float(np.quantile(sims, 0.975))]


def rank_key(s: dict):
    return (
        s.get("progress_by_600") or 0.0,
        s.get("completion_cap") or 0.0,
        s.get("progress_by_250") or 0.0,
        s.get("reward_total") or 0.0,
        -(s.get("first_progress_when_seen") if s.get("first_progress_when_seen") is not None else 1e9),
        -(s.get("death_per_100") or 0.0),
    )


def compare(rows: list[dict], a: str, b: str, reps: int, seed_base: int) -> dict:
    c = {"a": a, "b": b}
    metrics = ["progress_by_600", "progress_by_250", "completion_cap", "reward_total", "death_per_100", "action6_rate"]
    for i, metric in enumerate(metrics):
        d = paired_game_deltas(rows, a, b, metric)
        d["ci95"] = bootstrap_ci(d["game_deltas"], reps, seed_base + i * 17)
        c[metric] = d
    return c


def behavior_tuple(s: dict):
    return (
        float(s.get("progress_by_600") or 0.0),
        float(s.get("completion_cap") or 0.0),
        float(s.get("progress_by_250") or 0.0),
        float(s.get("reward_total") or 0.0),
    )


def main():
    cfg = load_cfg()
    runs = load_runs()
    expected = len(tasks(cfg))
    if len(runs) != expected:
        raise RuntimeError(f"Expected {expected} run files, found {len(runs)}")

    rows = flatten(runs)
    by = defaultdict(list)
    for r in rows:
        by[r["system_id"]].append(r)

    summaries = [{"id": sid, **summarize(rs)} for sid, rs in by.items()]
    summaries.sort(key=rank_key, reverse=True)
    for i, s in enumerate(summaries, 1):
        s["rank"] = i

    full_id = cfg["full_system_id"]
    full = next(s for s in summaries if s["id"] == full_id)
    reps = int(cfg["selection"]["bootstrap_reps"])
    comparisons = {}
    for i, s in enumerate(summaries):
        if s["id"] == full_id:
            continue
        comparisons[s["id"]] = compare(rows, full_id, s["id"], reps, 12012 + i * 101)

    # E012 is a consolidation, not a fresh architecture search. Keep the full
    # stack unless an ablation is behaviorally better on the matched evaluation.
    ablations_better = [s for s in summaries if s["id"] != full_id and behavior_tuple(s) > behavior_tuple(full)]
    if ablations_better:
        best = max(ablations_better + [full], key=rank_key)
        decision = "E012_COMPONENT_REVIEW_REQUIRED"
        selected = best
    else:
        decision = "E012_FULL_STACK_CONFIRMED"
        selected = full

    out = {
        "experiment_id": cfg["experiment_id"],
        "summaries": summaries,
        "comparisons_full_minus_ablation": comparisons,
        "decision": decision,
        "selected": selected,
        "full": full,
        "expected_tasks": expected,
        "n_game_runs_per_system": len(cfg["evaluation"]["folds"]) * len(cfg["evaluation"]["seeds"]) * 5,
        "selection_rule": "E012 is a matched final ablation. Keep the E009-derived full stack unless an ablation is behaviorally better on p600, completion-cap, p250, then reward. Exact ties keep the full stack; any ablation win triggers component review rather than silently rewriting prior conclusions.",
        "generalization_guardrail": "All 25 public ARC-AGI-3 games are development-exposed. E012 freezes the DQN development baseline; it is not hidden-game evidence and its sparse progress metrics are not the official Kaggle score.",
    }
    safe_dump(out, ROOT / "results" / "ABLATION_RESULTS.json")
    safe_dump(out, ROOT / "results" / "LOCK_IN.json")
    print(json.dumps(out, indent=2)[:20000])


if __name__ == "__main__":
    main()
