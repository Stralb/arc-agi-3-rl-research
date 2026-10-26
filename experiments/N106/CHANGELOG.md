# Changes relative to frozen Kaggle submission

- Original `submission.py` and `submission.ipynb` copied byte-for-byte into inputs; no changes to their checkpoint or action algorithm.
- Reused original N106 connected-component parser in `src/n106_odsl.py`.
- Added 15 hand-authored scene predicate metrics with unknown/inapplicable semantics and observed merge special case.
- Added action-effect evidence gate: two independent paid observations of progress under same coarse context, with no negative effect, Q-near-tie guard, legal action filter, and exact-frame ACTION6 binding.
- Added separately quarantined speculative object/goal probing arm with 24-action maximum.
- Added tests for goal vacuity, holes, symmetry, connectivity, legal clicks, the core reward firewall, and exploration boundaries.
- Added paired local SDK controls and archived full action/frame traces. The results do not support promotion.
- Kept no-LLM/VLM, no shadow-oracle, no full-game RESET probes, and original 200-action level budget.