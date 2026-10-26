# N090 — Test-Time Fine-Tuning of B1's Neural Action Prior

**Date:** 25 October 2026  
**Decision:** **Not promoted to B1.** Two implemented test-time training (TTT) variants perform genuine gradient-based adaptation after a native Level-1 win but obtain **zero additional native Level-2 rewards** and **zero reduction in reward-milestone action counts** compared with frozen B1 across the ten predeclared training families.

## 1. Question and rationale

The rejected N089 hand-designed deictic Q abstraction achieved 9/30 native levels versus frozen B1's 30/30 in the same training-family protocol. N090 therefore leaves B1's raw-observation Q-state hash, native-only Bellman updates, and `self.nodes.clear()` level isolation **unchanged**. Instead it tests whether updating B1's pretrained neural action prior from its *own successful Level-1 observations* improves subsequent Level-2 gameplay. No cross-level Q-value transfer, causal probe sweep, action mask, hand-coded objective, teacher trace or privileged game state enters acting.

This is not the proposition that moving to Level 2 necessarily creates a different MDP, nor that test-time training must solve arbitrary level twists. It is one concrete, falsifiable implementation of online per-game neural adaptation.

## 2. Frozen protocol

- **Families:** `ar25`, `cd82`, `g50t`, `lp85`, `ls20`, `m0r0`, `s5i5`, `sc25`, `tu93`, `vc33` — the existing 10 public training families.
- **Native SDK seed:** 47. **Policy seeds:** 76, 77, 78. These seeds produce the same game configuration, so seeds are not independent game layouts.
- **Budget:** maximum 200 B1 policy decisions per native episode, with game-over termination when the SDK reports it. Every SDK step is charged; N090 adds **zero** discovery/reset steps.
- **Arms, matched per family and seed:** (1) untouched frozen `PortableAgentCore`; (2) test-time behavioural cloning (BC) on recent actions of B1's *own* completed Level-1 trace; (3) the same BC plus an auxiliary next-observation prediction objective on nonreward Level-1 transitions.
- **Checkpoint:** frozen, original `prior_checkpoint.pt`, SHA-256 `42996eed8eea3581971b054a499cf9063d82862147222d8d79c6c0d632e6c5f3`. Each native game begins from that checkpoint, with no persistent weights between games.
- **Update point:** exactly once, after the **actual native Level-1 reward**, before the first Level-2 policy action. If no Level-1 reward occurs, no network update is permitted.
- **Supervision:** on-policy Level-1 `(frame, previous-frame, legal-actions, candidate-set, selected-action, next-frame-if-nonreward)` records; never read Level-2 teacher trajectories, terminal post-winning frames as same-level targets, or reserved evaluation-family data.
- **Policy update:** 24 Adam steps, learning rate `8e-5`; train B1's final 192→192 trunk Linear and neural policy head. Earlier feature layers and Q head receive no optimizer steps. Short-window BC uses at most 16 most recent Level-1 actions, chosen actions contrasted against up to 12 deterministic alternative legal candidates per decision. A frozen-teacher KL penalty stabilises adaptation.
- **Dynamics auxiliary:** predicts an **80-dimensional coarse next-observation target**: an 8×8 blockwise changed-pixel proportion and the next frame's 16-colour occupancy histogram, from the chosen `(s,a)` representation. Up to 48 nonwinning source transitions are eligible. **It does not generate a full 64×64 successor frame.** The auxiliary head shares the trainable final trunk layer; it is discarded after adaptation, leaving the adapted policy as the acting model.
- **Control policy:** B1's `learning=True`, native level-up reward only, original tabular Bellman update and predecessor graph, same neural tie-ranking behavior, no Q injection, same legal candidate generator and progressive widening.

**Major constraint:** the historical frozen B1 checkpoint had been trained on Level-1 data from all 25 public families. Accordingly, this is repeated adaptation on *studied public families*, **not** an unseen-mechanics generalization test or private Kaggle score.

## 3. Main native results

| Measure | Frozen B1 | TTT BC | TTT BC + next-state auxiliary |
|---|---:|---:|---:|
| Native episodes | 30 | 30 | 30 |
| Level-1 native completions | 27 | 27 | 27 |
| Level-2 native completions | 3 | 3 | 3 |
| **All native level completions** | **30** | **30** | **30** |
| Total charged SDK calls | **3,154** | **3,200** | **3,196** |
| Extra native probe/reset calls | 0 | 0 | 0 |
| Episodes with changed neural weights | 0 | **27** | **27** |
| Gradient steps over successful episodes | 0 | **648** | **648** |
| Episodic reward milestones reached earlier than B1 | — | **0/30** | **0/30** |
| Reward milestones reached later than B1 | — | **0/30** | **0/30** |
| Episodes where subsequent action sequence differs from B1 | — | 20/30 | 21/30 |

**All 30 reward milestones match B1 at exactly the same charged action index.** The extra 46 and 42 SDK calls under the adapted arms occur **after** the last common reward, with no additional native completion. Thus neither lower/higher total episode length nor lower nonreward frame-change loss may be equated with faster reward acquisition.

At the family level, the source rewards remain:

| Game | Levels / 3 runs (B1, BC, BC+dynamics) | First reward action | Notable adapted difference |
|---|---:|---|---|
| `ar25` | 3, 3, 3 | 15 | Same first reward; ±1–2 calls after it |
| `cd82` | 3, 3, 3 | 8 | Later action sequences differ, no reward gain |
| `g50t` | 3, 3, 3 | 17 | Later action sequences differ, no reward gain |
| `lp85` | 3, 3, 3 | 6 | Small shifts in unsuccessful later exploration |
| `ls20` | 3, 3, 3 | 13 | Same actions and rewards |
| `m0r0` | 3, 3, 3 | 25 | Later decisions differ without additional reward |
| `s5i5` | 0, 0, 0 | None | No Level-1 success, therefore **no TTT** |
| `sc25` | 3, 3, 3 | 17 | Later decisions differ without Level-2 success |
| `tu93` | 3, 3, 3 | 21–22 | At seed 78, +42 unsuccessful calls under both adapted arms |
| `vc33` | 6, 6, 6 | 3; second reward 32 | Level-2 completion retained, not accelerated |

No reward-completion difference exists to bootstrap: the paired reward difference is exactly zero in the tested sample. The 10-family sample and three repeated policy seeds are too small to infer that test-time training is useless in general.

## 4. What N090 did and did not learn

**Positive engineering result:** A native Level-1 episode produces legitimate gradient data; the pretrained neural prior updates *within a game* and the modified weights affect B1's future action sequence. Training consumes no additional native SDK probes. The original Q system works unchanged, and weights are reset to the frozen checkpoint for the next game.

**Negative control result:** The learned preference produces no additional win and never advances a common win sooner, including on `vc33` and `sc25`. The auxiliary next-observation target provides no observed native reward gain over BC alone. At least one adapted trajectory spends longer searching after achieving its last reward.

**Why this is plausible:** B1 was already strong on all accessible Level-1 starts. Cloning B1's own winning *trajectory* supervises the model to reproduce choices, but does not prove those choices were necessary or causally sufficient. Unrewarded visual transition prediction, especially at coarse resolution, captures mechanics without saying which resulting states satisfy the task. The original pretrained actor is already a powerful prior; fine-tuning from 2–25 on-policy transitions may sharpen an existing bias instead of uncovering new analogies.

**Unresolved:** Whether a richer structured latent successor objective, contrastive reward-aware temporal credit, more diverse within-game actions, regularised low-rank adaptation or longer adaptation would help. The present implementation does not test those hypotheses. In particular, this is **not** a full generative 64×64 world-model learner.

## 5. Independent source and native verification

- 90 complete native episodes, all from the predeclared ten families.
- **9,550 SDK actions** independently replayed from the logged action records in separate simulator instances. Every pre-action and post-action frame SHA-256, level count, native reward and terminal-state token matched.
- Fresh frozen B1 control matched the previously archived N087 B1 control on **30/30** family/seed pairs for native levels completed and total charged actions.
- Pretraining checkpoint SHA-256 was verified unchanged. Q network parameters are not optimizer-updated by N090; no Bellman reward shaping, SDK reset hack, hard mask, causal Q seeding, or teacher actions.
- Runtime and source SDK are included to permit standalone offline reproduction. The experiment does not read the game-engine source or privileged state.
- Run `./RUN_N090_CHECKS.sh` for manifest, unit/integration and evidence-accounting checks; run `./RUN_N090_NATIVE_REPLAY.sh` for the longer, native 9,550-action check. Re-running full native training with `./RUN_N090.sh` writes a new ledger after respecting the existing-file guard.

## 6. Research decision

**Do not integrate N090 into deployed B1.** It is a complete, reproducible negative experiment, not evidence that test-time neural adaptation is fundamentally unsuitable for ARC-AGI-3. The next credible test should make the *objective* more informative: predict a verified, reward-relevant successor distinction or train a policy to adapt from genuinely independent evidence rather than merely imitate its own pretraining-biased choices. Keep the 15 previously evaluated public families burned, preserve B1, and perform any new selection on training data before obtaining fresh evaluation evidence.