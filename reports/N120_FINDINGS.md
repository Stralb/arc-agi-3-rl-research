# N120: Episodic Return Prediction and TD(lambda) for ARC-AGI-3

**Date:** 26 October 2026. **Status:** Completed, verified negative experiment. **Deployment:** Do not promote.

This implements the user's proposed episodic-value directive, numbered **N120** because the existing archive already calls the prior delayed-credit/risk experiment **N119**. Both original frozen B1 + N093 files were preserved byte-for-byte.

## Main research finding

A value network cannot learn Level-3 winning behavior from these particular historical trajectories: **zero Level-3 wins appear in the source evidence**. When the only two Level-2-winning families (`vc33`, `tu93`) are genuinely held out, the training set also has **zero Level-2 wins**. This is a support/coverage failure, not a claim that episodic RL or TD(lambda) in general cannot work.

N093 is a **one-step PUCT-style action ranker**, *not* a simulated MCTS tree. A state-only `V(s,h)` is identical across candidate actions at the same state, so there is no action-specific leaf ranking without a transition model. N120 therefore trains both (1) the requested state/history value `V(s,h)` for diagnostics and (2) an action-conditioned observational return estimator `Q(s,h,a)` for acting, with a strict state-only null ablation. `Q` should not be misinterpreted as a causal estimate of the return under arbitrary untried actions: it is fitted from logged behavior-policy decisions.

## Source evidence and reconstruction

- 25 frozen N093 public episodes from N114; 75 N118 history/no-history/corrupted-history episodes; 25 archived local+effect episodes; **125 previously logged episodes**.
- Each of their **13,856 action requests** was separately replayed through the public SDK *without alternative actions*, verifying pre-action and post-action frame SHA and native advancement. These are charged replays of prior action sequences, not oracle training transitions or extra policy exploration.
- Deduplicated **75 distinct level trajectories / 6,312 distinct level-action transitions**; 124 duplicate level trajectories removed. Across distinct levels, **13 rewarded Level-1 trajectories, 3 rewarded Level-2 trajectories, and 0 rewarded Level-3 trajectories**. The 3 Level-2 trajectory wins represent only two game families.
- Within each level, an observed native reward at the last charged action gives label `gamma^(T-1-t)` for logged preceding transitions, using frozen `gamma=0.985`. No native advancement in a level segment yields observed return 0 for the tested policy and horizon. Capped cases are **censored**, not intrinsically unsolvable.
- The TD(lambda) model uses **fitted on-policy SARSA lambda-returns** from each logged level, with `lambda=0.80`: `G_t = r_t + gamma ((1-lambda) Q_target(s_{t+1},h_{t+1},a_{t+1}) + lambda G_{t+1})`. This never bootstraps between game levels. Frozen target predictions are recomputed after each fitting epoch. Monte Carlo is the lambda=1 limit. A shuffled-label control breaks the return-to-observation association during training.
- Features use public 64x64 frames, color-role occupancy, coarse edges, candidate-action context, two preceding observed action/effect categories, and normalized elapsed actions. No game name or environment source-derived action semantics enters the model.

### Strict family split

| Split | Families | Distinct transitions |
| --- | --- | ---: |
| Training | 20 public families, excluding the five below | 4,863 |
| Validation | `g50t`, `lp85`, `sc25` | 932 |
| Held-out native target games | `vc33`, `tu93` | 517 |

**Training rewards by level:** Level 1 has **8 rewarded trajectories across 1,430 transitions**; Level 2 has **0 rewarded transitions across 3,433 samples**; no Level-3 samples. `vc33` and `tu93` have never entered the offline training or validation split. Other families are historically exposed, so this is a family-disjoint diagnostic within the public set, not independent hidden-test validation.

## Value prediction audit on the held-out target families

| Estimator | Held-out continuous-return Brier error | Mean predicted return | Mean observed return |
| --- | ---: | ---: | ---: |
| Training stage-frequency-only reference | 0.129673 | 0.00477 | 0.15974 |
| Monte Carlo action-value | **0.129670** | 0.02422 | 0.15974 |
| Fitted TD(0.80) action-value | 0.130250 | 0.02144 | 0.15974 |
| Shuffled-training-label control | 0.130877 | 0.02368 | 0.15974 |

The tiny numeric Brier difference between the Monte Carlo model and the simple reference is **not convincing evidence of transferable utility**. In held-out Level 2, TD(lambda) predicts an average value of approximately **0.0225** while the mean observed discounted return is approximately **0.498**. The network is drastically underconfident on the available winning trajectories; Level-3 return is structurally unidentifiable from a corpus with no Level-3 wins.

## Native 25-game benchmark

Only the conservative **Monte Carlo action-conditioned value prior** was run across all 25 public games. N093 Level 1 and local-effect Level 2 were untouched; the new value prior activates exclusively on Level 3. It does not simulate new frames, and each real chosen action is SDK-charged.

| Acting policy | L1 wins | L2 wins | L3+ wins | Total completed levels | SDK actions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Frozen B1 + N093 reference | 13 | 1 | 0 | 14 | 2,982 |
| Existing local-effect candidate | 13 | 2 | 0 | 15 | 2,790 |
| N120 Monte Carlo value prior | **13** | **2** | **0** | **15** | **2,787** |

**All 25 Level-1/Level-2 action, observation hash and native reward sequences match the archived local-effect reference**. The 3-action aggregate reduction is due to earlier `tu93` Level-3 termination, not better solution efficiency. `vc33` and `tu93` remain the sole Level-2 finishers. There is no official Kaggle private score or RHAE claim.

### Targeted Level-3 ablations (policy seed 76)

| Policy activated at L3 | `vc33` L3 SDK actions | `tu93` L3 SDK actions | Additional L3 wins |
| --- | ---: | ---: | ---: |
| Local-effect reference | 75 | 35 | 0 |
| Monte Carlo Q, bounded centered prior | 75 | 32 | 0 |
| TD(lambda) Q, bounded centered prior | 75 | 32 | 0 |
| TD(lambda) Q + winning-level online updates | 75 | 32 | 0 |
| Direct replacement of optimistic Q (negative control) | 75 | 35 | 0 |
| Shuffled-return-label Q control | 75 | 32 | 0 |
| State-only V(s,h) null | 75 | 35 | 0 |

N120 modifies Level-3 selection in up to **23** of the 75 `vc33` actions for the MC model and **21** for TD(lambda), with no native reward gain; the shuffled-label control also changes **20** decisions. Hard Q replacement changes many more, **66** in `vc33` and **29** in `tu93`, again without a win. The state-only null is action-for-action identical to the original local-effect controller on both games.

### Additional policy seeds

Two more policy seeds (77, 78), for local, MC and TD(lambda) arms on `vc33` and `tu93` (**12 native episodes**), preserve the exact two Level-2 completions, with **zero Level-3 completions**. These seeds reproduce exposed starting layouts and cannot be treated as independent environments.

## Verification

- Frozen `submission.py`: `e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d`.
- Frozen `submission.ipynb`: `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`.
- Offline historical corpus: **125/125 episodes and 13,856/13,856 charged action requests** replayed exactly during feature extraction (frame hashes and real rewards).
- N120 Monte Carlo full public suite: **25 episodes / 2,787 native actions** independently replayed exactly.
- N120 targeted ablations: **14 episodes / 1,276 native actions** independently replayed exactly.
- N120 matched-seed controls: **12 episodes / 1,089 native actions** independently replayed exactly.
- **9/9** regression tests passed, including reward-label integrity, TD(lambda) terminal and level-boundary behavior, state-only invariance, source hashes and family separation.
- All reported full public benchmark outcomes were compared against actual N114 and N117 archives, with 25/25 exact pre-Level-3 action/frame/reward parity.

## Deployment and next evidence requirement

**Do not promote N120. Keep frozen N093 as the competition submission fallback; retain the 15-level local-effect policy strictly as an unvalidated experimental alternative.** N120 does not add any new native reward and has no evidence for hidden-layout generalization.

The next useful data source would be *independent Level-2 and Level-3 rewarded native trajectories across multiple game families*, not more bootstrapping from the same failures. Without them, a value network can learn behavior-policy timeout patterns and time-to-win on Level 1, but it cannot identify whether an unseen Level-3 silent setup action is causally useful. The legal alternatives are to collect more **charged**, observable successful interactions on unseen configurations, or to develop a more sample-efficient online algorithm that produces its own genuine reward and validates improvement against an independent held-out test set.