#!/usr/bin/env python3
"""Verify E126 source and notebook hashes and 25-game development arithmetic."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "release/e126"
MANIFEST = json.loads((BASE / "manifest.json").read_text(encoding="utf-8"))

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def cell_text(cell):
    text = cell.get("source", "")
    return "".join(text) if isinstance(text, list) else text

def verify():
    frozen = ROOT / "src/best_public_agent.py"
    agent = ROOT / "src/e126_submission_agent.py"
    notebook = ROOT / "notebooks/E126_Kaggle_Candidate.ipynb"
    ckpt = ROOT / "assets/e126/effect_prior_s11.pt"
    for path, key in (
        (frozen, "frozen_n117_sha256"),
        (ckpt, "peer_effect_checkpoint_sha256"),
        (agent, "full_agent_sha256"),
        (notebook, "notebook_sha256"),
    ):
        assert path.is_file() and sha256(path) == MANIFEST[key], (str(path), key)
    assert agent.read_bytes().startswith(frozen.read_bytes())
    assert MANIFEST["official_kaggle_submission"] is False

    nb = json.loads(notebook.read_text(encoding="utf-8"))
    assert nb.get("nbformat") == 4
    assert nb["metadata"]["kaggle"]["isInternetEnabled"] is False
    prefix = "%%writefile /tmp/my_agent.py\n"
    source = [cell_text(c)[len(prefix):] for c in nb["cells"] if cell_text(c).startswith(prefix)]
    assert source == [agent.read_text(encoding="utf-8")], "E126 notebook and source diverged"

    # Every reported arm/seed must have exactly 25 corresponding game records.
    all_arms = rows(ROOT / "results/e126_all_arms.csv")
    games = rows(ROOT / "results/e126_per_game.csv")
    groups = defaultdict(list)
    for r in games:
        groups[(r["family"], int(r["seed"]), r["arm"])].append(r)
    assert len(all_arms) == len(groups) == 45
    for r in all_arms:
        key = (r["family"], int(r["seed"]), r["arm"])
        group = groups[key]
        assert len(group) == len({g["game"] for g in group}) == 25, key
        assert int(r["games"]) == 25
        assert sum(int(g["completed_levels"]) for g in group) == int(r["completed_levels"]), key
        assert sum(int(g["actions"]) for g in group) == int(r["sdk_actions"]), key
        for k, threshold in (("L1", 1), ("L2", 2), ("L3plus", 3)):
            assert sum(int(g["completed_levels"]) >= threshold for g in group) == int(r[k]), (key, k)
        avg = sum(float(g["sdk_score_0_100"]) for g in group) / 25
        assert math.isclose(avg, float(r["mean_sdk_score_0_100"]), abs_tol=1e-8), key

    lookup = {(int(r["seed"]), r["arm"]): r for r in all_arms if r["family"] == "E126"}
    for seed, baseline in ((76, 15), (77, 14), (78, 15)):
        original = lookup[seed, "baseline"]
        hybrid = lookup[seed, "hybrid_trained"]
        assert int(original["completed_levels"]) == baseline
        assert (int(hybrid["L1"]), int(hybrid["L2"]), int(hybrid["L3plus"])) == (14, 2, 0)
        assert int(hybrid["completed_levels"]) == 16
        assert float(hybrid["mean_sdk_score_0_100"]) > float(original["mean_sdk_score_0_100"])
    robustness = rows(ROOT / "results/e126_robustness.csv")
    assert len(robustness) == 4
    assert [int(r["delta_levels"]) for r in robustness] == [1, 0, 0, 1]
    assert all(float(r["delta_sdk_mean"]) > 0 for r in robustness)

    build = BASE / "build"
    if build.exists():
        for path, expected in (
            (build / "my_agent.py", MANIFEST["full_agent_sha256"]),
            (build / "E126_Kaggle_Candidate.ipynb", MANIFEST["notebook_sha256"]),
        ):
            assert path.is_file() and sha256(path) == expected, str(path)
    print("PASS: E126 frozen-source hashes, notebook parity, 45 x 25 public game results")
    print("NOTE: no official Kaggle rerun or unseen-game generalisation is implied")

if __name__ == "__main__":
    verify()
