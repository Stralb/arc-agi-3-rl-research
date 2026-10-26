# N108 — Runtime Action-Grammar Calibration (offline research artifact)

This archive contains a **negative, reproducible, native ARC SDK experiment**, not a new Kaggle submission. It preserves the frozen N093 B1+PUCT notebook byte-for-byte and includes the earlier N100 source archive needed to reproduce the SDK experiments.

**Experiment result:** N108's UI+canvas calibration spent 42 paid clicks, learned no licensed grammar, made zero Level-2 symbolic option calls, and completed the same 9 Level-1 and 1 Level-2 games as the frozen baseline (1,148 vs 1,116 native actions).

## Layout

- `src/n108_grammar.py`: UI role candidates, paid pair observations, contradictory-effect rejection, dynamic cross-level click compilation; the learner documents causality limitations.
- `src/n108_controller.py`: eight-action maximum Level-1 calibration, native fallback and SMDP option integration with real reward accounting.
- `src/n107_smdp.py`, `src/n106_odsl.py`, `src/n106_executor.py`, `src/core_priors.py`: parent model/parser code, retained for provenance and reproducibility.
- `experiments/native_ab.py`: ten-family matched N093 vs N108 native SDK comparison.
- `experiments/passive_pairs.py`: separate 60-episode Level-1 trace control (no SDK calls).
- `experiments/replay_saved_native.py`: independent after-the-fact real SDK replay/verification.
- `results/`: complete saved JSON traces, per-family CSV and independent replay results.
- `inputs/`: unchanged original N100 source ZIP, unchanged frozen competition notebook, original N103 Level-1 frames and manifest.
- `tests/`: 19 deterministic regression tests, including positive synthetic compiler and causal counterexamples.
- `PROTOCOL.json`, `FINDINGS.md`, `CHANGELOG.md`, `SHA256SUMS.txt`.

## Local reproduction

Run from this project directory (Python 3.11+ with `numpy`, `scipy`, `torch`, `pytest`, and dependencies bundled/installed with the original SDK environment):

```bash
python -m pytest -q tests/test_n108.py
python verify_package.py
python prepare_source.py
python experiments/native_ab.py --source work/N100_ACTIVE_FSM --out results/native_ten_families_reproduced.json --budget 200 --cal-calls 8 --min-support 2
python experiments/passive_pairs.py --frames inputs/native_frames.npz --manifest inputs/native_manifest.json --out results/passive_five_families_reproduced.json
python experiments/replay_saved_native.py --source work/N100_ACTIVE_FSM --results results/native_ten_families.json --out results/replay_validation_reproduced.json
```

`prepare_source.py` extracts only the bundled N100 archive; runtime execution uses the **native SDK** interface. No source-game implementation is consulted in the controller. Do not confuse independent verification replay with uncharged acting-time lookahead. All experimental probes are charged native actions.

`inputs/frozen_submission.ipynb` is the exact unchanged baseline for the Kaggle administrative workflow; **do not upload N108 as the competition agent**, since it has no measured Level-2 advantage.