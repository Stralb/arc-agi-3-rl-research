# Agent sources

- `best_public_agent.py`: **best observed public 25-game result**, 15 completed native levels (13 L1, 2 L2, 0 L3). This is experimental and not shown to generalize to fresh layouts. Identical bytes to the archived `ARC_DEEP_RL_AUDIT_20261026/candidate_submission.py`.
- `baselines/frozen_n093.py`: **deployment-conservative baseline**, 14 completed native levels (13 L1, 1 L2, 0 L3); byte-for-byte frozen.
- `algorithms/local_effect_policy.py`: transparent implementation of the local effect-memory modification. The single-file agents embed their dependencies and pretrained prior, and require the official `arcengine` and ARC-AGI-3 Agents APIs at execution.

**Use the matching notebook under `notebooks/` for Kaggle-style execution.** Neither has a verified private-leaderboard score. No source contains a game-family dispatch table. The N093 score is not human-normalized RHAE.
