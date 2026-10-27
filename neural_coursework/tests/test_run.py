import json

import numpy as np

from src.config import RunConfig
from src.run import run


def test_random_policies_run_and_record(arc, tmp_path):
    for algo in ("random_type", "random_flat"):
        rec = run(RunConfig(algo=algo, game="ls20", budget=300, seed=1), arc=arc, out_dir=str(tmp_path))
        c = rec["counters"]
        assert rec["status"] == "budget" and c["scorer_actions"] == 300 == c["sdk_total_actions"]
        assert rec["official_score"]["score"] is not None
        assert len(rec["identity"]["config_hash"]) == 12 and rec["identity"]["schema_version"] == 1
        d = list(tmp_path.glob(f"{algo}-V0-ls20-s1-*"))[0]
        assert json.loads((d / "record.json").read_text())["identity"]["run_id"] == d.name
        assert len(np.load(d / "actions.npy")) == 300 - (c["resets"] - 1)     # steps = budget minus counted resets


def test_same_seed_same_trajectory_different_seed_differs(arc):
    a = run(RunConfig(algo="random_type", game="ls20", budget=200, seed=5), arc=arc)
    b = run(RunConfig(algo="random_type", game="ls20", budget=200, seed=5), arc=arc)
    c = run(RunConfig(algo="random_type", game="ls20", budget=200, seed=6), arc=arc)
    assert a["diagnostics"]["progress_curve"] == b["diagnostics"]["progress_curve"]
    assert a["diagnostics"]["unique_states"] == b["diagnostics"]["unique_states"]
    assert a["cost"]["wall_s"] > 0
    assert a["diagnostics"]["action_type_counts"] != c["diagnostics"]["action_type_counts"]


def test_no_reset_after_budget_exhaustion(arc):
    from src.adapter import ArcSession, sample_type_uniform
    rng = np.random.default_rng(0)
    s = ArcSession(arc)
    s.start_run("sb26", budget=250)
    while not s.done:
        s.step(sample_type_uniform(rng, s.obs.mask))
    assert s.tracker.actions == 250
    assert s.scorecard()["total_actions"] == 250          # a trailing reset would have made this 251


def test_config_hash_stable_and_resolved():
    a = RunConfig(algo="dqn", game="ls20").resolved()
    b = RunConfig(algo="dqn", game="ls20", params={"lr": 1e-4}).resolved()
    c = RunConfig(algo="dqn", game="ls20", params={"lr": 3e-4}).resolved()
    assert a.hash() == b.hash() != c.hash()
    assert a.params["replay_capacity"] == 50000 and a.arch["id"] == "onehotcnn_stack2"
