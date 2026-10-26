# N119 experimental change log

- Added observation-only recent-state-return empirical outcome model. It can only create a soft selector penalty; never a hard action mask.
- Added short-horizon discounted credit to action descriptors from *real SDK level-completion rewards only*. Bellman rewards and native Q-updates unchanged.
- Added wrong-descriptor attribution placebo and exact original Level-1 parity checks.
- Added 25-family four-arm native SDK evaluation and preserved all charged action requests/frame hashes/rewards.
- Added family-held-out terminal-within-five diagnostic using previous N118 charged transitions, with explicit caution that it is behavior-policy prognosis, not a counterfactual action risk model.
- Added two-extra-policy-seed native controls on `vc33` and `tu93`, standalone Kaggle-format experimental candidate, acting-time source parity checks, 11 regression tests, independent native replays and checksum manifest.
- Frozen B1 + N093 remains unchanged. No production notebook replacement and no Kaggle submission.