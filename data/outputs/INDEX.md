# Public output and visualization index

This directory holds curated **derived** tabular evidence from permitted, historically exposed public-game runs. The full original binary/native-frame archives are not hosted in this public tree; see [repository coverage](../../docs/REPOSITORY_COVERAGE.md).

## Benchmark and experiment files

| Path | Type |
|---|---|
| [`benchmarks/local_effect_vs_n093.csv`](benchmarks/local_effect_vs_n093.csv) | CSV results |
| [`benchmarks/n114_public25_matrix.csv`](benchmarks/n114_public25_matrix.csv) | CSV results |
| [`benchmarks/n117_local_vs_frozen_25.csv`](benchmarks/n117_local_vs_frozen_25.csv) | CSV results |
| [`experiments/N108/per_family.csv`](experiments/N108/per_family.csv) | CSV results |
| [`experiments/N109/per_family.csv`](experiments/N109/per_family.csv) | CSV results |
| [`experiments/N111/per_family.csv`](experiments/N111/per_family.csv) | CSV results |
| [`experiments/N113/per_arm.csv`](experiments/N113/per_arm.csv) | CSV results |
| [`experiments/N115/per_family.csv`](experiments/N115/per_family.csv) | CSV results |
| [`experiments/N117/ablations_13.csv`](experiments/N117/ablations_13.csv) | CSV results |
| [`experiments/N117/action_audit_baseline_local.csv`](experiments/N117/action_audit_baseline_local.csv) | CSV results |
| [`experiments/N117_effect_prior/ablation_25.csv`](experiments/N117_effect_prior/ablation_25.csv) | CSV results |
| [`experiments/N117_effect_prior/candidate_action_audit.csv`](experiments/N117_effect_prior/candidate_action_audit.csv) | CSV results |
| [`experiments/N117_effect_prior/comparison_25.csv`](experiments/N117_effect_prior/comparison_25.csv) | CSV results |
| [`experiments/N117_effect_prior/prequential_native_actions.csv`](experiments/N117_effect_prior/prequential_native_actions.csv) | CSV results |
| [`experiments/N118/per_family.csv`](experiments/N118/per_family.csv) | CSV results |
| [`experiments/N119/per_family.csv`](experiments/N119/per_family.csv) | CSV results |
| [`experiments/N120/comparison_25.csv`](experiments/N120/comparison_25.csv) | CSV results |
| [`experiments/n117_ablations.csv`](experiments/n117_ablations.csv) | CSV results |
| [`experiments/n118_per_family.csv`](experiments/n118_per_family.csv) | CSV results |
| [`experiments/n119_per_family.csv`](experiments/n119_per_family.csv) | CSV results |
| [`plots/01_level_completions.svg`](plots/01_level_completions.svg) | SVG figure |
| [`plots/02_family_completion_matrix.svg`](plots/02_family_completion_matrix.svg) | SVG figure |
| [`plots/03_action_count_comparison.svg`](plots/03_action_count_comparison.svg) | SVG figure |
| [`plots/04_effect_prior_ablations.svg`](plots/04_effect_prior_ablations.svg) | SVG figure |
| [`plots/05_level3_native_attempts.svg`](plots/05_level3_native_attempts.svg) | SVG figure |
| [`plots/06_predictor_false_negative_risk.svg`](plots/06_predictor_false_negative_risk.svg) | SVG figure |
| [`plots/07_level2_failure_modes.svg`](plots/07_level2_failure_modes.svg) | SVG figure |
| [`plots/public_level_completions.svg`](plots/public_level_completions.svg) | SVG figure |

## Newly restored original JSON research summaries

The following compact JSON files are original offline experiment outputs. Their public release does not recreate the full frame-level evidence; see the original archive checksums in `data/provenance/`.

| File | Contents |
|---|---|
| [`experiments/N114/verified_summary.json`](experiments/N114/verified_summary.json) | Original baseline parity/25-game native verification summary |
| [`experiments/N115/N115_summary.json`](experiments/N115/N115_summary.json) | Original joint-action ablation summary |
| [`experiments/N117_effect_prior/prequential_summary.json`](experiments/N117_effect_prior/prequential_summary.json) | False-negative and calibration diagnostic |
| [`experiments/N117_effect_prior/deployment_gate.json`](experiments/N117_effect_prior/deployment_gate.json) | Original deployment decision |
| [`experiments/N118/prequential/summary.json`](experiments/N118/prequential/summary.json) | History-conditioned prediction controls |
| [`experiments/N119/hazard/summary.json`](experiments/N119/hazard/summary.json) | Family-held-out GAME_OVER hazard audit |
| [`experiments/N119/analysis/summary.json`](experiments/N119/analysis/summary.json) | Delayed-credit / recurrence-risk native results |
| [`experiments/N120/native_summary.json`](experiments/N120/native_summary.json) | N120 episodic-value native ablations |

Interpreting the tables: a shorter game can mean earlier native `GAME_OVER`, not better efficiency. Raw completed-level counts are **not** the human-normalized RHAE metric or the official hidden Kaggle score.

E126's later public comparison matrices and controls are in [`experiments/E126/results/`](../../experiments/E126/results/E127_AUDIT.md), with [paired and robustness CSVs](../../experiments/E126/results/robustness_summary.csv). They are separate from the historical N114/N117 benchmark data above.
