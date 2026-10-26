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
    print("Offline, historically exposed public games; not Kaggle score.")

if __name__ == "__main__":
    main()
