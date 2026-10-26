# N104 change and evidence register

## Changes from N103

- Replaced full-frame next-palette reconstruction objective with sparse categorical delta-mask prediction, positive-weighted BCE, Dice, changed-region colour prediction and a delta-conditional contrastive representation head.
- Split archived 60 native episodes by complete policy-seed trajectories: fit 276/277, calibration 278, held-out source replay 279. No new native SDK actions executed.
- Evaluated a separately trained frame-only model, action-blind recurrent model, and recurrent model without contrastive supervision.
- Added predictive-response signatures and a train-fitted threshold with held-out true/false state fragmentation metrics, rather than assuming vector clustering implies bisimulation.
- Added novel frame/action split, per-family scores, trivial extremes and paired whole-episode bootstrap.

## Detected QA errors / scientific corrections

1. **Model training first-step bug fixed:** Mixed minibatches sometimes encoded absent previous action as actual control `0` on episode starts. Added `first_step_mask` and regression test, reran primary and affected recurrent controls. Superseded pilot/checkpoints in `results/pre_first_step_fix/`.
2. **Inference performance fixed:** Batched aligned episode steps for prediction without changing recurrence or result arrays. The original serial evaluation could exceed tool timeouts. No predictive computation occurs on the native simulator.
3. **Denominator corrected:** N103's 0.15% is model recall, not changed-pixel prevalence. True prevalence: 1.36% of source pixels, 1.29% on the evaluation partition.
4. **Causal claim narrowed:** The aggregate N104 recall gate passes, but a separately trained action-blind control approaches it, history-reset F1 improves, and predicted-key clustering misclassifies many identical-outcome pairs.
5. **Bisimulation claim rejected:** Same immediate predicted deltas are not sufficient for equal future observation/reward dynamics, even with perfect one-step predictions. One-step counterexample and limited action-probe support are explicit.
6. **Holdout qualification:** The test policy seed was previously used in N103 and seen in a 50-step N104 pilot, and native initial layouts repeat; this is a controlled source replay, not a sealed prospective test.

## Release validation

Re-run `python verify_package.py` and `python -m pytest -q tests` on a clean extraction. Archived source frames/checkpoints, numerical metrics, ablation diagnostics, model files and original N103 ZIP are pinned by SHA-256.