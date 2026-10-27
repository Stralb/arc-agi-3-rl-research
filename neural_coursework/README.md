# ARC-AGI-3 neural coursework source

This directory preserves the original Wits cluster source files for **Random,
Double DQN and PPO** baseline learners, plus the separately selected **structured
DQN V1** implementation. The code is preserved as researched; missing later
evaluation artifacts are not regenerated.

## Source layout

- `src/adapter.py`, `bridge.py`, `learner.py`, `run.py`: native ARC
  action/observation translation, random reference, runner and checkpoints.
- `src/dqn.py`: online/target Double DQN with masked legal-action selection,
  replay, gradient updates and target synchronization.
- `src/ppo.py`: factorized actor/critic PPO, stored old log-probabilities,
  legal-action masks, GAE and clipped policy updates.
- `src/dqn_v1/`: original selected DQN value learner, dueling network,
  structured exploration, frozen effect representation and cross-fold weights.
- `assets/dqn_v1/checkpoints/`: five existing **historical** 2026 public
  cross-fold effect-model checkpoints copied byte-for-byte from the Wits
  research directory. SHA-256 hashes are available in the export manifest.
- `tests/`: original Wits learner, adapter, lifecycle, DQN V1 and runner tests.

## Reproduction notes

The baseline hyperparameters in `src/config.py` are explicitly marked
**provisional** in the source and are not evidence that every published
experiment used those exact settings. The selected DQN V1 loads a frozen
cross-fold effect prior; its performance and pretraining costs must not be
attributed solely to online DQN. It is a distinct development protocol from
the later four-game coursework outcome table.

The existing `kaggle/learner_agent.py` is a research integration scaffold,
not proof of a fully evaluated Kaggle neural submission. Exact historical
DQN/PPO I1/I2 coursework source, rollout histories and scorer receipts are
not established by this directory alone. Do not describe the files as a
verified reproduction of the later seven-arm study.

For a basic import smoke test, install `requirements.txt` dependencies,
then from this directory run:

```sh
python3 -m pytest -q tests/test_adapter.py tests/test_learners.py tests/test_dqn_v1.py
```

The source files were copied from
`/home-mscluster/astrauss/RL-ARC-AGI-3-Project` on 2026-10-27; existing
repository files were not overwritten during this sync.
