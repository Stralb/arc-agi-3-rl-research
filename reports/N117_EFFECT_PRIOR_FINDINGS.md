# Action-effect learning for deep-level ARC-AGI-3: completed native experiment

**Date:** October 26, 2026. **Status:** complete reproducible negative result,
with retained public Level-2 wins but **no new Level-3 success**. Existing frozen
B1 + N093 is preserved without modification and remains the Kaggle fallback.

## 1. Source and causal hypothesis

Frozen baseline: B1 optimistic empirical Bellman Q (`Q_new = 1.0`,
`gamma = .985`), Level 2+ pretrained N093 one-step PUCT
`Q(s,a) + 0.1 * P_N093(a|s)/(1+N(s,a))`; original Level 1 is left untouched.
The frozen selector is NOT an MCTS tree with simulated rollouts.

N114 measured 13 L1 / 1 L2 (`vc33`) / 0 L3+ across all 25 public games.
A prior research-only local-action-effect ranker measured 13 / 2
(`tu93`,`vc33`) / 0. N116 found that raw object-change patterns did not
license credible Level-3 progress checkpoints.

The new hypothesis is that an online classifier can predict action *effects*
well enough to improve use of the game's scarce native actions, without
predicting the complete next frame or hiding necessary latent-state actions.

The implemented classifier is a regularized online **27-feature logistic
predictor**, not StochasticGoose's CNN. It uses primitive action ID or a
palette-invariant local pixel context (location-normalized border/center role,
clicked-colour frequency and neighborhood contrast). The predictor trains
only on earlier native transitions of the **same** game, including Level 1.
Reward transitions are excluded from visual-effect classifier fitting, since
the outgoing frame belongs to the next level. Q updates still use only native
level advancement; screen-change labels are **never native rewards**.

The soft action ranking adds uncertainty-shrunk score biases while keeping
all N093 legal candidates selectable. The `hard_substantial` negative control
explicitly masks candidates with effect probability below 0.5 after eight
training transitions; an all-masked state falls back to the frozen selector.
Hard prediction masks do not change SDK legality or action limits.

### Models and causal ablations

1. `soft_any`: predict >=1 pixel of change; soft score bonus.
2. `soft_substantial`: predict >=4 changed pixels; soft score bonus.
3. `soft_plus_local`: >=4-pixel model plus the prior successful local-effect
   evidence bonus (existing N093 `HypothesisMemory` descriptor).
4. `soft_persistent`: require at least four changed pixels, at least 70%
   persisting through the following observed action; train one step late.
5. `hard_substantial`: full-candidate hard negative predicted-effect mask.
6. `repeat_silence`: conditional soft penalty for repeated exact-frame/action
   no-effect events alongside local-effect memory.
7. `soft_shuffled`: deliberately mismatched action-feature input as a control.

**No extra SDK actions for model training. No oracle labels. No per-game
hyperparameter choices or game-ID branch. No source-game policy.**

## 2. Full 25-game native results

All new runs were carried out through the public native SDK, native seed 47,
policy seed 76, with **200 charged actions per level**. Level 1 is byte-identical
to frozen N093 in all 175 episodes. The preexisting local-result column comes
from the previous fully archived native experiment, not a new acting run.

| Controller | L1 | L2 | L3+ | Completed levels | Charged SDK actions |
|---|---:|---:|---:|---:|---:|
| Frozen B1 + N093 | 13 | 1 | 0 | 14 | 2,982 |
| Previous local-effect agent | 13 | 2 | 0 | 15 | 2,790 |
| Soft any visible effect | 13 | 1 | 0 | 14 | 2,728 |
| Soft substantial effect | 13 | 2 | 0 | 15 | 2,743 |
| Soft effect + local memory | 13 | 2 | 0 | 15 | 2,706 |
| Persistent effect predictor | 13 | 1 | 0 | 14 | 2,856 |
| Hard substantial-effect filter | 13 | 2 | 0 | 15 | 2,778 |
| Repeated-silence penalty | 13 | 2 | 0 | 15 | 2,783 |
| Shuffled-feature negative control | 13 | 0 | 0 | 13 | 2,963 |

The only new Level-2 family relative to frozen N093 is `tu93`, **already won by
the preceding local-effect experiment**. None of the tested predictors yields
an additional Level-2 family relative to that existing experiment, and none
wins Level 3. Level-1 performance is identical by construction.

Lower total SDK actions are NOT a demonstrated RHAE improvement: many episodes
end in native `GAME_OVER` sooner. For example, `soft_plus_local` completes
`tu93` Level 2 at global action **45** (23 L2 actions), while the previous
local-effect candidate completes it at global action **44** (22 L2 actions).
After the reward, `soft_plus_local` dies in **27** Level-3 actions compared
with **35** for the previous candidate; both have zero L3 rewards.
`vc33` still ends after 75 L3 actions. The 75-action observation is not a
universal environment rule and cannot be reset by model inference.

## 3. Prequential effect-prediction audit on frozen native SDK replay

This was a separate retrospective replay of the N114 *actual* actions, not
acting-time training on future outcomes. Each prediction preceded the outcome
and its training update, using only the game's earlier observed actions.
Reward and terminal transitions are excluded from frame-effect fitting and
from the reported binary classification denominators.

| Prediction target / split | Transitions | Real positives | False-negative rate | Brier |
|---|---:|---:|---:|---:|
| Any change, L1 | 1,471 | 1,359 | 0.66% | 0.07815 |
| Any change, L2+ | 1,475 | 1,000 | 8.20% | 0.12908 |
| Any change, L3+ | 74 | 66 | 0.00% | 0.09994 |
| >=4 pixels, L1 | 1,471 | 1,145 | 3.14% | 0.12640 |
| >=4 pixels, L2+ | 1,475 | 542 | 20.85% | 0.14479 |
| >=4 pixels, L3+ | 74 | 30 | **46.67%** | 0.21621 |

The substantial-effect model predicted a negative outcome for **14/30 actual
substantial Level-3 transitions** with the threshold 0.5. These are observed
actions, not outcomes of untested counterfactual candidates. This demonstrates
an unacceptably high risk of pruning potentially useful actions. Conversely,
the any-change predictor predicted all 74 nonterminal Level-3 actions as
positive at this threshold even though 8 produced no visible change; it does
not usefully prune the Level-3 branch.

Predicting the next observable change is markedly easier than full-frame
transition prediction, **but binary classifier accuracy is not progress
prediction**. A visual no-change action can still modify hidden controls.

## 4. Matched-seed sensitivity

54 additional native episodes: the same two exposed games (`vc33` and `tu93`),
three agents (frozen N093, original local effect, experimental soft+local),
nine policy/native seed pairs per agent-game. Every tested native seed in
47–50 gave the **same initial screenshot hash** for each game.

For `tu93`: N093 failed L2 in all nine; local and soft+local each won L2 in
all nine. There were only **two distinct native action trajectories per
agent**, and only **one distinct starting screenshot**. For `vc33`: all three
agents won L2 in all nine and failed L3; each agent produced **one physical
action trajectory** despite repeated seeds. No independent layouts were
produced. Therefore, these experiments **cannot establish generalization**.

## 5. Code and native-integrity checks

- 175/175 experimental acting episodes, **19,557/19,557 charged native SDK
  actions** independently replayed with exact frame hashes, reward events and
  final states.
- 54/54 seed-study episodes, **4,834/4,834 actions** replayed exactly.
- **229/229 total episodes, 24,391/24,391 native actions** independently replayed.
- **175/175 frozen Level-1 physical traces** exactly match the archived N114
  immutable N093 controller, across 25 families and seven interventions.
- The experimental single-file `.py` and `.ipynb` were generated without
  modifying the frozen originals. Acting-time candidate vs modular implementation
  was exactly matched on **four separate native episodes** (`vc33`, `tu93`,
  `ar25`, `lp85`).
- 9 automated tests passed, including palette relabeling invariance, hard
  feature bounds and predictor prequential update ordering.
- Fixed frozen Python SHA-256:
  `e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d`.
- Fixed frozen notebook SHA-256:
  `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`.

All native test environments are already historically exposed in this research.
The internal SDK implementations are bundled strictly for legitimate replay;
the acting code accesses only the public observation/action interface. No
human reference action counts or genuine private Kaggle scores are available.

## 6. Deployment verdict

**Do not promote. Retain frozen B1 + N093 PUCT.** The best new soft variant
matches the preexisting local-effect two-Level-2 public count but is less
robust during the `tu93` Level-3 attempt. Hard effect masking excludes many
candidates with no new reward and is vulnerable to false-negative effects.

No claim is made of Kaggle hidden-game improvement, a whole-game WIN, an
official RHAE score, or a newly recovered Level-3 completion. The experimental
notebook is provided as an auditable artifact and reversible test branch,
**not** as the recommended final competition notebook.

### Direction of future research (not executed here)

The next scientifically meaningful question is whether reliable *task progress*
and the mechanisms leading to native `GAME_OVER` can be learned from history
without access to hidden physics, rather than predicting whether *any image
pixel* will change. Before adding bonuses, require independent progress labels
or a truly new layout and demonstrate a native Level-3 or cross-family win.
