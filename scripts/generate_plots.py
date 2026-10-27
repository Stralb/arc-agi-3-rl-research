#!/usr/bin/env python3
"""Regenerate comparison charts from saved public-game CSVs (no SDK calls)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "plots"

def read(path):
    with (RESULTS / path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    OUT.mkdir(parents=True, exist_ok=True)

    frozen = read("n093_public25.csv")
    local = read("n117_public25.csv")
    arms = {(int(r["seed"]), r["arm"]): r for r in read("e126_all_arms.csv") if r["family"] == "E126"}

    names = ("N093", "N117", "E126 seed 76")
    counts = (
        sum(int(r["l1"]) + int(r["l2"]) + int(r["l3plus"]) for r in frozen),
        sum(int(r["local_L1"]) + int(r["local_L2"]) + int(r["local_L3plus"]) for r in local),
        int(arms[76, "hybrid_trained"]["completed_levels"]),
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(names, counts)
    ax.set_ylim(0, 18)
    ax.set_ylabel("Completed public-game levels")
    ax.set_title("Archived development results, not Kaggle scores")
    for i, n in enumerate(counts):
        ax.text(i, n + .2, str(n), ha="center")
    fig.tight_layout()
    fig.savefig(OUT / "recomputed_level_comparison.svg")
    fig.savefig(OUT / "recomputed_level_comparison.png", dpi=160)
    plt.close(fig)

    seeds = (76, 77, 78)
    control = [int(arms[s, "baseline"]["completed_levels"]) for s in seeds]
    candidate = [int(arms[s, "hybrid_trained"]["completed_levels"]) for s in seeds]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([i - .18 for i in range(3)], control, width=.36, label="N117")
    ax.bar([i + .18 for i in range(3)], candidate, width=.36, label="E126")
    ax.set_xticks(range(3), [str(s) for s in seeds])
    ax.set_ylim(0, 18)
    ax.set_xlabel("Policy seed")
    ax.set_ylabel("Completed public-game levels")
    ax.set_title("Matched local SDK runs, exposed environments")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "recomputed_e126_by_seed.svg")
    fig.savefig(OUT / "recomputed_e126_by_seed.png", dpi=160)
    plt.close(fig)
    print("Regenerated four plot files from committed CSVs; no SDK or Kaggle run")

if __name__ == "__main__":
    main()
