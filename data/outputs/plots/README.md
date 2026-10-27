# Plots and scientific scope

These SVG figures were generated from archived native experiments discussed in the project, not from hidden Kaggle games.

- **01**: frozen N093 vs local-effect native completions.
- **02**: 25-game per-level completion matrix. Blue marks the additional `tu93` Level-2 win.
- **03**: paired native charged action counts, **not** action efficiency or RHAE.
- **04**: action-effect policy ablations.
- **05**: observed Level-3 attempts; GAME_OVER may occur earlier than the 200-action per-level cap.
- **06**: prequential false-negative rates on *taken* actions.
- **07**: Level-2 failures by native termination type.

All 25 games are historically exposed. These figures are **not independent-generalization or official leaderboard evidence**. Original data are under `data/outputs/benchmarks/` and `data/outputs/experiments/`.

The optional `python3 scripts/generate_plots.py` command (requires `requirements-analysis.txt`) also produces `recomputed_e126_seed_levels.svg` and PNG, comparing the preserved N117 and E126 public SDK level counts by policy seed. Generated files are not new native evaluation evidence.
