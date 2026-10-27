from __future__ import annotations

import json
from pathlib import Path

from arc_e012.action_bank import ActionBank
from arc_e012.exploration import load_selector
from arc_e012.tournament import load_cfg, systems, tasks


def winner_id(lock: dict):
    w = lock.get("winner", lock.get("selected", {}))
    return w.get("id") if isinstance(w, dict) else str(w)


def main():
    cfg = load_cfg()
    e004 = Path(cfg["e004_root"])
    e005 = Path(cfg["e005d_root"])
    e008 = Path(cfg["e008_root"])
    e009 = Path(cfg["e009_root"])
    e011 = Path(cfg["e011_root"])

    assert (e004 / "src/arc_e004").is_dir()
    assert (e005 / "src/arc_e005").is_dir()
    for root in (e008, e009, e011):
        assert (root / "results/LOCK_IN.json").is_file(), root

    l8 = json.loads((e008 / "results/LOCK_IN.json").read_text())
    l9 = json.loads((e009 / "results/LOCK_IN.json").read_text())
    l11 = json.loads((e011 / "results/LOCK_IN.json").read_text())
    assert winner_id(l8) == cfg["required_e008_winner_id"], (winner_id(l8), cfg["required_e008_winner_id"])
    assert winner_id(l9) == cfg["required_e009_winner_id"], (winner_id(l9), cfg["required_e009_winner_id"])
    assert l11.get("decision") == cfg["required_e011_decision"], (l11.get("decision"), cfg["required_e011_decision"])

    d14 = load_selector(e005, cfg["d14_selector_id"])
    assert d14["id"] == cfg["d14_selector_id"]

    ss = systems(cfg)
    assert len(ss) == 4
    ids = {s["id"] for s in ss}
    assert ids == {"E12_F_full_dueling_d14", "E12_A_no_d14", "E12_A_no_dueling", "E12_A_plain_ddqn"}
    by = {s["id"]: s for s in ss}
    assert by["E12_F_full_dueling_d14"]["dueling"] is True and by["E12_F_full_dueling_d14"]["exploration_policy"] == "d14"
    assert by["E12_A_no_d14"]["dueling"] is True and by["E12_A_no_d14"]["exploration_policy"] == "uniform"
    assert by["E12_A_no_dueling"]["dueling"] is False and by["E12_A_no_dueling"]["exploration_policy"] == "d14"
    assert by["E12_A_plain_ddqn"]["dueling"] is False and by["E12_A_plain_ddqn"]["exploration_policy"] == "uniform"
    for s in ss:
        assert s["learn"] is True
        assert s["n_step"] == 1
        assert s["per"] is False
        assert s["distributional"] is False

    all_tasks = tasks(cfg)
    assert len(all_tasks) == cfg["evaluation"]["expected_tasks"] == 60

    bank = ActionBank(cfg["click_action_id"], cfg["click_size"], max_action_id=cfg["max_action_id"])
    keys, enc = bank.encode_candidates([3, 4, 6, 7])
    assert len(keys) == 4099
    assert enc.shape == (4099, 10)
    assert any(k.action_id == 7 for k in keys)

    print("E012_PREFLIGHT_OK")
    print("E008_WINNER", winner_id(l8))
    print("E009_WINNER", winner_id(l9))
    print("E011_DECISION", l11.get("decision"))
    print("SYSTEMS", [s["id"] for s in ss])
    print("TASKS", len(all_tasks), "GAME_RUNS", len(all_tasks) * 5)


if __name__ == "__main__":
    main()
