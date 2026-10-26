# N118 — History-Conditioned Online Action-Effect Prediction (ARC-AGI-3)

**Status: Completed negative policy result; reproducible positive prediction result. Research-only; do not replace frozen N093.**

## Summary

A registered per-game online logistic predictor observes only charged actions and public SDK frames. It estimates `P(next native frame changes >=4 pixels | current frame, candidate action, previous one/two native actions and their observed effects)`. Its estimates alter **selection bonuses** for Level 2 onward; they are never injected into the native Bellman reward and never hard-mask legal actions.

- Frozen N093 reference from N114: **13 L1 / 1 L2 / 0 L3+** across 25 public games (14 total completed levels).
- Existing N117 soft+local baseline: **13 / 2 / 0** (15 total), limited to `vc33` and `tu93` on Level 2.
- New N118 temporal-history agent: **13 / 2 / 0**, **no new Level-2/Level-3 successes**.
- Level-2+ prequential Brier (identical 1,197 charged source decisions): **0.169102** no-history versus **0.151572** history versus **0.162504** corrupted-history. Lower is better.
- False-negative rate for >=4-pixel changes increased: **5.3%** without history to **12.2%** with history (threshold p < 0.5).
- Native 25-family actions: **2706** no-history, **2703** actual-history, **2759** corrupted-history; differing termination times cannot be construed as improved RHAE.
- **75/75** native episodes and **8,168/8,168** charged actions independently replayed; **12/12** matched-seed episodes, **1,019/1,019** actions separately replayed.
- Native seeds 47–50 gave identical initial screenshots for `vc33` and `tu93`. No independent-layout generalization demonstrated.

See `FINDINGS.md` and `results/analysis/comparison_summary.json` for exact per-family outcomes and limitations.

## Files

- `inputs/submission.py`, `inputs/submission.ipynb`: byte-identical immutable frozen N093 source / Kaggle notebook.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: original public SDK runtime and N093 source needed for native replay, never used as an environment oracle by the acting policy.
- `inputs/N114_public25_matrix.csv`: N114 frozen control benchmark, historically exposed public games.
- `inputs/archived_soft_plus_local_25/`: immutable native-action trace records from the prior N117 experiment, used for **diagnostics only**; they are never supplied to the actor.
- `src/reference_policy.py`, `src/effect_prior.py`: exact earlier controller implementations; needed to reproduce N118's no-history control and its inherited native Bellman learning.
- `src/temporal_effect.py`: N118 history-conditioned actor and online learner.
- `run_native.py`, `run_matrix.py`: actual SDK experiments. **200 actions per level**, no uncharged simulator calls.
- `prequential_fixed.py`: same-action real SDK playback for a properly paired predictor comparison.
- `verify_replay.py`: independent action/frame/reward replay, with no acting policy.
- `analyze.py`: exact 25-game and baseline parity, per-family comparison.
- `candidate_submission.py`, `candidate_submission.ipynb`: **unpromoted experimental** standalone N118 implementation.
- `verify_candidate_parity.py`: acting-time parity of embedded Kaggle-format core with modular source.
- `results/native25/`: 75 real native episodes and every charged action.
- `results/prequential/`: 25-family fixed-policy prediction probabilities, Brier, log loss, FNR.
- `results/seed_77/`, `results/seed_78/`: 12 additional native episodes.
- `tests/`, `SHA256SUMS.txt`: correctness and source-integrity controls.

## Reproduce from clean extraction

Requirements: Linux, Python 3.11+, NumPy, SciPy, PyTorch, pytest, plus bundled ARC-AGI-3 public SDK modules. **No Internet or competition account required.**

```bash
cd N118_TEMPORAL_EFFECT_RL_20261026
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python prepare_runtime.py
PYTHONPATH="src:inputs:work/N100_ACTIVE_FSM/sdk_runtime/site:work/N100_ACTIVE_FSM/baseline_source:work/N100_ACTIVE_FSM" python -m pytest -q tests
python analyze.py
python verify_release.py
python verify_candidate_parity.py
```

To repeat the fixed-policy observed-transition prediction audit (all 25 games):

```bash
cd N118_TEMPORAL_EFFECT_RL_20261026
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python prequential_fixed.py --out results/reproduced_prequential
```

To rerun a live experiment (write to new directory):

```bash
cd N118_TEMPORAL_EFFECT_RL_20261026
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python run_matrix.py --arms temporal_nohistory temporal_history temporal_corrupt --workers 3 --timeout 150 --out results/new_live_25
```

To independently replay all archived native experimental actions:

```bash
cd N118_TEMPORAL_EFFECT_RL_20261026
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python verify_replay.py results/native25/*/*.json
```

Rebuild optional **unpromoted** notebook:

```bash
cd N118_TEMPORAL_EFFECT_RL_20261026
python generate_candidate.py
python verify_candidate_parity.py
```

## Privacy, scientific validity and restrictions

All 25 games are historically exposed public development cases. The benchmark lacks human-relative action counts, so **no official RHAE** can be calculated. The tested seeds do not yield independent puzzles. Model probabilities may correlate with visible changes that have no puzzle value. A game can `GAME_OVER` before the 200-action-per-level cap. Only SDK `levels_completed` progression is counted as native reward. The public runtime file archive is never read by the acting policy to infer game-specific rules.

**Deployment:** Frozen N093 remains untouched; switching back requires loading `inputs/submission.ipynb` (SHA-256 `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`). The N118 notebook was not submitted to Kaggle.