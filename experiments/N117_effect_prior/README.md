# ARC-AGI-3: Uncertainty-Aware Action-Effect Prior Audit

**Research experiment, not a promoted Kaggle submission.** Date: 2026-10-26.

The objective was to improve native Level-2/Level-3 performance by learning a
cheap per-action prediction of visually detectable effects, using only legal,
charged native SDK interactions. The control is frozen B1 + N093 pretrained PUCT.

## Final outcome

Across 25 historically exposed public interactive games, the experimental
soft-plus-local model achieved 13 L1 / 2 L2 / 0 L3+ completions, compared with
13 / 1 / 0 for frozen N093, and 13 / 2 / 0 for the *existing* local-effect
candidate. **No new game reached Level 2; no native Level 3 was completed.**

The supported result is a negative result: effect classification helps to
predict observed screen changes but does not identify deep puzzle progress.
The strict hard mask is dangerous because many useful-looking changed-pixel
outcomes would have been labeled negative. See `FINDINGS.md`.

## Contents

- `inputs/submission.py`, `inputs/submission.ipynb`: immutable frozen control.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: public SDK baseline runtime source
  needed to reproduce the native test; game-source files are never accessed by
  the acting core.
- `inputs/N114_public25_native_traces.json`: verified archived baseline action
  ledger, retrospective parity / diagnostics only, never fed to actor.
- `inputs/previous_local_traces/`: original previously verified local-effect
  comparison, retrospective evaluation only.
- `src/effect_prior.py`: per-game online regularized logistic classifier and
  soft / hard / shuffled / persistent / repeated-silence ablations.
- `src/reference_policy.py`: previous local-effect selection logic on frozen N093.
- `run_native.py`, `run_matrix.py`: live public SDK acting runs; per-level cap 200.
- `prequential.py`: independent archived-action playback with pre-action effect
  prediction and per-action updating.
- `candidate_submission.py`, `candidate_submission.ipynb`: optional **unpromoted**
  standalone experimental agent using soft-plus-local, with the exact Kaggle
  interface from the frozen notebook; not executed on Kaggle servers.
- `generate_candidate.py`, `verify_candidate_parity.py`: candidate generation
  and acting-time source parity.
- `seed_runs.py`: matched native/policy-seed sensitivity on two exposed games.
- `verify_replay.py`: independent native replay of saved action requests.
- `analyze.py`: all 25-game comparisons; immutable Level-1 baseline parity.
- `results/full/`: 175 episodes, 19,557 chargeable native actions.
- `results/seed_study/`: 54 episodes, 4,834 chargeable native actions.
- `results/prequential_native_actions.csv`, `prequential_summary.json`:
  classification audit on frozen baseline actions.
- `results/ablation_25.csv`, `results/comparison_25_games.csv`,
  `results/candidate_action_audit.csv`: comparisons and action evidence.
- `RESEARCH_DIRECTIVE.md`, `FINDINGS.md`: objective, evidence and decision.

## Reproduce from a fresh extraction

Requirements: Linux, Python 3.11+, NumPy, SciPy, PyTorch, pytest. The original
SDK files are bundled; no Internet access is needed after dependencies exist.

```sh
cd /path/to/ARC_SOFT_EFFECT_RL_20261026
python prepare_runtime.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=src python -m pytest -q tests
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python analyze.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_candidate_parity.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_release.py
```

A fresh native smoke run, writing to a *new* output directory:

```sh
cd /path/to/ARC_SOFT_EFFECT_RL_20261026
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_native.py \
  --arm soft_plus_local --families vc33 tu93 --out results/new_smoke
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_replay.py \
  results/new_smoke/soft_plus_local/vc33.json \
  results/new_smoke/soft_plus_local/tu93.json
```

A full 25-game fresh comparison (can take time):

```sh
cd /path/to/ARC_SOFT_EFFECT_RL_20261026
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_matrix.py \
  --arms soft_any soft_substantial soft_plus_local soft_persistent \
         hard_substantial repeat_silence soft_shuffled \
  --workers 3 --timeout 90 --out results/new_full
```

Full independent replay of the archived 175 episodes:

```sh
cd /path/to/ARC_SOFT_EFFECT_RL_20261026
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_replay.py \
  results/full/*/*.json
```

Rebuild the self-contained candidate (experimental, **do not promote**) with:

```sh
cd /path/to/ARC_SOFT_EFFECT_RL_20261026
python generate_candidate.py
```

## Restrictions and provenance

The agent's runtime code contains **no game identifiers** and does not access
bundled environment implementation files except through the public SDK. Native
reward advancement is the only Q backup reward. Classifier predictions and
shaping bonuses only change selection scores; no extra native calls are hidden
in inference. Every per-level run is capped at 200 charged actions; the games'
actual `GAME_OVER` events may terminate earlier.

All 25 public ARC-AGI-3 games and the two analyzed Level-3 layouts are already
historically exposed development cases. Varying a seed does not guarantee
varying a puzzle layout. Human-reference action counts are not provided, so
**no official RHAE, hidden-game score, Kaggle commit, or hidden evaluation** is
claimed.

## Deployment

Keep byte-identical frozen N093. The standalone candidate is **research only**;
rollback is simply `inputs/submission.py` / `inputs/submission.ipynb`.