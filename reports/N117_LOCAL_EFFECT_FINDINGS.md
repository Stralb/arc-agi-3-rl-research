# Deep-level ARC-AGI-3: adversarial N093 audit and native A/B evaluation

**Date:** 2026-10-26. **Research status:** public exposed-case improvement; **not promoted for hidden-game submission**.

## Scientific outcome

A small, observation-grounded, local-action-effect ranking change produced **one additional native Level-2 completion** on `tu93`. In a paired 25-game public SDK evaluation, the frozen N093 agent completed **13 Level 1, 1 Level 2, 0 Level 3+** (14 completed levels); the experimental local-ranking candidate completed **13 Level 1, 2 Level 2, 0 Level 3+** (15 levels). The two Level-2 winners are `tu93` and the previously known `vc33`. This is **not** a new whole-game WIN, Level-3 completion, official RHAE, Kaggle score, or evidence of unseen-layout generalization.

The full 25-game paired runs used exactly **2,982** charged SDK actions for the baseline and **2,790** for the candidate, but reduced action totals partially reflect **earlier GAME_OVER** (notably `ar25` and `lp85`), so they are not a demonstrated efficiency gain.

A simple *unnormalized level-index count* increases from 15 to 17 by giving 2 to each completed Level 2 and 1 to each completed Level 1. This is **not** an RHAE score; human action reference counts and reliable game-level normalization are not available in this package.

## Phase 1 — exact frozen source audit

Source: immutable frozen `inputs/submission.py` with SHA-256 `e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d`.

- New per-state candidate actions initialize `Q(s,a)=1`. The original `gamma=0.985` backup can decrease a previously attempted, unrewarded action to `0.985` while untried actions remain at `1`.
- Level 2 onward uses a one-step selector `Q(s,a)+0.1 P(a|s)/(1+N(s,a))`. It **is not an MCTS tree**. The pretrained network is fixed; the action prior temperature is 2.0.
- `HypothesisMemory` collects descriptor-level native action effects, merges Level 1 observations into cross-level `past` with `previous_level_weight=.25`, but **`PretrainedPUCTCore.choose()` does not use `HypothesisMemory.rank()`** on Level 2 onward. The original B1 tie-break does consult the memory on Level 1.
- At each level transition, the per-state Q table and PUCT counts are cleared. HypothesisMemory cross-level evidence is retained, but is not used by the Level-2 selector.
- Across **1,487 Level-2+ chosen actions** in the instrumented 25-game frozen run, **976 had Q=1.0**, **510 Q≈0.985**, and **1 Q≈0.970**. These choices alone do not establish that any individual ignored repeat was beneficial. **477** Level-2+ actions resulted in no change to the observed 64×64 frame.
- The action-effect evidence is **not a semantic physics oracle**. In particular, the current `meaningful` label requires `log2(changed_pixels)>=2` (roughly ≥4 changed pixels); a nonzero one- to three-pixel update is recorded but classed nonmeaningful. This threshold is central to the positive result below.

All 25 instrumented baseline trajectories exactly match the original N114 SDK actions, frame hashes and native rewards. The frozen Level-1 trajectory is identical across baseline and experimental candidate in all 25 games.

## Phase 2 — native, charged causal ablations

The experiment changes the **selection score only**; it does not inject intrinsic rewards into B1 Bellman updates and does not pretend to simulate native SDK actions. The selected action must be legal. Every real `env.step` counts. Level 1, trained prior, RL Q backups and 200-action-per-level limit remain frozen.

Modes were fixed before running. The primary candidate augments N093 PUCT using a small, confidence-weighted effect bonus from **the current level's observed action-descriptor evidence**, without blindly carrying pixel-hash Q states across levels. Its effect label inherits the existing N093 ≥4-pixel `meaningful` threshold. The strict transfer-only arm instead uses earlier-level action-descriptor observations. The combined arm adds both signals.

The following table covers the **same thirteen games that completed Level 1 under frozen N093**; all other games cannot be affected by these Level-2-only interventions:

| Arm | L1 completed | L2 completed | L3+ | Key observation |
|---|---:|---:|---:|---|
| Frozen N093 (matched subset) | 13 | 1 | 0 | Only `vc33` |
| Cross-level prior evidence only | 13 | 1 | 0 | Changes decisions, no extra reward |
| Current-level local action-effect ranking | 13 | **2** | 0 | Adds `tu93` |
| Combined transfer + local effect | 13 | **2** | 0 | Adds `tu93` |
| Uncertainty curiosity with repeated-silence penalty | 13 | 1 | 0 | No new win |
| Same curiosity without repetition penalty | 13 | 1 | 0 | Risk ablation has no completion improvement |
| Pixel-effect ranking control | 13 | **2** | 0 | Also adds `tu93`, weaker evidence of a unique mechanism |
| Seeded random novelty control | 13 | 1 | 0 | No additional native reward |
| Event-terminated conditional repeated-action skills | 13 | 1 | 0 | 289 skill actions, no additional completion |
| Any nonzero pixel change counted as meaningful | 13 | 1 | 0 | Removes `tu93` gain |
| Descriptor evidence shuffled among primitive controls | 13 | 1 | 0 | Removes `tu93` gain |

The proposed risk feature is a conservative **recent repeated-silence penalty**, **not** a calibrated `GAME_OVER` probability. No evidence demonstrates it predicts irreversible hazards; calling it a general risk model would be incorrect. The attempted conditional skill activates only after repeated Level-1 effect evidence and requires observed Level-2 effects; it did not add native completion. Neither mechanism should be deployed on these results.

## The `tu93` causal event

Frozen N093 completes Level 1 at action 22 but ends GAME_OVER after 72 total charged actions without clearing Level 2. The experimental local ranking also completes Level 1 at action 22, and **earns native Level-2 reward at action 44**, then reaches Level 3 and ends GAME_OVER after 35 more actions (79 total).

The first causally relevant divergence is native action **26**, on the **same pre-action frame**. The baseline chooses `ACTION4` (encoded action 3), producing a one-pixel change. The local model chooses `ACTION1` (encoded action 0), producing a 19-pixel change. The local score *penalizes the repeatedly small changes* of a previously preferred action; its action selection escapes that trajectory. This is **not** verified discovery of a universal control grammar or completion predicate.

Independent replay matches all 79 experimental SDK actions, pre/post frames and rewarded level counter changes. The shuffled-label and any-nonzero-positive controls both fail the `tu93` Level-2 reward; a simple pixel-effect policy also succeeds, showing that the causal interpretation must remain narrow.

## Seed independence and overfitting

With policy seeds **76, 77, 78, 79, 80, 81** and native seed 47, `tu93` yields **0/6 baseline Level-2 completions**, **6/6 local Level-2 completions**, and **6/6 combined Level-2 completions**. But there are only **two distinct physical trajectories per mode**, not six independent configurations. Native seeds **47, 48, 49, 50** produce the **same initial `tu93` frame hash**; repeating those seeds does not establish different physics or layouts.

The original 15/5/5 public split is preserved as **historical provenance only**; every public game has already been exposed somewhere in this research. The additional win occurs in originally trained `tu93`. No originally validation-family game acquires a Level-2 win. The `vc33` win remains an already-exposed case. Consequently, there is **no untouched family holdout on which to claim transfer**.

## Phase 3 — 25-game regression and deeper-level risks

- Baseline **13/25 L1**, **1/25 L2**, **0/25 L3+**, 14 total levels, 2,982 SDK actions.
- Candidate **13/25 L1**, **2/25 L2**, **0/25 L3+**, 15 total levels, 2,790 SDK actions.
- Candidate reaches previously unreachable `tu93` Level 3 and fails after 35 Level-3 actions. `vc33` continues to reach Level 3 and fail.
- Baseline Level-2 no-visible-change actions: **469 of 1,412**. Candidate: **205 of 1,185**. The populations differ in terminal time and should not be interpreted as a controlled information-efficiency effect.
- Several failures terminate earlier under the candidate (`ar25`, `lp85`); N093 `GAME_OVER` count is 22, candidate count is 23. A gain in one game does not demonstrate a lower overall failure risk.
- No complete-game `WIN`, Level-3+ completion or private Kaggle evidence is claimed.

## Causal and legality controls

- No game ID or game-source strategy is referenced by the acting agent. The runner uses public game IDs solely to schedule and label evaluation episodes.
- No future frames, privileged physics, shadow clones, oracle paths or uncharged probes are supplied to the actor. Rewards in Q updates come solely from SDK `levels_completed` advancement.
- Existing N093 native action menu, legal mask, Q backups, checkpoint, Level-1 behavior and action caps are retained.
- An independent, policy-free SDK replay matched **2,790/2,790** candidate actions and all native reward/frame sequences.
- The final standalone candidate produced **four exactly matching acting-time native episodes** compared with the development core, including `tu93` and `vc33`. See `verify_candidate_parity.py`.

## Deployment decision

**Do not replace the frozen Kaggle notebook yet.** The candidate has a real, new native Level-2 completion on one exposed development family, and it is the strongest local outcome in this branch. But it also ends some attempts sooner, shows no additional reward on historical validation families, and has no independent configuration-level replication. The acceptance gate for generalizable deployment is **not satisfied**.

The optional `candidate_submission.py` and `candidate_submission.ipynb` are supplied for further independent testing, not as the recommended final Kaggle submission. Roll back simply to byte-identical `inputs/submission.py` and `inputs/submission.ipynb`.

The next scientifically justified test is a genuinely distinct, legal, previously unseen environment/layout with the intervention frozen in advance. Further tuning on this `tu93` screen would increase overfitting risk, not credibility.
