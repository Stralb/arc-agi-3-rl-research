# E012 experiment definition

Question: does the final evidence-backed DQN stack retain its advantage under direct removal of D14 and Dueling?

Evaluation:
- 25 public ARC-AGI-3 games.
- 5 fixed folds of 5 games.
- 3 new seeds: 5209, 5623, 6043.
- 600 command budget per game-run.
- 4 systems x 5 folds x 3 seeds = 60 tasks.
- Each task contains 5 games, giving 300 game-runs total.

Primary ordering: p600, completion-cap, p250, reward, then first-progress speed/safety.

Matched comparisons:
- FULL minus no-D14.
- FULL minus no-Dueling.
- FULL minus plain-DDQN anchor.

Public games are development-exposed. This experiment does not claim hidden-game generalization and does not implement the official Kaggle efficiency score.
