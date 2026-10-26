# N104 — Action-Conditional Delta Coding & Predictive-State Audit

This is an **offline research artifact**. It uses the native public Level-1 observation/action traces in the N103 source package, not a cluster, a privileged ARC simulator, or an unknown test family. The raw source archive is included in `inputs/` to trace provenance. **It is not a deployed ARC Level-2 controller.**

**Decision:** The corrected 47,613-parameter delta-GRU passes **aggregate** changed-pixel recall >80% on the N103 policy-seed-held-out test (81.01% recall, 21.96% precision), but does **not** pass an independently novel frame/action gate (76.66% recall) or a stable predictive-equivalence state-key gate. Do not claim learned causal engine state or bisimulation.

Read `FINDINGS.md` before interpreting the metrics.

## Files

- `src/n104_delta.py`: recurrent action-conditioned observation coding, categorical changed-pixel supervision, latent contrastive objective, and model-only action-response predictions.
- `experiments/train_delta.py`: frozen-source fit/calibrate/evaluate procedure; episode-start masking and complete-episode splits.
- `experiments/eval_checkpoint.py`: recompute the calibration-selected operating point and paired test ablations from frozen weights.
- `experiments/diagnose_delta.py`: metrics by ARC development family and previously unseen `(frame, action)` keys.
- `experiments/bisimulation_audit.py`: restricted multi-action predicted-effect signatures and train-fit/held-out pair-distance clustering audit. **Not a bisimulation algorithm or deployed native key.**
- `experiments/paired_bootstrap.py`: descriptive uncertainty from whole-episode paired resampling.
- `experiments/plot_results.py`: rebuild figures, from frozen checkpoints only.
- `inputs/native_frames.npz`, `inputs/native_manifest.json`: exact frozen public trace data from N103, SHA-256 pinned.
- `inputs/N103_PREDICTIVE_BELIEF_RESEARCH_20261025.zip`: upstream primary source archive; contains its own provenance and replay paths.
- `results/delta_*.pt` and `.json`: frozen corrected PyTorch checkpoints and metrics for four matched models.
- `results/per_family_novelty.json`, `bisimulation_audit.json`, `paired_episode_bootstrap.json`: principal failure checks.
- `results/pre_first_step_fix/`: **superseded** preliminary models and pilot results, retained for change history, not for primary claims.
- `tests/test_n104.py`: source, causal encoder, loss, calibration, counterexample and checkpoint regression checks.
- `PROTOCOL.json`: exact constraints and caveats; protocol was recorded retrospectively after source inspection, not a sealed preregistration.
- `SHA256SUMS.txt`: file hashes for the release.

## Python dependencies

Python 3.11+ with CPU PyTorch, NumPy, SciPy, Matplotlib and Pytest. Tested locally with torch 2.10.0+cpu, numpy 2.3.5, scipy 1.17.0, pytest 9.0.2; original dataset was collected with the bundled N103 ARC SDK, but no SDK is required to retrain N104 from the frozen trace arrays.

## Verify frozen release BEFORE retraining

```bash
python verify_package.py
python -m pytest -q tests
python experiments/eval_checkpoint.py --suffix n104_recurrent
python experiments/diagnose_delta.py
python experiments/bisimulation_audit.py
python experiments/paired_bootstrap.py
python experiments/plot_results.py
```

The scripts that compute diagnostics overwrite only derived JSON/PNG files, which can invalidate the frozen checksum register if the library version changes. For strict frozen validation, run `verify_package.py` **first**.

## Reproduce training from source data

**Work in a COPY of the extracted directory** so the archived checkpoints and checksums remain unchanged. Train/checkpoint commands are deliberately explicit.

```bash
python experiments/train_delta.py --steps 250 --mode recurrent --contrastive 0.06 --train-only --suffix n104_recurrent
python experiments/eval_checkpoint.py --suffix n104_recurrent
python experiments/train_delta.py --steps 250 --mode frame_only --contrastive 0.06 --train-only --suffix frame_only
python experiments/eval_checkpoint.py --suffix frame_only
python experiments/train_delta.py --steps 250 --mode recurrent --contrastive 0 --train-only --suffix no_contrast
python experiments/eval_checkpoint.py --suffix no_contrast
python experiments/train_delta.py --steps 250 --mode recurrent --contrastive 0.06 --action-blind --train-only --suffix action_blind
python experiments/eval_checkpoint.py --suffix action_blind
python experiments/diagnose_delta.py
python experiments/bisimulation_audit.py
python experiments/paired_bootstrap.py
python -m pytest -q tests
```

The model uses actual **past** frame/action sequences and one actually executed **current** action. Future frames are present **only in the training loss**. Offline model-only counterfactual probe passes in `bisimulation_audit.py` execute **no native actions**. Fit-observed candidate actions are not guaranteed to be currently legal in a given state: consequently this is not an acting policy.

## Interpreting the 80% threshold

The first 50-step development pilot inspected the previously used N103 test seed, so the final policy-seed split is **not a sealed independent test**. The final fit uses 30 episodes (869 transitions), calibration 15 (530), and test 15 (449), with repeated native starting layouts. Approximately 34.97% of test `(frame,action)` pairs exactly appear in fit. The >80% result passes the **aggregate source-replay metric**, not genuine new-layout or broad-puzzle generalization. Both a copy-frame predictor (0 recall) and an all-change predictor (100% recall, ~1.29% precision) are weak reference extremes. Report recall together with precision, F1 and changed-area fraction.