# N105 Macro-Action Bellman Search — Offline ARC-AGI-3 Research

**Result:** implemented and tested, **no new native Level-2 completion** on the eight development families. The previously delivered frozen B1+N093 PUCT `submission.py` and `submission.ipynb` are **not modified or superseded**.

## Files

- `src/n105_options.py`: source Level-1 contiguous-block synthesis, bounded repeated-action controller, option-level semi-Markov Bellman graph, two action-vocabulary variants and backup disable switch.
- `experiments/run_native.py`: on-policy native training-family evaluation using the original N093 checkpoint and original SDK (all steps charged).
- `experiments/analyze.py`, `analyze_ablations.py`, `verify_frozen_parity.py`, `replay_native.py`: read-only analysis and independent native trace audit.
- `tests/test_n105.py`: fast unit tests including a constructive latent-state aliasing counterexample.
- `results/`: original action traces for the primary, no-Bellman and open-vocabulary experiments, immutable after collection.
- `evidence/`: 48/48 exact archived Level-1 parity, 80/80 independent replays (9,838 charged actions).
- `inputs/N100_ACTIVE_FSM_20261025.zip`: original 25-MB frozen research SDK, archival source, checkpoint and prior experiments.

## Prerequisites

Python >= 3.11 with NumPy, SciPy, Torch, and pytest. The original N100 archive includes the offline SDK/runtime. Internet and access to the real Kaggle hidden-test gateway are not required. Do **not** run experiments against held-out families or clone live SDK state.

## Reproduce

From the package root:

```bash
python -m zipfile -e inputs/N100_ACTIVE_FSM_20261025.zip work
python -m pytest -q tests/test_n105.py
python experiments/verify_frozen_parity.py --results results/n105_native_8f_2seed_3arm.json --additional results/n105_native_remaining.json --reference work/N100_ACTIVE_FSM/results/N093_10X3X5.json --out /tmp/n105_level1_parity.json
python experiments/replay_native.py --source work/N100_ACTIVE_FSM --data results/n105_native_8f_2seed_3arm.json results/n105_native_remaining.json results/n105_no_backups_8f_seed76.json results/n105_novel_8f_2seed.json --out /tmp/n105_replay.json
python experiments/analyze.py --first results/n105_native_8f_2seed_3arm.json --second results/n105_native_remaining.json --out /tmp/n105_summary.json
python experiments/analyze_ablations.py
```

To regenerate a **new native experiment** (never overwrite frozen results):

```bash
python experiments/run_native.py --source work/N100_ACTIVE_FSM --output /tmp/n105_native_recheck.json --games ar25 cd82 g50t lp85 ls20 m0r0 sc25 tu93 --seeds 76 77 --arms baseline source_only open --max-level2 200 --max-option 12
```

`run_native.py` refuses `vc33` and all other excluded/untested families. It issues **no explicit RESET**. The SDK creates a new native game for each independent experimental episode. No extra calls are hidden outside the charged action logs.

The sample run's original N093 comparator used 200 total actions, but the N105 matched study uses **200 per level** to compare post-Level-1 search fairly. They are not directly comparable action-count protocols.

## Do not treat this as a Kaggle release

The package contains an executable offline research controller and native SDK evaluation, **not a validated Kaggle `MyAgent` framework integration**. It lacks a cross-level semantic coordinate rebinding mechanism for ACTION6 and has not improved native reward. Do not replace the already verified frozen Kaggle submission with this experimental code.

Refer to `FINDINGS.md` for all controls, limitations, and complete provenance. The formal method is **semi-Markov option-level Bellman search**, not proven RTA\* or a transformation of a POMDP into an MDP.