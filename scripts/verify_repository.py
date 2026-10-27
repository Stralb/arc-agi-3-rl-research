#!/usr/bin/env python3
"""Check immutable agent sources and the saved public results; no SDK calls."""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASHES = {
    "src/baselines/frozen_n093.py": "e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d",
    "src/best_public_agent.py": "0663845070e47a053076db54243c3445921a06b4bf0908b7b233c263da423bfa",
}

def read_csv(path: str):
    with (ROOT / path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def verify():
    for relative, expected in HASHES.items():
        file = ROOT / relative
        assert file.is_file(), f"Missing frozen source: {relative}"
        assert hashlib.sha256(file.read_bytes()).hexdigest() == expected, relative
        ast.parse(file.read_text(encoding="utf-8"), filename=relative)
    ast.parse((ROOT / "src/e126_submission_agent.py").read_text(), filename="e126_submission_agent.py")
    ast.parse((ROOT / "src/algorithms/local_effect_policy.py").read_text(), filename="local_effect_policy.py")
    assert (ROOT / "assets/e126/effect_prior_s11.pt").is_file()

    frozen = read_csv("results/n093_public25.csv")
    local = read_csv("results/n117_public25.csv")
    assert len(frozen) == len(local) == 25
    assert len({r["game"] for r in frozen}) == 25
    assert {r["game"] for r in frozen} == {r["family"] for r in local}
    b_levels = tuple(sum(int(r[k]) for r in frozen) for k in ("l1", "l2", "l3plus"))
    l_levels = tuple(sum(int(r[k]) for r in local) for k in ("local_L1", "local_L2", "local_L3plus"))
    assert b_levels == (13, 1, 0), b_levels
    assert l_levels == (13, 2, 0), l_levels
    assert sum(int(r["charged_sdk_actions"]) for r in frozen) == 2982
    assert sum(int(r["local_charged"]) for r in local) == 2790
    assert {r["family"] for r in local if int(r["local_L2"])} == {"vc33", "tu93"}
    assert {r["family"] for r in local if int(r["baseline_L2"])} == {"vc33"}

    ablations = read_csv("results/n117_ablations.csv")
    arms = {r["arm"]: r for r in ablations}
    assert int(arms["local"]["L2"]) == 2
    assert int(arms["local_any_pixel"]["L2"]) == 1
    assert int(arms["local_shuffled"]["L2"]) == 1
    assert len(list((ROOT / "results/plots").glob("*.svg"))) == 4
    for svg in (ROOT / "results/plots").glob("*.svg"):
        assert ET.parse(svg).getroot().tag.endswith("svg"), svg

    notebook = json.loads((ROOT / "notebooks/E126_Kaggle_Candidate.ipynb").read_text())
    assert notebook["nbformat"] == 4
    assert any(c["cell_type"] == "code" for c in notebook["cells"])
    print("PASS: immutable N093/N117 sources, local SDK results, ablations and figures")
    print("NOTE: neither native SDK runs nor official Kaggle submissions are tested here")

if __name__ == "__main__":
    verify()
