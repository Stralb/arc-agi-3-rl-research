#!/usr/bin/env python3
"""Regenerate two visualizations from verified public-game summary CSV files.
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
    print("Regenerated SVG and PNG figures from committed 25-family results.")

if __name__ == "__main__":
    main()
