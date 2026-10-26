# N112 — action-conditioned forward dynamics and MCTS: evidence audit

**25 October 2026. Research branch only. No Kaggle submission and no demonstrated new ARC completion.**

## 1. What was implemented

1. The unchanged frozen B1 optimistic tabular Bellman controller and N093 **pretrained** PUCT action ordering select all Level-1 native actions. No hindsight gradient updates or new test-time oracles.
2. After an actual SDK Level-1 reward, fit a lightweight **nonparametric action-conditioned empirical delta forward model** from that game's nonreward Level-1 transitions. The Level-1 win transition is excluded as a physical-dynamics target because the SDK advances to another level.
3. Derive a *candidate* visual goal by comparing the **pre-reward observation** with the last outgoing Level-1 frame in the reward response, `frame[-2]` for the archived traces. Do **not** treat `frame[-2]` as the pre-action state or claim a necessary goal predicate.
4. On Level 2, rank legal B1 candidate native actions, search in the learned forward model with depth-three, 192-iteration bounded MCTS, and execute a proposal **only** if its predicted transitions satisfy independent confidence and contrast criteria. Otherwise fall back to frozen B1/PUCT. All SDK actions are charged.

**Deviation from requested neural architecture:** this is an empirical transition-memory dynamics model, **not** a CNN, XGBoost ensemble, or universal learned physics representation. That choice makes tiny per-game transition buffers and uncertainty directly auditable. Therefore the experiment validates a minimal MBRL integration and identifies bottlenecks, not neural world-model superiority.

## 2. Fixed held-out Level-1 action-effect prediction

Original N103 source has 1,848 transitions from 60 policy-seed episodes. Fit on seeds 276–278, test on **15 held-out seed-279 episodes**. This is a **trajectory holdout only**, not a novel native layout, and seed 279 already appeared in historical research.

All 13 reward handoff transitions are separated from the 436 nonreward action-effect transitions; no Level-2 incoming frame is treated as a Level-1 physics example.

| Model / split | Test steps | Pixel accuracy | Changed-pixel precision | Changed-pixel recall | Changed-pixel F1 |
|---|---:|---:|---:|---:|---:|
| N112 empirical forward (all nonreward) | 436 | 99.46% | 96.12% | 59.46% | 73.47% |
| Copy current image | 436 | 98.75% | 0.00% | 0.00% | 0.00% |
| In-support wrong-action control | 436 | 98.55% | 24.73% | 7.57% | 11.59% |
| N112 exact seen frame/action | 159 | 99.47% | 99.58% | 70.11% | 82.29% |
| N112 novel frame/action | 277 | 99.46% | 91.15% | 48.04% | 62.92% |

**Interpretation:** changed-pixel prediction is clearly action-dependent on this observational split, but many states recur and prediction still misses over half of changed pixels on novel frame/action pairs. A copied full frame already attains 98.75% accuracy. The model does not meet an 80% changed-pixel recall gate on novel pairs.

## 3. Native Level-2 prediction and search

Ten historically exposed N093 training families, native seed 47 and policy seed 76, at most 200 charged native actions *per level*. The actual N112 Level-1 action/observation sequences are **exactly** the previously verified frozen baseline trajectories.

| Metric | Frozen B1 + N093 pretrained PUCT | N112 guarded MCTS |
|---|---:|---:|
| Level-1 completions | 9/10 | 9/10 |
| Level-2 completions | 1/10 | 1/10 |
| Charged SDK actions | 1116 | 1116 |
| In-memory MCTS iterations | — | 5184 |
| MCTS search invocations | — | 27 |
| Model inference calls in search | — | 969 |
| Trusted complete action plans | — | 0 |
| Model-planned native actions | — | 0 |

Across 939 *nonreward* Level-2 transitions on the baseline trajectory, N112 predicts the next native frame with:

- Pixel accuracy: **99.20%** (copy-current-frame control: **99.23%**).
- Changed-pixel precision: **44.80%**, recall: **6.52%**, F1: **11.38%**.
- This dataset is a **Level-2 forward-model generalization evaluation** only; no Level-2 examples were added to the fitted transition buffers.

### Native per-family results

| Family | L1 native actions | L2 native actions | Levels | Nonreward L1 dynamics rows | Goal contrast pixels | MCTS searches | Accepted plans |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ar25` | 15 | 200 | 1 | 14 | 105 | 4 | 0 |
| `cd82` | 8 | 100 | 1 | 7 | 51 | 4 | 0 |
| `g50t` | 17 | 130 | 1 | 16 | 49 | 4 | 0 |
| `lp85` | 6 | 190 | 1 | 5 | 288 | 4 | 0 |
| `ls20` | 13 | 66 | 1 | 12 | 49 | 3 | 0 |
| `m0r0` | 25 | 151 | 1 | 24 | 77 | 4 | 0 |
| `s5i5` | 50 | 0 | 0 | 0 | n/a | 0 | 0 |
| `sc25` | 17 | 26 | 1 | 16 | 4 | 1 | 0 |
| `tu93` | 22 | 50 | 1 | 21 | 19 | 2 | 0 |
| `vc33` | 3 | 27 | 2 | 2 | 265 | 1 | 0 |

Only `vc33` completed Level 2. That case was exposed before N112 and is **not** a new MCTS completion: the executed actions exactly match frozen B1/PUCT.

## 4. Causal and safety controls

- **Action ablation:** replacing the correct action with another source-supported action reduces held-out changed-pixel recall from 59.46% to 7.57%. This supports genuine action conditioning within the known native data; it does not prove cross-layout dynamics generalization.
- **Aliased-visual-state guard:** if the Level-1 source contains identical `(frame, action)` with conflicting observed successors, forward prediction abstains instead of treating one observed successor as physics.
- **Toy positive:** known synthetic action dynamics allow bounded MCTS to select and accept a goal-reaching plan. This tests code mechanics only.
- **Native plan gate:** MCTS simulations do not call `env.step`. Predicted plans must meet minimum supported-action confidence and a terminal-change proxy before one native click is committed. No plan was accepted in real ARC development games.
- **Native replay:** 1116/1116 charged actions were reproduced through a fresh SDK environment without invoking the forward model, B1 actor, or MCTS. All rewards and public frame hashes matched.
- **Budget:** native action limit enforced at 200 per level; no explicit RESET probes; no hidden-test games used for learning or evaluation.

## 5. Why the N112 proposal has not cleared the barrier

1. The Level-1 data are inadequate for robust physical forward prediction on changed Level-2 layouts and controls. In the native runs, the fitted forward model typically has only 2–24 nonreward observations per game.
2. Level-1 pre-reward → outgoing-frame contrast captures the last rewarded visible change, **not** a verified necessary-and-sufficient task goal. The earlier N102 controls demonstrated many such changes at nonreward times.
3. Generative planning cannot repair the model: deep MCTS compounds one-step errors. Its zero charged-call property is a compute/accounting fact, not an accuracy guarantee.
4. The planner reuses the legal B1 root candidate-action vocabulary at predicted nodes. It is not a proven comprehensive search over novel Level-2 UI controls.
5. Historical training families and repeated layouts cannot support leaderboard/generalization claims, regardless of offline reproduction quality.

## 6. Decision

**Keep the frozen B1 + N093 pretrained PUCT `submission.ipynb` unchanged.** N112 is a correctly wired, conservative model-based planning experiment with no demonstrated new native completion. It is not ready to replace the Kaggle submission.

Progression would require an action-conditional forward model that demonstrably improves **novel** native next-effect prediction and calibrated multistep rollout fidelity; only then should MCTS be allowed to execute Level-2 proposals.

**N093 accounting correction:** its original five-arm reference reports 27 Level-1 plus 3 Level-2 completions = **30** for the frozen B1/pretrained-PUCT arm over 30 episodes. The oft-repeated **33** total is not that arm's verified result.