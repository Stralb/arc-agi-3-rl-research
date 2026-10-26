# N112 — Action-conditioned forward-model MCTS (offline research)

**Status:** Completed known-family retrospective. Does not outperform frozen B1 + N093 pretrained PUCT. **Do not submit as a replacement.**

## Source and provenance

- Original, unmodified `N100_ACTIVE_FSM_20261025.zip` contains the N093 pretrained agent, B1, frozen weights, local native ARC-AGI-3 SDK and game environment.
- Original `submission.ipynb` included *unchanged* as a Kaggle baseline reference. N112 is not in the notebook.
- Original N103 frames: 1,848 Level-1 native transitions / 60 episodes; N103 policy-seed 279 is held out by whole episode.
- N107's ten-family frozen B1/PUCT native-result JSON is used for **paired baseline comparison**, never for fitting the forward model or directing actions.
- The ten native families are **historically exposed known-development families**. `vc33` is not an untouched holdout.

## Contents

- `src/n112_forward.py`: action-conditioned empirical transition model; causal data only, unobserved actions abstain; contradicting visual states flagged.
- `src/n112_planner.py`: depth-three, bounded PUCT/MCTS using *only model predictions*; terminal-effect histogram is candidate reward proxy, not oracle.
- `experiments/eval_heldout.py`: N103 whole-episode split, known/novel pair controls and in-support wrong-action comparison.
- `experiments/native_mcts.py`: original frozen B1/PUCT from the source archive, Level-1 in-episode model fitting, zero-SDK-action tree search, prediction gate, real native comparison.
- `experiments/replay_native.py`: independent replay of every native SDK action, with hash and level assertions. Does not run an acting policy.
- `tests/test_n112.py`: fixed deterministic tests, including toy planner positive, visually aliased conflicting-successor abstention.

## Reproduction (from fresh extraction)

```bash
cd N112_MBRL_FORWARD_MCTS_20261025
python bootstrap_inputs.py
PYTHONPATH=src python -m pytest -q tests/test_n112.py
python experiments/eval_heldout.py --dataset inputs/n103_native_frames.npz --manifest inputs/n103_manifest.json --out results/reproduced_heldout.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/native_mcts.py --source work/N100_ACTIVE_FSM --baseline-json inputs/n107_frozen_ten_family_reference.json --out results/reproduced_native.json --simulations 192 --max-plans 4
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/replay_native.py --source work/N100_ACTIVE_FSM --native results/reproduced_native.json --out results/reproduced_replay.json
python verify_release.py
```

One rerun of the ten-family native evaluation makes **1,116 charged SDK actions**. Independent replay also calls the SDK and is a verification step, **never an input to N112's planning policy**.

### Why not a CNN?

The implementation deliberately uses an *empirical action-conditioned forward model* instead of the suggested CNN/XGBoost variant. Most individual Level-1 training episodes provide only 2–25 nonreward clicks, and the earlier N104 CNN/GRU result was not reliable on novel game dynamics. A memory model allows direct, auditable confidence and action-support rejection. It is a minimal MBRL baseline, **not** evidence of a learned universal visual-physics model.

### Native action accounting

A native action is charged whenever `env.step` is called, including all training clicks and attempted Level-2 actions. MCTS tree traversal and `model.predict` never call `env.step`, but proposed plans are not free of model bias or compute cost. Only SDK level progression is counted as a win.

See `FINDINGS.md` for measured outcomes, comparison and limitations. No Kaggle submission was attempted.