# N109 - Deictic Action Grounding: Ten-Family Native Evaluation

**Experiment date:** 2026-10-25  
**Disposition:** Does not pass the Level-2 transfer gate; preserve frozen B1/N093 submission.

## Research question

Does encoding Level-1 coordinate clicks relative to the nearest native-visible N106 connected component permit replay of the Level-1 winning action sequence in a changed Level-2 scene, without an inferred symbolic O-DSL action grammar or an additional exploration policy?

**Result:** No additional native Level-2 completion, and zero transferred coordinate clicks executed. All three families with a winning Level-1 coordinate-click trajectory failed the first Level-2 deictic object match. The only Level-2 success in the frozen controller was the historically exposed `vc33` run.

## Locked protocol and comparison

- Ten already exposed N093 development examples (`ar25`, `cd82`, `g50t`, `lp85`, `ls20`, `m0r0`, `s5i5`, `sc25`, `tu93`, `vc33`). **`vc33` was historically in a protected test split and has already been exposed by prior research. This is not an untouched test-set evaluation.**
- One fixed native SDK seed **47**, policy seed **76**, and at most **200 charged native actions per level**. Same starting layout across arms, no claim of independent trials or layout generalization.
- Frozen core: N093 B1 (Level 1) and pretrained PUCT on Level 2+; no weights or baseline hyperparameters changed.
- **Frozen baseline:** unchanged B1+PUCT for Level 1 and Level 2.
- **Absolute replay control:** B1 solves Level 1; Level 2 replays its Level-1 native actions at the same x/y and the same key indices, no exploration or RL fallback.
- **N109 deictic:** B1 solves Level 1 and logs each click against the nearest uniquely identified centroid from the *pre-action image*. Object signature = exact component **colour, area (scale), reduced bounding-box aspect ratio, and N106 type**. The offset is stored as an exact floating residual (x - cx, y - cy). Level 2 resolves each click on the **current** frame to the *only* component with the same signature. Ambiguity, missing signatures, offscreen clicks and illegal actions cause abstention. Global/non-coordinate actions are replayed unchanged. The winning Level-1 sequence is replayed once; its exhaustion ends the test (no additional RL search).
- All action requests use the native SDK's legal action interface. No source-game physics, hidden state, shadow/oracle, game-ID action dispatch, privileged observation, reset probe, learned grammar, external model, or hindsight-corrected click.

## Measured performance: 30 native SDK episodes

| Measure | Frozen N093 | Absolute replay | N109 deictic replay |
|---|---:|---:|---:|
| Level-1 completed | **9/10** | **9/10** | **9/10** |
| Level-2 completed | **1/10** | 0/10 | 0/10 |
| Charged native SDK actions (both levels) | **1,116** | 302 | 276 |
| Charged Level-2 actions | 940 | 126 | 100 |
| Successfully relocated Level-2 clicks | n/a | n/a | **0** |
| Extra successful non-`vc33` Level-2 completions | 0 | 0 | **0** |

**Action-count caveat:** Replay arms use fewer actions because they stop at log exhaustion or the first failed anchor, not because they are more efficient solvers. No successful deictic replay is established.

## Where the proposal fails

From the frozen winning Level-1 traces:

- `lp85`: six coordinate clicks, all anchored in source, first Level-2 click **unmatched** under the exact colour/area/aspect/type signature.
- `sc25`: five coordinate clicks, four with duplicate same-signature source objects; first Level-2 click **ambiguous**, with multiple matches.
- `vc33`: three coordinate clicks, all with duplicate source signatures; first Level-2 click **ambiguous**. This family was previously exposed, so failure or success here is not evidence of generalization.
- `s5i5`: 50 coordinate clicks, but **no Level-1 completion**; no Level-2 test is possible.
- `ar25`, `cd82`, `g50t`, `ls20`, `m0r0`, `tu93`: Level-1 wins have **no coordinate-click actions**. N109 therefore replays the same key presses, using 100 charged Level-2 actions in aggregate, without reward.

Among the **14** Level-1 coordinate clicks in the three successful click-using families, the N106 parser found a nearest component to every click, and every click fell on that component. However, **eight** clicks had a source component signature shared with other visible objects. This is a fundamental correspondence ambiguity even before the Level-2 relocation step.

## Why the mathematical claim does not follow

1. **Nearest object is not a verified interaction target.** Even when the click lies in the nearest component, it could activate a global control, select a tool, set an internal mode, or trigger another object.
2. **A shared colour/scale/aspect signature does not uniquely identify an object.** Duplicate parts may be indistinguishable. Conversely, recolouring or resizing across levels destroys the exact signature.
3. **Relative position corrects translation, not changed program semantics.** The Level-2 rule can require additional clicks, new controls or different action order; replaying Level-1 actions cannot establish the solution by geometry alone.
4. **Static toolbar behaviour is a hypothesis, not a given.** Level changes may reconfigure glyphs, change colours or remap controls. The native match failure in all three winning click families disproves *successful deployment of this exact matcher*, not the existence of a usable relative reference in principle.
5. **No reduction in environment action cost is entailed.** Even if deictic replay succeeds, every emitted action remains charged, and the log has a fixed length independent of Level-2 complexity.

## Correctness and controlled positive test

The synthetic test draws an arbitrary solid shape at one location, records a within-object click, and moves the shape by an integer offset. N109 resolves the identical relative click in the moved shape without using its original coordinate. Tests also verify stable absolute replay, exact native ACTION7/ACTION6 legal masking, missing object rejection, same-signature duplicates, colour mismatches, no foreground, equidistant source tie, and non-coordinate action handling.

**That control shows the coordinate transform is implemented correctly under its assumptions. It does not imply successful native grounding.**

## Independent replay and preservation

- 30 acting-time runs contain **1,694 charged native actions** in total; the frozen arm contributes 1,116 of those.
- After deduplicating physical trajectories, an independent SDK replay verified **22 distinct action sequences / 1,394 QA native actions** with matching before-frame hashes, after-frame hashes, level increments, rewards and legal actions. QA calls are not included in policy cost and are not used for action selection.
- All **1,116 frozen baseline actions** matched the archived original N107 baseline reference exactly, with per-step frame and reward hash parity.
- The original N100 input archive is included unmodified; SHA-256 `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`.
- Frozen Kaggle notebook is included unmodified; SHA-256 `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`.

## Decision

**Do not deploy N109 and do not change `submission.ipynb`.** The successful synthetic relocation test is outweighed by a failed native grounding gate (0 relocated Level-2 clicks, 0 extra Level-2 completions). The work is a falsifiable negative transfer experiment, not a method that breaks ARC's Level-2 barrier or a claim about Kaggle leaderboard score.