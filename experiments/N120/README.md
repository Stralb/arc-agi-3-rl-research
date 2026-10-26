# N120 — Episodic value prediction + TD(lambda), ARC-AGI-3

**Status:** Complete negative research experiment, native Level-3 success **0**. The file names use N120 because N119 was already used for the preceding delayed-credit/risk study. This implements the new user-requested episodic-value directive without overwriting prior archives.

## What is inside

- `inputs/submission.py`, `inputs/submission.ipynb`: exact frozen B1 + N093 baseline; original hashes checked.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: original archived offline SDK fixture and N093 integration source; extracted only to run already legal public environments.
- `inputs/public25_native_traces.json`, `inputs/n118_native25`, `inputs/local25`: previously charged native trajectories used to reconstruct observation-level episodic labels.
- `inputs/archived_local_effect_25`: genuine existing 15-level native control traces for independent parity checks.
- `build_replay_dataset.py`: reconstruct exactly the logged SDK action sequences, verify frames, deduplicate level trajectories, create discounted level-bounded return labels.
- `src/episodic_features.py`, `src/value_model.py`, `train_value.py`: lightweight state/history value network plus action-conditional head, MC and fitted TD(lambda), shuffled-label control, family-disjoint split.
- `src/episodic_policy.py`: conservative Level-3 value prior, direct Q-initialization negative control, state-only null control, optional online reward-only fine-tuning.
- `run_native.py`, `run_matrix.py`, `verify_replay.py`, `analyze.py`: reproducible native acting and independent replay.
- `models/*.pt`: locally fitted, CPU-compatible PyTorch weight-only checkpoints. `heldout_value_audit.json` contains prediction metrics.
- `results/`: fully captured action, observation-hash and native-reward evidence, per-family matrix, independent replay logs, seed checks and training logs.
- `tests/`: nine regression tests; `SHA256SUMS.txt`: full research-file integrity manifest.

## Reproduce on Linux (full commands)

Requires Python 3.11+ with NumPy, SciPy, PyTorch and pytest. Internet and Kaggle credentials are not required. Commands are run **after extracting the release ZIP**:

```bash
cd N120_EPISODIC_VALUE_20261026
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python prepare_runtime.py
python -m pytest -q tests
python analyze.py
python verify_replay.py results/native25/value_mc/*.json
python verify_replay.py results/native_targeted/*/*.json
python verify_replay.py results/seed_77/*/*.json results/seed_78/*/*.json
sha256sum -c SHA256SUMS.txt
```

Regenerate observations and train networks, rather than trusting saved features or weights:

```bash
cd N120_EPISODIC_VALUE_20261026
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python prepare_runtime.py
python build_replay_dataset.py
python train_value.py
python -m pytest -q tests
```

Run fresh native targeted evaluation; never overwrite the archived results:

```bash
cd N120_EPISODIC_VALUE_20261026
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python run_matrix.py --arms local value_mc value_td value_shuffle value_hard value_state_only value_td_online --families vc33 tu93 --workers 3 --timeout 130 --out results/fresh_targeted
python verify_replay.py results/fresh_targeted/*/*.json
```

Run fresh complete 25-game Monte Carlo evaluation:

```bash
cd N120_EPISODIC_VALUE_20261026
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
python run_matrix.py --arms value_mc --workers 4 --timeout 180 --out results/fresh_public25
python verify_replay.py results/fresh_public25/value_mc/*.json
```

## Scientific constraints

The actor sees only legal public SDK actions, current frames, recent actions and their already-observed effects. No future frames, ground-truth goals, game IDs, engine internals, source-derived strategies or counterfactual simulator trajectories are used. Native advancement is the only Bellman reward. Action-value predictions are selection priors, not pseudo native rewards. All SDK actions during native testing are charged. Archived trajectories are only replayed *as previously logged*, with the number of reconstruction SDK steps recorded.

The 25 public games have all been historically exposed. Training and validation exclude the two targeted games, but this does not create new genuinely unseen game families. **No official Kaggle submission was modified.**