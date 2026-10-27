#!/usr/bin/env python3
"""Offline integrity verification for the E126 public-development release.

This does not execute the ARC SDK, run model inference or verify Kaggle scores.
"""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/E126"
MANIFEST = json.loads((BASE / "manifest.json").read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def cell_text(cell: dict) -> str:
    s = cell.get("source", "")
    return "".join(s) if isinstance(s, list) else s


def verify() -> None:
    frozen = ROOT / "src/best_public_agent.py"
    agent = ROOT / "src/e126_submission_agent.py"
    checkpoint = ROOT / "assets/e126/effect_prior_s11.pt"
    notebook = ROOT / "notebooks/E126_Kaggle_Candidate.ipynb"
    paths = (
        (frozen, "frozen_n117_sha256"),
        (checkpoint, "peer_effect_checkpoint_sha256"),
        (agent, "full_agent_sha256"),
        (notebook, "notebook_sha256"),
    )
    for path, key in paths:
        assert path.is_file(), f"Missing E126 artifact: {path}"
        assert digest(path) == MANIFEST[key], f"E126 checksum mismatch: {path}"
    assert agent.read_bytes().startswith(frozen.read_bytes()), "Frozen N117 prefix changed"
    assert MANIFEST["official_kaggle_submission"] is False

    nb = json.loads(notebook.read_text(encoding="utf-8"))
    assert nb.get("nbformat") == 4, "Invalid E126 notebook"
    assert nb.get("metadata", {}).get("kaggle", {}).get("isInternetEnabled") is False
    payloads = [
        cell_text(c).removeprefix("%%writefile /tmp/my_agent.py\n")
        for c in nb.get("cells", [])
        if cell_text(c).startswith("%%writefile /tmp/my_agent.py\n")
    ]
    assert len(payloads) == 1 and payloads[0] == agent.read_text(encoding="utf-8"), (
        "Embedded notebook source differs from committed E126 agent"
    )

    with (BASE / "results/all_arms.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    controls = {(int(r["seed"]), r["arm"]): r for r in rows if r["family"] == "E126"}
    assert sorted({key[0] for key in controls}) == [76, 77, 78]
    for seed in (76, 77, 78):
        control = controls[seed, "baseline"]
        treatment = controls[seed, "hybrid_trained"]
        assert int(treatment["completed_levels"]) == 16
        assert int(treatment["L1"]) == 14 and int(treatment["L2"]) == 2
        assert int(treatment["L3plus"]) == 0
        assert int(control["completed_levels"]) == (14 if seed == 77 else 15)
        assert float(treatment["mean_sdk_score_0_100"]) > float(control["mean_sdk_score_0_100"])
    with (BASE / "results/robustness_summary.csv").open(newline="", encoding="utf-8") as f:
        robustness = list(csv.DictReader(f))
    assert len(robustness) == 4
    assert all(int(r["delta_levels"]) >= 0 for r in robustness)
    assert all(float(r["delta_sdk_mean"]) > 0 for r in robustness)

    build = BASE / "build"
    if build.is_dir():
        for built, expected in (
            (build / "my_agent.py", MANIFEST["full_agent_sha256"]),
            (build / "E126_Kaggle_Candidate.ipynb", MANIFEST["notebook_sha256"]),
        ):
            assert built.is_file() and digest(built) == expected, (
                f"Deterministic E126 rebuild differs: {built}"
            )
    print("PASS: E126 hashes, N117 prefix, embedded notebook, seed-level arithmetic")
    print("NOTE: native SDK and official Kaggle submission NOT verified")


if __name__ == "__main__":
    verify()
