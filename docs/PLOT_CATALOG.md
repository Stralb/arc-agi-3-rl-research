# Published result figures

The SVG files under `data/outputs/plots/` are regenerable representations of archived public SDK evaluation summaries; they are **not** new experiment results or private leaderboard charts.

Key charts already in the repository:

- `01_level_completions.svg` — frozen 14-level versus experimental 15-level distribution.
- `02_family_completion_matrix.svg` — which of 25 historically exposed families reached each level.
- `03_action_count_comparison.svg` — SDK actions; note shorter episodes may be earlier `GAME_OVER`.
- `04_effect_prior_ablations.svg` — no additional Level-3 success across classifier variants.
- `05_level3_native_attempts.svg` — observed failure horizons on Level-3 attempts.
- `06_predictor_false_negative_risk.svg` — why hard action masking is unsafe.
- `07_level2_failure_modes.svg` — termination versus per-level budget exhaustion.

To generate independently constructed SVG and PNG figures directly from the committed per-family CSV files:

```bash
python3 -m pip install -r requirements-analysis.txt
python3 scripts/generate_plots.py
```

The recomputed files are written to `data/outputs/plots/recomputed_*.svg` and `*.png`. The plot generator never accesses restricted game binaries or private competition material.

The local plot-generation script additionally builds a per-policy-seed N117 vs E126 comparison as `recomputed_e126_seed_levels.svg` (and PNG) from the committed E126 CSV. It is **not** included among the archived native figures; run the script to regenerate it.
