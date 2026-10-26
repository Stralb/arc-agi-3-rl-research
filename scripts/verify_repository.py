#!/usr/bin/env python3
"""Offline integrity and arithmetic verification of the files ACTUALLY committed.
This does not run the native SDK, validate Kaggle scoring or check omitted archives.
"""
from pathlib import Path
from hashlib import sha256
import csv
import json
import ast

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = {
    "src/baselines/frozen_n093.py": "e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d",
    "notebooks/frozen_n093_submission.ipynb": "1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4",
    "src/best_public_agent.py": "0663845070e47a053076db54243c3445921a06b4bf0908b7b233c263da423bfa",
    "notebooks/local_effect_best_public.ipynb": "0f049935a633a14ba82c0427386e5eef852f3a8972aa205b61a3ca0e70c01acd",
}

def load_rows(relpath):
    with (ROOT / relpath).open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))

def verify():
    for relative, expected in EXPECTED_SHA256.items():
        path = ROOT / relative
        assert path.is_file(), f"Missing frozen/evaluated source: {relative}"
        actual = sha256(path.read_bytes()).hexdigest()
        assert actual == expected, f"Unexpected byte change: {relative}: {actual}"
    for rel in ("src/baselines/frozen_n093.py", "src/best_public_agent.py"):
        ast.parse((ROOT / rel).read_text(encoding="utf-8"), filename=rel)
    for rel in ("notebooks/frozen_n093_submission.ipynb", "notebooks/local_effect_best_public.ipynb"):
        notebook = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        assert notebook.get("nbformat") == 4 and any(
            c.get("cell_type") == "code" for c in notebook.get("cells", [])
        ), f"Invalid notebook: {rel}"

    frozen = load_rows("data/outputs/benchmarks/n114_public25_matrix.csv")
    local = load_rows("data/outputs/benchmarks/n117_local_vs_frozen_25.csv")
    assert len(frozen) == len(local) == 25
    assert len({r["game"] for r in frozen}) == 25
    assert len({r["family"] for r in local}) == 25
    flevels = tuple(sum(int(r[k]) for r in frozen) for k in ("l1", "l2", "l3plus"))
    llevels = tuple(sum(int(r[k]) for r in local) for k in ("local_L1", "local_L2", "local_L3plus"))
    assert flevels == (13, 1, 0), flevels
    assert llevels == (13, 2, 0), llevels
    assert sum(int(r["charged_sdk_actions"]) for r in frozen) == 2982
    assert sum(int(r["local_charged"]) for r in local) == 2790
    assert {r["family"] for r in local if int(r["local_L2"])} == {"vc33", "tu93"}
    assert {r["family"] for r in local if int(r["baseline_L2"])} == {"vc33"}

    for rel in ("notebooks/README.md", "docs/ARCHITECTURE.md", "reports/RESEARCH_SUMMARY.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "The requested file reference is not currently visible" not in text, rel
    plots = list((ROOT / "data/outputs/plots").glob("*.svg"))
    assert len(plots) >= 5, "SVG plots missing"
    print("PASS: published source hashes, notebooks, 25-game arithmetic, derived SVG figures")
    print("NOTE: original native SDK/frames and uncommitted archive bytes are NOT verified")

if __name__ == "__main__":
    verify()
