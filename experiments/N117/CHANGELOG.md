# Change log

- Audited frozen N093 Q backups, PUCT probability/count score and HypothesisMemory cross-level transitions without mutating the original source/checkpoint.
- Added action-level Q/prior/visits/bonus/effect/outcome diagnostics and verified exact frozen N114 action/frame/reward parity on 25/25 games.
- Implemented cross-level-only, local-effect-only, combined, uncertainty exploration with/without repeated-silence penalty, pixel novelty, random novelty, conditional event skills, all-nonzero threshold, and shuffled-label negative controls.
- Matched native 25-game A/B result: frozen 14 completed levels; local 15, adding `tu93` Level-2 reward. Local Q backups remain native-reward only.
- Replayed all 2,790 local SDK actions independently and verified pre/post observations and native reward events.
- Added policy/native-seed controls; verified repeated seeded `tu93` observations share one starting layout.
- Packaged single-file optional candidate and notebook. Verified acting-time parity on four native games.
- Recorded failures: no third-level win, risk curiosity and conditional skills no extra wins; shuffled and any-visible-effect controls remove `tu93` improvement.
- Kept exact frozen `inputs/submission.py` and `inputs/submission.ipynb` intact. No Kaggle submission performed.