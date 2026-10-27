#!/usr/bin/env python3
"""Print reproducible public-development results from committed CSVs."""
from pathlib import Path
import csv
ROOT = Path(__file__).resolve().parents[1]

def parse(name):
    with (ROOT / "data/outputs/benchmarks" / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    base = parse("n114_public25_matrix.csv")
    local = parse("n117_local_vs_frozen_25.csv")
    for title, rows, fields, action_col in (
        ("Frozen N093", base, ("l1", "l2", "l3plus"), "charged_sdk_actions"),
        ("Local-effect experiment", local, ("local_L1", "local_L2", "local_L3plus"), "local_charged")
    ):
        wins = [sum(int(r[f]) for r in rows) for f in fields]
        print(f"{title}: L1={wins[0]}, L2={wins[1]}, L3+={wins[2]}, total={sum(wins)}, native actions={sum(int(r[action_col]) for r in rows)}")
    with (ROOT / "experiments/E126/results/all_arms.csv").open(newline="", encoding="utf-8") as f:
        e126 = [row for row in csv.DictReader(f) if row["family"] == "E126"]
    arms = {(int(row["seed"]), row["arm"]): row for row in e126}
    for seed in (76, 77, 78):
        baseline, candidate = arms[(seed, "baseline")], arms[(seed, "hybrid_trained")]
        print(
            f"E126 policy seed {seed}: N117 control={baseline['completed_levels']} levels, "
            f"hybrid={candidate['completed_levels']} levels "
            f"(L1={candidate['L1']}, L2={candidate['L2']}, L3+={candidate['L3plus']}), "
            f"local SDK score={float(candidate['mean_sdk_score_0_100']):.6f}"
        )
    print("Offline, historically exposed public games; not an official Kaggle score.")

if __name__ == "__main__":
    main()
