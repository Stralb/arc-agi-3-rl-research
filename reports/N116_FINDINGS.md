# N116 — Object-Factorized Checkpointing: Native Evidence Gate

**26 October 2026. Research disposition: failed to license native Level-3 checkpoints. Do not promote to Kaggle.**

## Question

Can a reward-adjacent observable object transformation from Levels 1 and 2 be reused as a *partial-progress* checkpoint on Level 3, thereby allowing the level-3 action selector to restart its local exploration after each verified subgoal?

This experiment evaluates that precise hypothesis **without game-source strategy, shadow/oracle calls, privileged pre-action states, or uncharged native exploration**. `vc33` and `tu93` are the only historically exposed cases that the most recent Level-2-capable local-effect controller reaches at Level 3. They are not independent hidden games. Native seed 47; policy seed 76; 200 action cap per level. The tested control is the experimental local-effect policy (15/25 public-game completions in the earlier study), not a new promotion of it above frozen N093.

## Critical architecture corrections

1. **PUCT selector is not MCTS:** N093 computes Q(s,a)+0.1 P(a|s)/(1+N(s,a)) for the current frame, without maintaining hypothetical search depth. "Root truncation" is therefore not a reduction of an exponential rollout tree. The only tested software analogue is clearing action-visit exploration statistics; the native game state, timer, Q-values and SDK action charges remain intact.
2. **No universal 75-action budget:** `vc33` gives `GAME_OVER` after 75 Level-3 actions in the current policy; `tu93` after 35. This is an observed native termination, not a universal programmable checkpoint threshold. Neither can be reset without a new SDK action (and a reset may destroy progress).
3. **Reward-frame convention matters:** The last frame of the rewarded SDK response is the new level. In the observed native traces, the `frame[-2]` **of that same rewarded response** exposes the last in-level visual state. N116 uses public `frame[-2]` for retrospective/training-only reward transition extraction, never the new-level screenshot as an object transform. Availability should always be checked at runtime.
4. **Native rewards remain native:** No synthetic r=0.5 is passed to Bellman backups. A false progress event would corrupt value learning; even real object changes are not automatically causal evidence of winning.

## Precise retrospective N106 parser diagnostic

For each completed native level, N106 identifies location-independent local-operation signatures (including source colour, shape signature and transformation) on the **winning action's pre-frame → outgoing frame[-2]**. These templates were tested against normal unrewarded same-level action transitions. Unlike global single-operation matching, local matches are explicitly prone to incidental animation and occlusion and are not evidence that a target was completed.

| Game | Reward event | Reward-event templates | Same-game nonreward matches L1 | L2 | L3 |
|:--|:--|--:|--:|--:|--:|
| `vc33` | L1 win | 1 | 2/2 | 0/26 | **0/75** |
| `vc33` | L2 win | 2 | 0/2 | 13/26 | **0/75** |
| `tu93` | L1 win | 1 | 19/21 | 9/21 | **20/35** |
| `tu93` | L2 win | 1 | 19/21 | 9/21 | **20/35** |

The `vc33` Level-1 and Level-2 winning-action templates **do not overlap**. `tu93` does share one local template, but this signature occurs very frequently on unrewarded moves; it is not an identified subgoal. Thus none of the tested Level-3 events can be licensed as a verified, transferable checkpoint from this evidence. This **does not disprove** that other latent subgoals or richer object relations exist.

The original N106 audit also found **0/53 reward steps** representable as a single exact full-screen operation, so the local matches here are deliberately not treated as a stronger ground-truth semantic label.

## Acting-time guarded checkpoint test

`n116_checkpoint.py` collects unique local-operation signatures from actual rewarded terminal **in-level** frames and all nonreward actions. A checkpoint is licensed only if the same signature occurs at two independently rewarded levels, occurs in *no observed nonreward* transitions, and is present on a current native Level-3 transition. This is a deliberately strict feasibility/safety gate; genuine partial progress may occur on nonreward steps and would be abstained from. The gate tests whether this proposal has enough proof to justify using an intrinsic reward, not whether every possible subgoal detector is impossible.

If a checkpoint were licensed, the experimental wrapper would clear *only* `puct_state_actions` visit statistics. It **cannot** reset the SDK game, native failure clock, progression, action budget, or Bellman Q-values. No checkpoint was licensed in either game; zero exploration resets were performed.

| Native run | Levels completed | Charged SDK actions | Level-3 actions | Licensed checkpoints | Policy changes |
|:--|--:|--:|--:|--:|:--|
| `vc33` local-effect control | 2 | 105 | 75 | — | reference |
| `vc33` + guarded checkpoint | 2 | 105 | 75 | 0 | **none** |
| `tu93` local-effect control | 2 | 79 | 35 | — | reference |
| `tu93` + guarded checkpoint | 2 | 79 | 35 | 0 | **none** |

The guarded policy did not deliver a Level-3 completion. This is an observed **abstention**, not a stronger solver. Both Level-3 runs ended in native `GAME_OVER`. All four complete SDK action trajectories have exact action/frame/reward parity with their charged-policy runs, and an additional policy-free SDK replay reproduces **368/368** recorded actions. Eight regression tests pass, including reward-frame attribution, repeated proof, false-positive rejection, and rejection of synthetic native reward.

## Research decision and next test

**Do not make checkpoint-based dense reward part of the frozen Kaggle submission.** Our two accessible Level-3 configurations lack a reward-derived local visual event that is both (i) repeatable across rewarded levels and (ii) absent during normal unrewarded play. A fixed r=0.5 for every local-operation match would incorrectly call 20/35 ordinary `tu93` Level-3 actions successful checkpoints.

The credible next research direction is **survival-constrained, history-conditioned credit assignment**:

1. Derive observationally testable progress evidence from *persistence and changed future controllability*, not a single-frame recolour/translation. Use public consecutive frames, legal-action menus, action-effect outcomes, delayed native level reward and no engine-state labels.
2. Compare a detector's ability to distinguish reward-proximal events from matched nonreward controls **before** letting it modify action choices. Require held-out trajectories/layouts; identical starting frames across seeds do not qualify.
3. If progress is validated, test a bounded **potential-based** shaping signal or conservative candidate ranking rather than an uncalibrated r=0.5 and unconditional visit-count clearing. Abort on increased terminal hazards.
4. Evaluate complete native Level-3 outcomes on both exposed cases, then 25-game regressions and independent configurations. Do not promote a family-specific one-off.

**No Level-3 win is claimed.** Frozen N093 and the optional local-effect candidate remain byte-for-byte unchanged.