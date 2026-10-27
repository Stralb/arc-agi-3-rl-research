#!/usr/bin/env python3
"""Print the archived public SDK comparisons (not official Kaggle results)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "results"

def read(name):
    with (ROOT / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    frozen = read("n093_public25.csv")
    local = read("n117_public25.csv")
    for name, rows, cols, action_col in (
        ("N093", frozen, ("l1", "l2", "l3plus"), "charged_sdk_actions"),
        ("N117", local, ("local_L1", "local_L2", "local_L3plus"), "local_charged"),
    ):
        levels = [sum(int(row[col]) for row in rows) for col in cols]
        actions = sum(int(row[action_col]) for row in rows)
        print(f"{name}: L1={levels[0]}, L2={levels[1]}, L3+={levels[2]}, total={sum(levels)}, actions={actions}")
    arms = {(int(r["seed"]), r["arm"]): r for r in read("e126_all_arms.csv") if r["family"] == "E126"}
    for seed in (76, 77, 78):
        b = arms[seed, "baseline"]
        a = arms[seed, "hybrid_trained"]
        print(f"E126 seed {seed}: N117={b['completed_levels']}, hybrid={a['completed_levels']} levels; local SDK mean={float(a['mean_sdk_score_0_100']):.6f}")
    print("All results are from exposed public games. These are not private Kaggle scores.")

if __name__ == "__main__":
    main()
