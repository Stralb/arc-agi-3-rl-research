# N113 — Level-3 prior pruning, inheritance and alignment shaping

This is a reproducible *development-only* ARC-AGI-3 experiment. No oracle actions, game-ID-specific policy, code-reading of puzzle mechanics, shadow simulator, or Kaggle hidden test involved. Every real transition is made through the bundled public native SDK. The policy runs unchanged through Levels 1 and 2.

## Package contents

- `src/n113.py`: complete experimental action-selector amendments to frozen N093.
- `experiments_run.py`: native evaluation runner, eight-arm factorial experiment.
- `replay_native.py`: independent recorded-action SDK replay; no policy instance.
- `tests/test_n113.py`: 20 fast regression tests.
- `results/native_vc33_3x8.json`: 24 full native trajectories including SDK frame hashes and reward events.
- `results/per_arm.csv`, `results/summary.json`, `results/independent_replay.json`: experiment results and provenance.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: original frozen SDK, B1/N093 source and checkpoint, without edits.
- `inputs/original_N093_vc33.json`: original N093 control trace for independent parity checks.
- `inputs/frozen_submission.ipynb`: *unchanged* previously prepared Kaggle notebook, **not** an N113 deployment candidate.

## Reproduction

Start in the unpacked `N113_BASELINE_AMPLIFICATION_20261025` directory with Python 3.13, numpy, torch, scipy, pytest and the SDK's bundled installed dependencies.

```bash
unzip -q inputs/N100_ACTIVE_FSM_20261025.zip -d runtime
python -m pytest -q tests/test_n113.py
python replay_native.py --source runtime/N100_ACTIVE_FSM --results results/native_vc33_3x8.json --out results/replay_verify_again.json
python experiments_run.py --source runtime/N100_ACTIVE_FSM --out results/reproduced_3x8.json --seeds 76 77 78 --arms baseline top5 inherit10 shape top5_inherit10 top5_shape inherit10_shape all_three
python make_report.py
python verify_release.py
```

The paired runs take about 30 seconds on the preparation machine, though actual time depends on CPU. `elapsed_sec` is not stable; compare actions, observation hashes, reward milestones and terminal states. Check `FINDINGS.md` for negative results and relevant limitations.