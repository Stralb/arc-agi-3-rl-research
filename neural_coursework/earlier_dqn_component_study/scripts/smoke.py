from __future__ import annotations

import torch

from arc_e005.tournament import load_fold_model
from arc_e012.exploration import load_selector
from arc_e012.tournament import load_cfg, systems, run_game


def main():
    cfg = load_cfg()
    device = torch.device("cpu")
    seed = cfg["evaluation"]["seeds"][0]
    prior, _, _ = load_fold_model(0, device, seed)
    selector = load_selector(cfg["e005d_root"], cfg["d14_selector_id"])
    by = {s["id"]: s for s in systems(cfg)}
    game = cfg["folds"][0][0]
    gi = cfg["all_public_games"].index(game)

    full = run_game(game, gi, 0, seed, by["E12_F_full_dueling_d14"], 20, prior, selector, device, cfg)
    no_d14 = run_game(game, gi, 0, seed, by["E12_A_no_d14"], 20, prior, selector, device, cfg)
    no_duel = run_game(game, gi, 0, seed, by["E12_A_no_dueling"], 20, prior, selector, device, cfg)

    assert full["action_steps"] > 0 and no_d14["action_steps"] > 0 and no_duel["action_steps"] > 0
    assert full["d14_calls"] > 0, full
    assert no_d14["d14_calls"] == 0, no_d14
    print("E012_SMOKE_OK")
    print("GAME", game, "FULL_STEPS", full["action_steps"], "FULL_D14_CALLS", full["d14_calls"])


if __name__ == "__main__":
    main()
