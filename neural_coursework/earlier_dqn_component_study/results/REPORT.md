# E012 Final DQN Consolidation

## Question

Does the final evidence-backed DQN stack retain its advantage when D14 exploration and Dueling value architecture are removed one at a time?

## Frozen stack entering E012

- E004 representation: `E-onehotcnn__T-stack2__A-vector__U-effect`.
- E008 backbone: Dueling Double-DQN family, one-step uniform replay, no C51.
- E009 exploration: full D14 structured policy only on the epsilon-exploration branch.
- E010 mechanics adapter excluded: improved mechanics prediction but no behavioral uplift.
- E011 mechanics persistence excluded: tied the E009 behavioral control on fresh holdout seeds.

## Three-seed matched ablation

| rank | system | p250 | p600 | completion-cap | reward | first progress | D14/epsilon |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `E12_F_full_dueling_d14` | 0.147 | 0.160 | 0.0107 | 0.160 | 97.1 | 1.000 |
| 2 | `E12_A_no_dueling` | 0.120 | 0.120 | 0.0080 | 0.120 | 54.7 | 1.000 |
| 3 | `E12_A_plain_ddqn` | 0.027 | 0.053 | 0.0036 | 0.053 | 203.5 | 0.000 |
| 4 | `E12_A_no_d14` | 0.027 | 0.040 | 0.0027 | 0.040 | 137.7 | 0.000 |

## Full-stack ablation effects

- **FULL - no-D14**: p600 +0.1200 [-0.0267, +0.2800]; completion-cap +0.0080 [-0.0009, +0.0187].
- **FULL - no-Dueling**: p600 +0.0400 [+0.0000, +0.1067]; completion-cap +0.0027 [+0.0000, +0.0071].
- **FULL - plain-DDQN anchor**: p600 +0.1067 [-0.0400, +0.2667]; completion-cap +0.0071 [-0.0027, +0.0169].

## Decision

`E012_FULL_STACK_CONFIRMED`

Selected/frozen DQN: `E12_F_full_dueling_d14`

## Interpretation

- E012 is a consolidation/ablation, not another broad architecture search.
- Exact behavioral ties retain the full stack because D14 and Dueling already entered with prior experimental evidence.
- If an ablation is behaviorally better, E012 flags component review instead of automatically claiming a new architecture.
- This is the DQN baseline to freeze before building the official-style local evaluator and advanced specialist architectures.
- Public games are development-exposed and sparse p600 is not the official Kaggle score.
