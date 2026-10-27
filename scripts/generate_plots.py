#!/usr/bin/env python3
"""Regenerate public-development charts from committed summary CSV files.
Only aggregated public-development results are plotted; no SDK access is used.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/outputs/plots"
OUT.mkdir(parents=True, exist_ok=True)

def rows(name):
    with (ROOT / "data/outputs/benchmarks" / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = rows("n117_local_vs_frozen_25.csv")
    labels = ["Level 1", "Level 2", "Level 3+"]
    frozen = [sum(int(r[k]) for r in data) for k in ("baseline_L1","baseline_L2","baseline_L3plus")]
    local = [sum(int(r[k]) for r in data) for k in ("local_L1","local_L2","local_L3plus")]
    xs = [0, 1, 2]
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.bar([x - .18 for x in xs], frozen, width=.36, label="Frozen N093")
    ax.bar([x + .18 for x in xs], local, width=.36, label="Local effect-memory")
    ax.set_xticks(xs, labels)
    ax.set_ylabel("Native levels completed")
    ax.set_title("25 historically exposed public games — not hidden Kaggle score")
    ax.legend()
    for i, v in enumerate(frozen):
        ax.text(i-.18, v+.15, str(v), ha="center", fontsize=9)
    for i, v in enumerate(local):
        ax.text(i+.18, v+.15, str(v), ha="center", fontsize=9)
    ax.set_ylim(0, 15)
    fig.tight_layout()
    fig.savefig(OUT / "recomputed_level_completions.svg")
    fig.savefig(OUT / "recomputed_level_completions.png", dpi=160)
    plt.close(fig)

    data.sort(key=lambda r: r["family"])
    arr = [[int(r[k]) for k in ("baseline_L1","baseline_L2","baseline_L3plus",
                               "local_L1","local_L2","local_L3plus")] for r in data]
    fig, ax = plt.subplots(figsize=(8, 9))
    ax.imshow(arr, aspect="auto", cmap="Greens", vmin=0, vmax=1)
    ax.set_yticks(range(len(data)), [r["family"] for r in data])
    ax.set_xticks(range(6), ["N093 L1","N093 L2","N093 L3","Local L1","Local L2","Local L3"],
                  rotation=40, ha="right")
    ax.set_title("Native public level advancement by family")
    ax.set_xlabel("Controller and level")
    fig.tight_layout()
    fig.savefig(OUT / "recomputed_family_completion_matrix.svg")
    fig.savefig(OUT / "recomputed_family_completion_matrix.png", dpi=160)
    plt.close(fig)
    # Later E126 public-development comparison, separate from N093/N117 baseline.
    with (ROOT / "experiments/E126/results/all_arms.csv").open(newline="", encoding="utf-8") as f:
        release_rows = [row for row in csv.DictReader(f) if row["family"] == "E126"]
    release = {(int(row["seed"]), row["arm"]): row for row in release_rows}
    seeds = (76, 77, 78)
    base_levels = [int(release[(seed, "baseline")]["completed_levels"]) for seed in seeds]
    hybrid_levels = [int(release[(seed, "hybrid_trained")]["completed_levels"]) for seed in seeds]
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.bar([s - .18 for s in range(3)], base_levels, width=.36, label="N117 control")
    ax.bar([s + .18 for s in range(3)], hybrid_levels, width=.36, label="E126 hybrid")
    ax.set_xticks(range(3), [str(seed) for seed in seeds])
    ax.set_xlabel("Policy seed")
    ax.set_ylabel("Completed public-game levels")
    ax.set_ylim(0, 18)
    ax.set_title("E126 on exposed games (not hidden Kaggle score)")
    ax.legend()
    for i, value in enumerate(base_levels):
        ax.text(i - .18, value + .15, str(value), ha="center", fontsize=9)
    for i, value in enumerate(hybrid_levels):
        ax.text(i + .18, value + .15, str(value), ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "recomputed_e126_seed_levels.svg")
    fig.savefig(OUT / "recomputed_e126_seed_levels.png", dpi=160)
    plt.close(fig)
    print("Regenerated N093/N117 and E126 public-result charts (no SDK used).")

if __name__ == "__main__":
    main()
