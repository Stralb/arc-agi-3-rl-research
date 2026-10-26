# N115 changes

- Recovered original N098 research result and corrected the claim that it won Level 3.
- Implemented charged, precommitted two-step controller with frozen N093 Level 1.
- Added optional mode for distinct-controls, repeated-control and observation-
  conditioned second-step selection.
- Added semi-Markov pair Q updates with real native rewards, duration discounting
  and explicit illegal-second penalties. Frozen B1 atomic Bellman learning remains.
- Matched the frozen N114 25-game reference and ran all 125 N115 episodes.
- Ran a pair-value-disabled ablation; recorded five changed trajectories, no wins.
- Independently replayed all 14,795 experimental native SDK actions.
- Preserved frozen `submission.py` and `submission.ipynb` unchanged in `inputs/`.
- Released experiment code/data/tests with archive checksums, without deploying N115.