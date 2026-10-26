# N109 Deictic Action Grounding

Fully reproducible offline study of Level-1 action replay anchored to visible N106 connected components. The frozen competition notebook stays unchanged. **This is an experimental research archive, not an updated Kaggle submission.**

## Contents

- `src/n109_deictic.py`: pre-action click recording and strict object-relative Level-2 resolution.
- `src/n106_odsl.py`: original N106 connected-component parser (unmodified).
- `experiments/native_ab.py`: frozen B1/PUCT versus absolute replay versus object-relative replay on ten historically exposed N093 families.
- `experiments/replay_saved_native.py`: post-hoc independent native replay and archived N107 frozen parity test.
- `results/native_ten_families.json`: every acting-time action and before/after frame hash, rewards, Level-1 anchored click log, and outcomes.
- `results/per_family.csv`: per-family side-by-side comparison.
- `results/replay_validation.json`: independent native SDK reproduction results.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: exact archived SDK, B1 baseline and pretrained checkpoint (source preserved).
- `inputs/N107_original_frozen_native_reference.json`: earlier frozen baseline action/frame trace.
- `inputs/frozen_submission.ipynb`: exact original Kaggle notebook, **not** modified.
- `tests/test_n109.py`: deterministic tests for relocation and failure modes.
- `FINDINGS.md`, `PROTOCOL.json`, `CHANGELOG.md`, `SHA256SUMS.txt`.

## Reproduction (full commands)

The execution environment needs Python 3.11+, numpy, scipy, torch, pytest and the dependencies already bundled/installed for the archived native SDK. Run from this folder:

```bash
python -m pytest -q tests/test_n109.py
python prepare_source.py
python experiments/native_ab.py --source work/N100_ACTIVE_FSM --out results/native_ten_families_reproduced.json --budget 200
python experiments/replay_saved_native.py --source work/N100_ACTIVE_FSM --results results/native_ten_families.json --out results/replay_validation_reproduced.json --n107 inputs/N107_original_frozen_native_reference.json
python verify_package.py
```

The 200-action cap is per level. The independent replay is a separate **verification experiment**, not free lookahead for the acting agent. There is no game-id-specific policy in either replay arm. Level 2 has a fixed Level-1 sequence and stops instead of falling back to random actions when an anchor is unknown.

## Validity

This is a fixed-layout, single-policy-seed, already-exposed development comparison. In the historical split, `vc33` was a protected test family subsequently exposed by experimentation, so the suite cannot certify unseen-family generalization. There is no Level-3 success or Kaggle score claim.