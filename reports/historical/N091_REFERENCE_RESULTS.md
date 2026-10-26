# N091 — Neural-Anchored Contrastive Exploration

**Date:** 25 October 2026  
**Decision:** rejected for B1 promotion. Completed, native-replayed experiment.  
**Targeted failure mode:** B1's optimistic `Q_init = 1.0` prevents its neural prior from ordering previously unseen actions except via tie-breaking.

## 1. Tested hypothesis and competing explanations

The requested mechanism combines (i) Level-1 test-time contrastive learning of the reward-relevant action and (ii) Level-2 Q initialization with the adapted neural scoring function rather than uniform optimistic 1.0. In theory, this would make the agent select actions it expects to lead to native reward before exhausting alternative candidates.

A competing explanation is that B1's pretrained neural prior does not provide a calibrated reward-value signal; preferential Q initialization may amplify wrong rankings. We therefore evaluated the components independently.

**Crucial source correction:** B1 does not sample all 4,096 click coordinates uniformly; it starts from connected-component candidates and directional legal actions, then progressively widens click positions. B1's policy logits are uncalibrated and range around −50 to +14 on sampled observations, so `sigmoid(raw logits)` would effectively set all Q values to zero. We therefore use an explicit, same-for-all-arms relative score transform.

## 2. Implementation

### 2.1 Level-1 source examples

The on-policy SDK sequence for each episode supplies tuple `(frame, previous_frame, legal actions, chosen action, next frame if nonwinning, native reward)`. Only the winning Level-1 prefix, without the postwinning Level-2 frame as a transition target, may affect gradients. The native terminal action is the sole definite positive label `r=1`. Up to 24 previously attempted actions with actual `r=0` form immediate-reward negatives, with weights 0.4 for visually unchanged actions and 0.2 for others.

**These are negatives only for immediate native reward, not evidence of long-horizon uselessness.** A rewarded sequence can require nonreward actions. Unchosen alternative actions are never silently marked negative; they lack native counterfactual evidence. Each game provides only one actual positive example per first successful level. The `s5i5` trials do not win Level 1 and consequently perform no adaptation.

### 2.2 Contrastive loss

The pretrained policy logit `l_theta(s,a)` is converted to a *relative logit*, using the median and standard deviation of candidate logits at that decision point:

```
z_theta(s,a) = clip((l_theta(s,a) - median_a l_theta(s,a))
                       / max(2.0, std_a l_theta(s,a)), -8, 8)
```

Training minimizes weighted binary cross entropy for actual immediate rewards, an additional pairwise logistic margin ranking of the terminal positive over real nonreward actions, a low-weight pretrained-policy distillation loss, and parameter regularization. The updated tensors are `trunk.3` and the policy head; the original Q head remains frozen. This is a **discriminative objective for immediate rewards**, not a proof of causal necessity or a fitted discounted-return function. Thirty-two Adam updates at learning rate 0.0002 are used, once, after native Level-1 completion. The original B1 checkpoint is reloaded at the start of each new game episode.

### 2.3 Level-2 neural Q anchors

Before Level 1 completion, B1 retains its original optimistic value `Q=1.0` and exact learning behavior. At Level 2, newly created Q-node actions are initialized as:

```
Q_init(s,a) = sigmoid(z_theta(s,a))
```

The same mapping applies to newly widened click actions. The original `gamma=0.985` Bellman backup and reverse-state propagation, legal actions, candidate generation, native reward and Q-node reset on level advancement are untouched. All action types—including direction actions and ACTION6 click coordinates—remain legal. There are **no additional discovery probes or resets**. The Q anchor is a bounded, candidate-relative ranking, *not* a calibrated expected return. It can change as the candidate set widens, which is an additional limitation.

### 2.4 Five comparison arms

1. Original frozen B1: original policy model, Q initialized at 1.0, no test-time learning.
2. Raw neural Q anchor: identical network, but Level-2 Q uses the relative neural value without training; isolates anchoring.
3. Contrastive TTT with original optimistic Q: updates neural weights but retains original Q tie-resolution; isolates training.
4. N091 combined: contrastive TTT plus Level-2 neural anchoring.
5. BC anchor: identical Q anchoring with N090 behavioral-cloning updates, replacing the contrastive objective.

All evaluations are 10 established public *training* families × policy seeds 76/77/78, SDK seed 47, maximum 200 policy actions, same frozen checkpoint and environment, and no extra probe calls. The other 15 previously evaluated public families were not used. This is a development test, not untouched-game generalization.

## 3. Native results

| Policy | Native levels completed | Level-1 rewards | Level-2 rewards | Charged SDK calls | TTT episodes | Q anchors initialized |
|---|---:|---:|---:|---:|---:|---:|
| Frozen B1 | **30** | 27 | **3** | **3,154** | 0 | 0 |
| Raw neural anchor | 27 | 27 | 0 | 3,383 | 0 | 21,393 |
| Contrastive TTT, original Q | 27 | 27 | 0 | 3,028 | 27 | 0 |
| **N091 contrastive + anchor** | **27** | 27 | **0** | **3,020** | 27 | 24,156 |
| BC TTT + anchor | 27 | 27 | 0 | 3,254 | 27 | 21,193 |

The three initial wins on `vc33` Level 1 occur at action 3 for every policy; frozen B1 then wins Level 2 at overall action 32, while all modified arms fail its Level-2 reward. No treatment adds an additional completion on `sc25`, `ar25`, or any other training game. The 27 native Level-1 reward milestones are reached at exactly the same action index by all five arms. All arms fail Level 1 on `s5i5`.

Total charged calls **are not an efficiency estimator when completion differs**: B1 proceeds into later levels after wins, while a treatment that misses a win may terminate the episode early. The success requirement of bypassing 30–50 actions before *an equivalent Level-2 reward* therefore fails outright.

There are 27 genuine fine-tuning episodes in each TTT arm. Contrastive training made 864 gradient steps across 30 evaluation episodes (32 updates on 27 successful-Level-1 episodes). The median training objective dropped approximately 2.225 → 1.965; the measured weight change and lower training loss confirm successful optimization, **not** improved ARC reward attainment.

### 3.1 Game-level statistics

All ten training families show the same native first-reward counts under all arms. Nine families have no second reward under any policy. `vc33` is the sole game with a baseline second reward: B1 3/3 vs 0/3 for each treatment.

A bootstrap resampling **game families**, not treating same-start policy seeds as independent environments, yields mean change in levels completed per game-seed of −0.1 and an approximate 95% interval of **[−0.3, 0.0]** for every treatment versus B1. This is not evidence of performance improvement, and the 10 game families were already development/training families.

### 3.2 Component attribution

- Raw neural anchoring alone loses the three `vc33` Level-2 completions. Thus Q initialization is unsafe in this form without invoking fine-tuning.
- Contrastive TTT with the original Q initialization also loses the same three completions. Thus the current reward-discrimination training objective can damage the neural policy even if B1's optimistic Q behavior is retained.
- Combining the two does not recover any loss. Substituting behavioral cloning for contrastive learning does not recover it either.
- On the initial `vc33` Level-2 decision, both anchored versions select the fourth white candidate `(1,45)` with Q near 0.89, but the native reward does not occur then: readiness and action sequence still matter.

The positive control with frozen B1 exactly reproduces the previously verified N090 action sequence in all 30 episodes. Therefore the treatment regression is not attributable to a changed SDK or a broken baseline.

## 4. Verification and provenance

- **150 native episodes, 15,839 native SDK actions**, independently re-executed from action traces. Every initial observation, recorded pre/post frame SHA-256, native reward, level transition and game state matches.
- **30/30 frozen B1 action traces** byte-for-byte match the N090 historical baseline ledger.
- The checkpoint SHA-256 is `42996eed8eea3581971b054a499cf9063d82862147222d8d79c6c0d632e6c5f3`; every episode uses it as its pre-adaptation initialization.
- Level-2 observations are never gradient-label sources; no winning post-action same-level frame is fabricated.
- New tests verify bounded calibration, source-only true labels, unchanged B1 Level-1 Q initialization, actual L2 anchoring and progressive widening, a frozen Q-head, and the forbidden-family gate.
- Frozen source/SDK and prior N090 evidence are bundled for clean-room checks.

## 5. Scientific limitations

A primary conceptual mismatch remains:

\[\Pr(r_{t+1}>0 \mid s_t,a_t)\;\not\equiv\;Q^{\pi}(s_t,a_t)=\mathbb E_{\pi}\!\left[\sum_{k=0}^{\infty}\gamma^k r_{t+k+1}\mid s_t,a_t\right].\]

In games with prerequisites, a nonreward action can have high long-term value, while a terminal action can only succeed when prerequisites are complete. The data contains one labeled reward-positive action per Level-1 trajectory and no prospective nonwinning counterfactuals at exactly the winning decision point. It is therefore statistically insufficient to learn an accurate, transferable reward-value surface purely by this contrastive criterion. Direct Q initialization from relative policy logits **changes exploitation behavior**, but it does not convert logits into an empirically validated return.

The same three seeds were evaluated on the same native game configuration; this primarily measures policy-choice sensitivity and reproducibility, not independent task variation. The source neural checkpoint itself was previously trained using public Level-1 data. No private holdouts, hidden engine variables or Kaggle leaderboards were used.

## 6. Decision

**Reject N091 for B1 deployment.** It achieves 27/30 instead of B1's 30/30 completed native levels under the locked training-family protocol, despite genuine gradient updates, supported neural Q initialization and preserved Bellman learning.

The next defensible target is to estimate long-horizon advantage with better credit assignment and cross-level uncertainty calibration, and demonstrate *within-level* reward improvement before granting the neural head sole authority over Q initialization. Merely increasing optimism or the contrastive training strength is not supported by this evidence.

**B1 remains unchanged; the 15 previously used public evaluation families remain unopened in this iteration.**