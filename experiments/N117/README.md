> **Public repository edition:** The modular policy, original N117 legal-native runner, replay verifier and archived tests are committed. The `inputs/`, `work/`, original `results/` action/frame histories, notebooks in the original experiment folder and several auxiliary scripts described below are **not** included. The standalone candidate lives at [`src/best_public_agent.py`](../../src/best_public_agent.py). To stage and run the published native portion, use [the authorized setup instructions](../../docs/REPRODUCIBILITY.md). Experiment tests require the original archived ledgers and will not pass on the public subset alone.

# ARC-AGI-3 Deep-Level RL Audit — Frozen N093 vs Effect-Conditioned Action Ranking

**Status:** experimental native improvement (+1 Level-2 completion on exposed `tu93`), **not a hidden-game validated replacement**. All game interactions were charged public SDK actions; no game-source strategy, LLM/VLM, shadow oracle or hidden observations used.

## Contents

- `inputs/submission.py`, `inputs/submission.ipynb`: immutable frozen B1 + N093 baseline (SHA-256 in `results/summary.json`).
- `candidate_submission.py`, `candidate_submission.ipynb`: optional self-contained experimental candidate (not promoted).
- `src/policy.py`: source of all selection and causal ablation variants. No game IDs appear in this acting-time policy.
- `run_native.py`, `orchestrate.py`, `seed_study.py`: legal SDK runners.
- `verify_replay.py`: independent retrospective native replay, not used for model learning or action selection.
- `verify_candidate_parity.py`: acting-time single-file candidate parity.
- `analyze.py`: action-level and family-level report generator; verifies exact N114 frozen parity.
- `results/baseline/*.json` and `results/local/*.json`: 25 complete recorded episodes per arm.
- `results/{transfer,combined,curiosity,curiosity_no_risk,pixel_novelty,random_novelty,skill,local_any_pixel,local_shuffled}/*.json`: 13 native episodes per ablation.
- `results/seed_checks/`: paired `tu93` policy/native-seed controls (distinct-frame warning).
- `results/per_family_25.csv`, `results/ablations_13.csv`, `results/action_audit_baseline_local.csv`, `results/tu93_seed_checks.csv`, `results/summary.json`: analyzed outcome and instrumented actions.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: archived public SDK and frozen source reference (bundled for standalone reproduction).
- `inputs/N114_public25_native_traces.json`: independent frozen N114 reference, **not** accessible to the actor.

## Complete reproduction commands

From the extracted project directory, with Python, NumPy, SciPy, PyTorch and pytest available:

```bash
cd /path/to/ARC_DEEP_RL_AUDIT_20261026
python prepare_runtime.py
OPENBLAS_NUM_THREADS=1 python -m pytest -q tests
OPENBLAS_NUM_THREADS=1 python run_native.py --arm baseline --resume
OPENBLAS_NUM_THREADS=1 python run_native.py --arm local --resume
python analyze.py
OPENBLAS_NUM_THREADS=1 python verify_replay.py results/local/*.json
OPENBLAS_NUM_THREADS=1 python verify_candidate_parity.py
python verify_release.py
```

For a **fresh** evaluation, omit `--resume` and specify a new `--out` directory. To avoid one hanging game blocking others, use per-game process isolation through `orchestrate.py` with explicit `--games` arguments and a chosen per-episode wall-clock timeout. E.g.:

```bash
OPENBLAS_NUM_THREADS=1 python orchestrate.py --arms baseline local --games ar25 cd82 dc22 g50t lf52 lp85 ls20 m0r0 sc25 sp80 tn36 tu93 vc33 wa30 --workers 3 --timeout 65
```

Do not count native-seed reruns of identical starting frames as independent new layouts. The 25 games in this archive have historical training/validation/test provenance, but **all have been exposed by earlier research**.

**Competition artifact:** retain `inputs/submission.ipynb` unless new independent evidence establishes the candidate's generalization. The baseline has not been replaced or submitted by this research.