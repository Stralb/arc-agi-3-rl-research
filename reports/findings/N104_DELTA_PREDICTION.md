# N104 — Offline Action-Conditional Delta Prediction & Approximate Predictive Equivalence

**Date:** 25 October 2026  
**Research objective:** Resolve N103's near-zero changed-pixel recall with categorical delta prediction, then determine whether action-conditional latent predictions provide stable search-state keys.  
**Status:** **Aggregate delta-recall gate passed; mechanistic recurrent-state, novel-state transfer and bisimulation-key gates failed / remain unsupported.**  
**No cluster jobs, no new native Level-2 attempts, no `vc33`-specific optimization, no official benchmark score.**

## 1. Scientific decision

The *measurement* goal is achieved: a lightweight GRU trained primarily on directly supervised pixel-change masks attains **81.01% recall** at **21.96% precision** on N103's 449 held-out-by-policy-seed transitions (23,797 positive changed pixels out of 1,839,104 pixel positions). This yields **34.56% F1**. The validation-selected probability threshold is **0.325593**. The model predicts 87,767 pixels to change, of which 19,278 actually change; the other 68,489 are false-positive pixels.

However, the result does **not** establish a generally useful POMDP information state:

1. Held-out inputs never observed as an exact training `(frame, action)` combination reach **76.66% recall** at **15.35% precision**, short of the 80% goal.
2. Performance is unequal across training families, with `tu93` only **43.54% recall** and `g50t` **74.43%**.
3. A separately trained action-blind model reaches **80.91% recall, 19.95% precision and 32.00% F1**; removing or disrupting previous-action history in the fitted recurrent model changes very little, while **resetting history improves F1 to 38.40%** at its original calibrated threshold. These facts substantially weaken claims of recovered latent lock dynamics.
4. The fitted signature-distance key distinguishes **three of four** held-out conflicting successor pairs but splits **12 of 35** pairs with identical successors. Its distance threshold is **0.0005268** in averaged action-response probability, too fragile for a general Markov-state equivalence claim.
5. Native layouts are identical across the four SDK seeds within each family, ~**35%** of held-out test `(frame,action)` keys occur exactly in the two fitting policy seeds, and the N103 test seed had already been exposed in prior research. The evaluation is neither an independent new-layout test nor a genuinely untouched holdout.

**Recommendation:** Retain N104 as a supervised changed-region detector and an auditable negative result for recurrent key construction. Do **not** deploy a latent RTA* controller, and do not infer causality or bisimulation from its hidden vectors.

## 2. Source and task fidelity

The dataset is the frozen N103 offline Level-1 ledger, not reconstructed game engine state:

| Partition | Policy seeds | Episodes | Executed actions | Positive changed pixels |
|---|---|---:|---:|---:|
| Fit | 276, 277 | 30 | 869 | 50,210 |
| Calibration | 278 | 15 | 530 | 29,160 |
| Evaluation | 279 | 15 | 449 | 23,797 |
| **Total** | — | **60** | **1,848** | **103,167** |

All frames are public `uint8[64,64]` ARC palette-index observations. True target is the **Boolean** categorical change mask `M_t[i,j] = 1[o_(t+1)[i,j] != o_t[i,j]]`; palette subtraction is **not** treated as a numerical physical distance. The predictor's inputs at step `t` are `o_t`, actually executed action `a_t`, and recurrent state derived from **previously observed** frames/actions. The supervised `after[t]` is used only in the loss and evaluation, never as a prediction-time feature. For rewarded steps, N103 already recorded the last outgoing Level-1 frame, not an incoming Level-2 state.

The 1,848-record source SHA-256 is `e7893617548df1589bf0ff705e0b1430df6821c3ad9130d3f44d4b28ff5f190d`. The upstream self-contained N103 ZIP SHA-256 is `a97a81e04013a1dc25c3f52ccfd63606eb99cb4432035b44348016992277c2b5`. Both are included or referenced under `inputs/`.

An important correction to the N104 prompt: **0.15% was the N103 model's changed-pixel recall, not the observed changed-pixel prevalence.** The positive-mask prevalence is **1.36% overall and 1.29% on the evaluation split**. An always-predict-change classifier therefore achieves 100% recall with **1.29% precision**, which is not a useful dynamics model.

## 3. Model and training procedure

The fitted model has **47,613 parameters**: one-hot palette-frame convolutional encoder, 48-dimensional recurrent hidden state, current-action embedding (including click geometry), FiLM-conditioned spatial delta decoder, changed-pixel colour classifier and 32-dimensional auxiliary delta-latent head. No game ID, source-code features, privileged puzzle state or test-family-specific labels enter the neural network.

- **Primary supervision:** changed-pixel sigmoid/BCE with `pos_weight=24` and soft Dice; predicts categorical pixel changes, not the next full frame.
- **Secondary supervision:** next-colour cross-entropy **at changed pixels only**. On test it identifies the new palette at a truly changed pixel **72.56%** of the time. This is *conditional colour accuracy*, not an end-to-end exact-delta score.
- **Optional contrastive term:** a learned 32-dimensional predicted delta code competes with a learned encoder of the actual downsampled changed-mask/signed-colour difference. In-batch identical targets are excluded as false negatives. This term is weighted `0.06` for the primary and frame-only/action-blind controls and `0` in the contrastive ablation.
- **Causal recurrence:** hidden state is updated from `o_t`, the previous executed action and observed `o_t - o_(t-1)` indicator (for prior change magnitude); it is not passed the future supervised next frame. Episode boundaries reset hidden state.
- **Training:** 250 seeded AdamW minibatch windows of length five, four independently selected fitting episodes/window, with at most 14 preceding public steps to warm the GRU hidden state. The *corrected* trainer masks a non-existent previous action at episode starts rather than inventing action zero. CPU only.

**Threshold calibration:** Choose the highest-F1 candidate among validation thresholds with recall >=80% and precision >=10% if available. Apply its exact value unchanged to policy seed 279. At the selected validation threshold (0.325593), validation recall = 80.61%, precision = 22.54% and F1 = 35.23%. A threshold optimized solely for F1 without the recall requirement would select a more conservative trade-off; the high-recall operating point must be understood accordingly.

### Source limitations

The split is by *policy seed/whole episode*, not by independently generated game layouts. The same five initial screenshots recur across seeds. A first 50-step N104 pilot also inspected test seed 279, so this is **not sealed prospective testing**. The subsequent model comparisons and implementation correction were made within this known research corpus; fresh independent native layouts remain necessary for confirmatory generalization claims.

## 4. Held-out mask prediction and controls

| Model | Recall | Precision | F1 | Comment |
|---|---:|---:|---:|---|
| **Corrected recurrent + delta contrast** | **81.01%** | **21.96%** | **34.56%** | Aggregate mask goal passed |
| Separately trained frame-only, same loss | 80.39% | 19.12% | 30.90% | Small recurrent-model advantage on these paths |
| Separately trained recurrent, no contrastive term | 82.13% | 17.46% | 28.79% | Higher recall, more false-positive pixels |
| Separately trained recurrent, action blind | 80.91% | 19.95% | 32.00% | Action information has limited incremental value |
| All-zero/copy-last mask | 0% | 0% | 0% | Identity prediction |
| Always-change mask | 100% | 1.29% | 2.55% | Trivial high-recall baseline |

All four trained models use the exact same fit/calibration/evaluation episodes, fixed optimizer-window budget and model size; each has its own calibration-only operating threshold. Comparison is at the >=80%-recall *operating point*, rather than peak F1 unconstrained by recall.

**Inference-only ablations of the fitted primary recurrent model, at its frozen threshold:**

| Test-time perturbation | Recall | Precision | F1 |
|---|---:|---:|---:|
| No ablation | 81.01% | 21.96% | 34.56% |
| Zero current-action encoding | 80.77% | 20.78% | 33.06% |
| Zero previous-action encodings | 81.52% | 21.88% | 34.50% |
| Shuffle preceding actions | 81.15% | 21.76% | 34.31% |
| **Reset recurrent history every step** | 79.90% | **25.27%** | **38.40%** |

This last row is especially important. Recurrent history increases recall by ~1.11 points relative to the reset-history ablation but **worsens precision/F1**. It would be incorrect to infer that the model is confidently using history to resolve latent locks. Future causal-state tests should evaluate accurate action-specific transitions and state equivalence, not recall alone.

### Performance by source family

| Family | Changed-pixel recall | Precision | Outcome versus 80%-recall target |
|---|---:|---:|---|
| `ar25` | 88.49% | 36.20% | Pass |
| `g50t` | 74.43% | 10.65% | Fail |
| `lp85` | 99.54% | 26.49% | Pass |
| `m0r0` | 70.62% | 37.60% | Fail |
| `tu93` | 43.54% | 41.44% | Fail |

A high aggregate performance therefore hides broad variation. At the exact training-key overlap level:

- **157** test transitions share an exact frame/action input key with fitting data: recall **85.25%**, precision **35.30%**, F1 **49.92%**.
- **292** test transitions have a previously unseen input combination: recall **76.66%**, precision **15.35%**, F1 **25.58%**.

For context, the source N103 recurrent predictor reported changed-pixel recall **0.1471%**, F1 **0.2931%**, and raw full-frame accuracy **98.01%**, worse than copying the frame (**98.71%**). N104 fixes the categorical mask measurement target and the sparse-loss problem. It does **not** establish ability to predict action-conditional new layouts or true hidden dynamics.

### Uncertainty

A 2,000-sample **whole-episode bootstrap** on 15 policy-seed-held-out episodes yields primary F1 [25.13%, 49.63%]. Its observed F1 advantage over separately trained frame-only is +3.66 points, descriptive paired bootstrap interval [+1.40, +6.03] points. Against action-blind, +2.56 points, interval [+1.07, +2.97] points. Against no-contrast, +5.77 points, interval [-0.68, +7.43] points. This describes variability when resampling the archived trajectories; with repeated starting layouts it is **not** a confidence interval for new game families or unknown levels.

## 5. Predictive equivalence versus actual bisimulation

A correct POMDP information state is a belief distribution over environment states given the complete public action/observation history. Predictive equivalence also depends on future **reward** and **observation** distributions after every legal continuation, not merely instantaneous next-frame masks. A one-step list of predicted binary masks for actions is neither a sufficient Markov statistic nor an exact bisimulation quotient.

N104 runs a **restricted pairwise audit**. Each history is encoded recurrently through *actually observed* past observations/actions. An offline model-only probe predicts the change-mask response to the six common action indices and at most four fit-observed click actions for that family, pooling the response map to 8x8. These probes involve **no native SDK steps**, no resets and no source-code oracle. But importantly, the fit-observed probe set is **not confirmed legal in every particular state**. It is a diagnostic partial action-support set, not the user's requested full legal-action bisimulation test.

Predictive-signature distance threshold is calibrated only using 322 **fit** repeated `(frame,performed action)` pairs, of which 21 have different recorded successor screenshots. The selected threshold is **0.00052677** RMS pixel-response-probability difference. On 39 held-out repeated pairs, **four** have different recorded successors. Results:

| State-key comparison | Detect genuinely different successor pairs | Incorrectly split identical-successor pairs |
|---|---:|---:|
| Visual-only key | 0/4 | 0/35 |
| **N104 predictive-response distance** | **3/4** | **12/35** |
| Same model, shuffled history control | 4/4 | 35/35 |

A complete-link clustering on the 29 repeated held-out input groups creates **40 clusters**, and **one** resulting cluster still contains conflicting recorded successors. The history-shuffle negative control breaks nearly everything apart; merely splitting all observations is not evidence of useful causal states. Four independent conflict pairs are a very small test set, and differing recorded successors can also reflect animation/stochasticity rather than a lock.

**Constructive impossibility guard:** Two invisible lock states requiring one versus two remaining silent enabler actions can have identical one-step observable change masks for every action. After a silent enabler, their subsequent reducer response diverges. Therefore equality of one-step delta signatures **cannot** prove bisimulation even with a perfect predictor. The packaged test `test_identical_one_step_delta_signatures_are_not_bisimulation` locks this fact into the regression suite. The user's proposal to compare all simulated forward trajectories would need a validated model, complete legality and robust multi-step uncertainty treatment—none are established by N104's current training source.

## 6. Code QA, errors and reproducibility

The initial N104 implementation mistakenly encoded a dummy previous action as `0` for a subset of minibatch episode starts. The correction explicitly zeros the previous-action/motion channels for rows at `t=0`. After correction and retraining, primary held-out recall increased from 80.50% to **81.01%**, with F1 from 33.01% to **34.56%**. Prior checkpoints are retained under `results/pre_first_step_fix/` solely for audit; the principal `results/delta_*.pt` are corrected. Vectorized evaluation was added to avoid expensive per-transition inference while preserving exact original calibration values.

The 13 tests cover frozen source counts/hashes, legal history boundaries, response-head equivalence, all-zero-loss resistance, categorical palette labels, data partitions, the train-only predictive threshold, checkpoint metrics and the one-step bisimulation counterexample. `README.md` provides complete commands, including all four full fit/control training runs. The release includes checkpoint predictions, per-family/novel-input analysis, episode bootstrap, signature-cluster diagnostics, visual metric figures, trace provenance and checksums.

## 7. Scientific stop condition and next actionable evidence

1. **Keep** the supervised changed-pixel model as a baseline; the >80% aggregate mask-recall metric is achieved. Avoid reporting raw full-frame reconstruction accuracy as evidence of dynamics.
2. **Do not promote** the latent-state key or deploy native Level-2 RTA*. It has weak action/history dependence, 12 false splits among 35 identical-successor pairs, one unresolved conflicting cluster and extremely limited pair support.
3. The next independent data evidence should be **multiple genuine initial layouts**, balanced observed different-action responses at the *same public image*, and longer silent-prerequisite trajectories that disclose a predictive advantage over history-free controls. This requires legal source collection, not an illegal oracle or hidden simulator state.
4. Before claiming bisimulation, evaluate predictive distributions for **all currently legal actions** and multi-step continuations with calibration and uncertainty. Reward/termination must enter the behavioral equivalence criterion; pooling an immediate pixel-mask map does not establish it.
5. If future source data makes the native recurrent representation causally useful, compare **identical-action-policy Bellman-on versus Bellman-off** execution using the same learned key on training/validation games. Maintain the pre-existing sealed-family policy; no `vc33` development or test-family tuning is justified.

**Overall:** N104 demonstrates a credible, quantified fix to sparse *pixel-change prediction*, not a validated solution to POMDP partial observability or general ARC planning. That narrower, reproducible result is the research contribution.