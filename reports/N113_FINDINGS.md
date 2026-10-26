# N113 — Targeted model-free baseline amplification on exposed `vc33`

**25 October 2026. Decision: no improvement; do not promote.** This is a real SDK experiment on a previously exposed public development family, *not* an untouched Kaggle test, leaderboard result, or demonstration of generalization. No cluster or shadow oracle used.

## Research question

Can a frozen N093 pretrained-PUCT action selector complete Level 3 by (1) pruning to its five highest-prior candidates, (2) multiplying priors of native-observed Level-2 winning actions by 10, and (3) adding Level-1-derived alignment-distance shaping to its empirical Bellman updates?

The original N093 implementation is *one-step* PUCT-style action selection, **not RTA\*** and not a tree search. Restricting its candidate set to five does not mathematically imply deeper search.

## Experimental design

- Evaluation family `vc33`, native SDK seed 47 and policy seeds 76, 77, 78. The native layout is the same for all seeds.
- Eight factorial arms: baseline, top5, inherit10, shape, top5_inherit10, top5_shape, inherit10_shape, all_three.
- No changes to the Level-1 or Level-2 policy. **All interventions activate only after a genuine native Level-2 reward.** A full-game reset is never requested.
- Per-level 200-action software cap, in addition to any environment-imposed termination; 3 levels maximum in this study.
- Inheritance uses **only actual clicks executed in Level 2 of the same run**, never the N098 diagnostic/oracle sequence. An inherited click may be admitted to the N093 candidate list only if still legal in the native SDK. Initial Q value remains the same B1 optimism Q=1.0, with visit-decayed PUCT prior multiplier 10.
- Shaping uses the uniquely induced N097B alignment relation from Level-1 observations and reward response outgoing `frame[-2]`. The bonus is `0.5*(old_gap - new_gap)/64`, only when the same object pair is unambiguously measurable on both real consecutive Level-3 frames. This is a tested heuristic *separate from actual native reward* and is not theoretically policy-invariant.

## Main native result

| Arm | Native L1 successes | Native L2 successes | Native L3 successes | L3 actions/run | SDK actions (3 seeds) |
|---|---:|---:|---:|---:|---:|
| Frozen pretrained PUCT | 3/3 | 3/3 | **0/3** | 75 | 315 |
| Top-5 prior pruning | 3/3 | 3/3 | 0/3 | 75 | 315 |
| 10x Level-2 prior inheritance | 3/3 | 3/3 | 0/3 | 75 | 315 |
| Alignment-distance shaping | 3/3 | 3/3 | 0/3 | 75 | 315 |
| Top-5 + inheritance | 3/3 | 3/3 | 0/3 | 75 | 315 |
| Top-5 + shaping | 3/3 | 3/3 | 0/3 | 75 | 315 |
| Inheritance + shaping | 3/3 | 3/3 | 0/3 | 75 | 315 |
| **All three** | **3/3** | **3/3** | **0/3** | **75** | **315** |

All 24 trajectories reward at actions **3 and 30**, enter native Level 3, and end in native `GameState.GAME_OVER` at total action **105**. Crucially, the 200-action software cap is **never hit**. These are only **two distinct physical action trajectories** across the entire 24-arm/seed ledger, because all three policy seeds yield identical gameplay for this native starting layout.

## Mechanistic ablations

**Top-5 pruning is active but not beneficial.** It changes 32 of 75 Level-3 actions relative to baseline and reduces distinct clicked coordinates from 13 to 8. At 37/75 decisions it excludes a B1 candidate with strictly higher empirical Q than all retained candidates. Despite the different path, it still ends in game over without Level-3 reward.

**Inheritance required explicit, legal candidate admission.** The simplest prior-only implementation boosted zero candidate matches because the 3 Level-2 action IDs did not appear in Level 3's standard B1 candidate sets. N113's final implementation corrects this by admitting each *previously executed, still native-legal* Level-2 action with original optimistic Q, then applying a 10x multiplier to its *current* PUCT prior. This produces **225 matched boost-candidate occurrences per run** (3 candidates at each of 75 Level-3 decisions), yet yields exactly the baseline action trajectory and no new reward. It is not forced replay.

**The alignment heuristic cannot be grounded on Level 3.** N097B's Level-1 extractor identifies one alignment relation. Its shape/role-matched moving/static pair is not uniquely identifiable at **any** of the 75 actual Level-3 steps. Thus the shaping function abstains 75/75 times and makes zero Bellman adjustments. To add a reward anyway would invent target correspondences that the observations do not support.

**End condition dominates the proposed budget strategy.** All arms reach SDK game over after 75 Level-3 actions; none exhausts the 200-action *policy* cap. The action budget being 200 rather than 75 does not give the controller more legal actions after game over. We cannot conclude from these data whether native game over is a hidden action cap, an engine rule or other terminal condition without privileged evidence; it is simply directly observed.

## Provenance and validation

- 24 executed SDK episodes; 2,520 charged SDK actions; no explicit reset probes.
- Exact Level-1 and Level-2 parity for all 24 paired arms.
- The three N113 baseline episodes match **105/105 actions, pre/post observation hashes, and rewards each** in the original frozen N093 pretrained-PUCT result.
- Independently re-executed the **two physically distinct trajectories (210 SDK actions)**, with exact matching observations, rewards, legal-action masks and terminal states. Every archived row duplicates one of these trajectories.
- 20 regression tests, including first two levels' parity, native-reward checks, probability boost normalization, Top-K tie handling and missing-alignment abstention.
- Original N100 source and frozen Kaggle notebook stored as immutable inputs; N113 did not edit the production submission.

## Research conclusion

The requested Level-3 improvement was **not achieved**. Of the proposed components, only Top-5 pruning actually changes native action sequences, and this change is not beneficial on the target development layout. Using the Level-1 alignment goal or Level-2 exact controls on Level 3 is not grounded by observed geometry or native action selection.

**Keep frozen B1 + N093 pretrained PUCT for submission.** Do not claim independent multi-seed generalization or score improvement from this repeatedly exposed `vc33` case. No Kaggle submission occurred in N113.