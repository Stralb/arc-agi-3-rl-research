# N103: Offline Predictive Belief Search and Forced Trajectory Diversity

**Date:** 2026-10-25. **Status:** Offline research; no native Level-2 improvement established. **Scope:** Existing N100/N102 archives, native public Level-1 training SDK, and explicitly labeled synthetic POMDP controls. No cluster, no Kaggle submission, no `vc33` testing.

## Decision (first)

Do **not** deploy a GRU-keyed native RTA* controller yet. A small action-conditioned GRU learns near-perfect hidden prerequisite tracking in one synthetic environment, but its native Level-1 changed-pixel predictions are inadequate and native recurrent-key clustering does not resolve observed conflicting transitions. The underlying recurrence is experimentally active; useful belief abstraction and online planning are separate, unsatisfied gates.

The positive finding is elsewhere: generating diverse, genuine Level-1 successes substantially improves the **selectivity** of the pre-existing fixed contrastive goal-predicate grammar, on the five families in this protocol. This produces *candidate* goals, not identified necessary-and-sufficient causes.

## 1. Source protocol and new native trajectories

- Frozen source: user-supplied `N100_ACTIVE_FSM_20261025.zip`, SHA-256 `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`.
- Acting source: unchanged B1 source/checkpoint and candidate set from the native SDK archive. Randomness only overrides B1's selected action with a uniform member of the **same currently legal B1 candidate set** with probability epsilon. Q/observation updating remains B1's own. No shadow oracle, teacher action labels, simulator state or reset action is supplied to the controller.
- Allowed development families: `ar25`, `g50t`, `lp85`, `m0r0`, `tu93`. The excluded test/validation families were not used to train, select, or run this new policy. No `vc33` source test.
- Predeclared epsilon: 0, 0.15, 0.40. Four policy seeds 276-279 and native seeds 47-50; each attempt stops at first genuine Level-1 reward or 90 actions.
- Fresh local SDK instances: 60; native SDK **steps**: 1,848; Level-1 wins: 53; distinct complete action sequences: 44, comprising 37 distinct winning sequences.
- By epsilon: 0.00 = 20/20 wins, 339 steps, 6 distinct traces; 0.15 = 17/20, 654 steps, 19 distinct; 0.40 = 16/20, 855 steps, 20 distinct. Non-B1 overrides: 0, 91, 289 respectively.
- Native seeds 47, 48, 49, 50 yielded **the same initial 64x64 screenshot within each family** (five distinct initial frames over five families). Hence the attempts are **not independent starting layouts**. There are distinct trajectories under a shared observed initial configuration; an unseen-layout generalization claim is unsupported. Repeated action paths further reduce effective sample independence.
- On a rewarded transition, the next Level-1 frame is the outgoing `frame[-2]`, not the incoming Level-2 screen. Nonreward steps use the SDK post-step observation. No Level-2 training frames were included.

## 2. Pre-existing contrastive goal grammar tested on diverse trajectories

`src/n102_contrastive.py` is an unchanged copy of the predecessor grammar. Candidate `p` must be true in the outgoing terminal frame and false at **every preceding** pre-action observation on that trajectory. The candidate selection is intersection over **different actual winning action sequences** in training seeds 276-278. Seed 279 and every nonreward transition provide separate tests. This is still within a single initial layout per family.

| Family | Distinct training winning paths | Selected shared predicates | Held-out reward events nominated | Held-out nonreward first-flip events nominated |
|:--|--:|--:|--:|--:|
| `ar25` | 6 | 0 | 0/3 | 0/71 |
| `g50t` | 4 | 0 | 0/2 | 0/129 |
| `lp85` | 5 | 7 | 3/3 | 1/44 |
| `m0r0` | 7 | 3 | 3/3 | 1/97 |
| `tu93` | 7 | 1 | 2/2 | 0/93 |
| **Total** | — | **3/5 families nonempty** | **8/13** | **2/434** |

`lp85` produces alignment candidates; `m0r0` yields colour-10 fill/shape candidates; `tu93` yields `c14:absent`. Nominating these predicates is **not** a causal discovery guarantee. Different actions can yield the same terminal picture; terminal animation can create spurious features; no counterfactuals or independent layouts were collected. Treat 2/434 as a *sampled event alarm rate conditional on the pre-selected predicates*, not real-world false-positive probability. No candidate is forced for the two uncovered families.

## 3. Native action-conditioned recurrent predictor

A 48-dimensional `GRUCell` encodes current 64x64 public frame features and the actual legal selected action. It predicts the exact next-frame 16-way pixel palette, changed-pixel map and step-change probability. Full 64x64 outputs are produced (not downsample-only results). Previous observations enter only through hidden state. Two models use the same architecture and 150 training optimizer windows: `frame_only` zeros recurrent history; `recurrent` retains it. An ablation resets the trained recurrent model at test and a second ablation removes action features.

Training: 45 entire episodes from policy seeds 276-278, 1,399 source transitions. Test: 15 **held-out episodes** from policy seed 279, 449 transitions. **37.86% of held-out (frame,action) pairs have appeared in training**, and all native seeds share initial layout per family. Results are exploratory and must not be described as independent game transfer.

| Held-out metric | Frame-only model | GRU with history | Copy-last observation |
|:--|--:|--:|--:|
| Entire-frame pixel accuracy | 97.0071% | **98.0130%** | **98.7061%** |
| Next-frame cross-entropy | 0.217863 | **0.205516** | not comparable (deterministic) |
| Changed-pixel F1 | 0 | **0.002931** | 0 |
| Changed-pixel recall | 0 | **0.001471** | 0 |
| Step-change Brier (lower better) | **0.125630** | 0.126811 | not evaluated |

The recurrent model is somewhat better than the same trained capacity without history on frame CE, **but it is worse than a no-training frame-copy predictor on raw pixel accuracy and virtually never predicts changed pixels**. Pixel copy is a difficult baseline because backgrounds dominate, but the changed-pixel F1 confirms that the model has not learned useful source dynamics. Training for only 150 optimizer windows limits what this experiment says about *possible future models*. No native Level-2 search was run with these weights.

### Native observed-transition collision audit

There are **46** distinct native (frame, action) input keys with multiple subsequent frame hashes in the 1,848-step collection, affecting 123 rows. This is incompatible with a deterministic frame-only transition table **at the level of the recorded observations**; it does not by itself prove those collisions are invisible locks rather than animation or other stochastic effects.

Clustering the GRU before-action hidden vectors with **k=8 fitted on training episodes only** does not remove the **four** conflicting repeated frame/action groups observed in the held-out subset. The visual key has 415 distinct groups, 29 repeated keys, four conflicting keys. The GRU cluster key has 417 groups, 29 repeated keys, **the same four conflicting keys**. Shuffled cluster labels create 439 keys with only one conflicting group by breaking most repeats into singletons; this demonstrates why raw alias-count reduction is not reliable evidence of improved state estimation.

## 4. Synthetic POMDP: recurrent prediction and two approaches to state clustering

This section is **synthetic diagnostic evidence only**. A local hidden-lock environment has three legal actions: silent enabler, gap reducer and decoy. After two enabler actions, a reducer can change the public picture by one unit; its internal unlock counter is not available to the learner. Synthetic Level-1 source trajectories have gap three and *fixed latent depth two*. A 32-dimensional GRU predicts the probability that the next public picture changes, given only observed gap pixels and chosen action.

On held-out random synthetic action paths with gap five, fixed depth two:

- Recurrent model: **F1 0.99960**, Brier 0.00006 over 7,776 source transitions.
- Identical trained network with history reset at every step: **F1 0**.
- Shuffled historical actions: **F1 0.15412**.
- Depth three, which is **outside the training mechanism**: F1 falls to **0.69108**. A successful depth-two source-trained GRU is **not** a generic hidden-lock solver.

Three key representations for search were compared against identical legal synthetic actions, the same visible geometric gap heuristic and the same action budget:

1. Visual-state SHA alone.
2. Raw GRU hidden-state embedding clustered using training-only k-means k=8.
3. **Predictive signature** clustered using training-only k-means k=3: estimated probability of an observable reducer effect after 0, 1, or 2 *model-imagined* enabler actions. These are local model forward passes, not simulator queries, resets, or oracle actions. The expectation that imagined enabler actions leave the public image unchanged is an explicit *synthetic-only* assumption; native deployment would need to predict and update the imagined frame as well.

| Representation | Synthetic L2 completed / 36 | Depth 1 / 12 | Depth 2 / 12 | Depth 3 / 12 |
|:--|--:|--:|--:|--:|
| Visual hash | **30** | 12 | 12 | **6** |
| Raw GRU cluster | 17 | 12 | 3 | 2 |
| Predictive-signature cluster | 24 | **12** | **12** | **0** |

These 36 conditions vary gap (4 or 5), unlock depth (1, 2, 3), and six legal-action order permutations; **they are matched synthetic configurations, not independent game families**. Within the two in-distribution depths, predictive clustering improves mean actions-to-solve relative to the visual controller (21.375 versus 25.875 over the 24 solved matched conditions), but the depth-three OOD failures make it *worse on total completions*.

Its training-only predictive-cluster centers cleanly distinguish three depth-two latent modes (diagnostic AMI 1.0 against hidden simulator labels used only for evaluation). Raw-GRU-vector clusters reach AMI 0.612 on training. That is an important representation lesson: distances between arbitrary recurrent embeddings are not the same as predictive-state equivalence.

Bellman-backup ablation with predictive key: **12/36 action trajectories change**, 1224 online value updates, but **0 added synthetic wins**; a backup-off paired control completes the same 24/36 tasks with the same aggregate actions. On the raw-vector key, Bellman affects 16/36 action trajectories but not win count. Bellman functionality is separately demonstrated by predecessor N101 tests, but its incremental effectiveness is still unproven here.

## 5. Mathematical interpretation and failure gates

The correct POMDP information state is a posterior over latent modes, conceptually

`b_t(z) = P(z_t=z | o_0, a_0, ..., a_(t-1), o_t)`.

A recurrent hidden vector `h_t = f(h_(t-1), encoder(o_(t-1), a_(t-1)))` can approximate a useful predictive statistic **if the input sequences reveal it and the training objective learns it**. It does not automatically recover unobservable engine locks or guarantee Markov sufficiency. Two latent states that generate identical outcomes under every available continuation are observationally indistinguishable. For Level-2 deployment we need held-out evidence that `P(o_(t+1)|h_t,o_t,a_t)` is better calibrated than history-free controls and that the cluster key is approximately stable under revisits.

A predictive-state signature compares future **learned action-conditional observation distributions**, not latent Euclidean geometry. Two-step signatures cannot reliably distinguish hidden states that require three silent prerequisites, especially when training contained only two. The synthetic depth-three failure is a deliberate adversarial test of exactly this limitation.

**Gates before any native Level-2 attempt:**

1. Improve native model changed-pixel prediction under episode- and initial-layout-held-out splits; report against copy-frame, frame-only, shuffled-history and no-action controls. Native unseen layouts are not available in this archive; do not claim this gate passed.
2. Verify learned cluster states reduce held-out contradictory transition outcomes **without arbitrary fragmentation**, and compare with shuffled labels and a fixed-key-count baseline. Current gate **failed**.
3. Prove enabling Bellman improves task reward or charged action count compared with the same learned representation and same action policy, not just changes trajectories. Current gate **failed**.
4. Test predictive horizons and model-rollout uncertainty, especially depth changes, on synthetic and independent legitimate training layouts before making Level-2 claims. Current two-step generality gate **failed**.
5. Continue diverse Level-1 source collection on allowed families, preserving true SDK reward and exact action ledger; validate terminal predicates across distinct initial layouts when such data exists. Current same-layout evidence is candidate-only.

## 6. Reproduction

The archive includes source modules, precommitted protocol, raw native public frames, policy seed/action metadata, trained native and synthetic PyTorch checkpoints, train-only clusterers, matched ablation trajectories, original N100 source ZIP and 12 offline tests. `README.md` contains full commands. `SHA256SUMS.txt` pins the final files.

**No new Level-2 ARC completion, official benchmark score, private test use, illegal shadow oracle, cluster execution, or claimed breakthrough.**