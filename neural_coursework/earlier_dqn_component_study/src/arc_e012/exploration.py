from __future__ import annotations

import copy
import json
import math
import random
from collections import defaultdict
from pathlib import Path

import numpy as np

from arc_e004.abstraction import action_bucket, state_key
from arc_e004.actions import CandidateAction
from arc_e005.tournament import (
    bucket_candidates,
    choose_action,
    expand_bucket_values,
    visual_salience,
)

from .action_bank import ActionKey
from .policy import should_use_structured, type_prior_random_action


def load_selector(e005d_root: str | Path, selector_id: str) -> dict:
    cfg_path = Path(e005d_root) / "configs/e005.json"
    cfg = json.loads(cfg_path.read_text())
    for selector in cfg.get("selectors", []):
        if selector.get("id") == selector_id:
            return copy.deepcopy(selector)
    raise KeyError(f"Selector {selector_id!r} not found in {cfg_path}")


def candidate_to_key(c: CandidateAction) -> ActionKey:
    if int(c.action_id) == 6:
        return ActionKey(int(c.action_id), int(c.x), int(c.y))
    return ActionKey(int(c.action_id))


class D14Explorer:
    """E005 D14 used only inside the epsilon-exploration branch.

    Counts include every executed action, including greedy RL actions. This makes
    D14's novelty signal describe what the integrated agent has actually tried,
    rather than only the subset of actions proposed by D14 itself.
    """

    def __init__(self, selector: dict, click_action_id: int = 6, click_size: int = 64):
        self.selector = copy.deepcopy(selector)
        self.click_action_id = int(click_action_id)
        self.click_size = int(click_size)
        self.pair_counts = defaultdict(int)
        self.structured_calls = 0

    @property
    def action6_prob(self) -> float:
        return float(self.selector.get("action6_prob", 0.7))

    def type_prior_action(self, available, rng: random.Random) -> ActionKey:
        return type_prior_random_action(
            available,
            rng,
            self.click_action_id,
            self.click_size,
            self.action6_prob,
        )

    def structured_action(
        self,
        *,
        rng: random.Random,
        available: list[int],
        grid: np.ndarray,
        emb: np.ndarray,
        simple: list[int],
        prior_simple_logits: np.ndarray,
        prior_a6_logits: np.ndarray | None,
    ) -> ActionKey:
        _feats, meta = bucket_candidates(emb, simple)
        sk = state_key(grid, "downsample16")
        count_map = {}
        for m in meta:
            mt = tuple(m)
            count_map[mt] = 1.0 / math.sqrt(self.pair_counts[(sk, mt)] + 1.0)
        expanded_count = expand_bucket_values(count_map, simple)

        simple_logits = np.asarray(prior_simple_logits, dtype=np.float64)
        a6_logits = None if prior_a6_logits is None else np.asarray(prior_a6_logits, dtype=np.float64)
        zeros_s = np.zeros(len(simple), dtype=np.float64)
        zeros_6 = None if a6_logits is None else np.zeros((64, 64), dtype=np.float64)
        sal6 = visual_salience(grid, self.selector, rng) if a6_logits is not None else None
        signals = {
            "effect": (simple_logits, a6_logits),
            "salience": (zeros_s, sal6),
            "count": expanded_count,
        }
        for name in [
            "repeat", "exact_repeat", "danger", "rnd", "drnd", "rff",
            "disagree", "re3", "mechanics", "learnprog", "graph", "reverse",
        ]:
            signals[name] = (zeros_s, zeros_6)

        chosen = choose_action(rng, self.selector, available, simple, signals)
        self.structured_calls += 1
        return candidate_to_key(chosen)

    def choose(
        self,
        *,
        system: dict,
        rng: random.Random,
        action_index: int,
        since_progress: int,
        available: list[int],
        grid: np.ndarray,
        emb: np.ndarray,
        simple: list[int],
        prior_simple_logits: np.ndarray,
        prior_a6_logits: np.ndarray | None,
    ) -> tuple[ActionKey, str]:
        policy = system.get("exploration_policy", "uniform")
        if policy == "type_prior":
            return self.type_prior_action(available, rng), "type_prior"
        if policy != "d14":
            raise ValueError(f"Unsupported exploration policy for D14Explorer: {policy}")
        if should_use_structured(system, action_index, since_progress, rng):
            return self.structured_action(
                rng=rng,
                available=available,
                grid=grid,
                emb=emb,
                simple=simple,
                prior_simple_logits=prior_simple_logits,
                prior_a6_logits=prior_a6_logits,
            ), "d14"
        return self.type_prior_action(available, rng), "type_prior"

    def observe(self, grid: np.ndarray, action: ActionKey) -> None:
        c = CandidateAction(int(action.action_id), int(action.x), int(action.y)) if int(action.action_id) == self.click_action_id else CandidateAction(int(action.action_id))
        bucket = tuple(action_bucket(c.vector(), coord_block=8))
        sk = state_key(grid, "downsample16")
        self.pair_counts[(sk, bucket)] += 1
