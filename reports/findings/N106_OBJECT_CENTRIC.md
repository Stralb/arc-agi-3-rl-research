# N106 — Object-Centric Inverse Graphics: Evidence and Decision

25 October 2026 · Public development-family data only · no cluster · no `vc33` · no hidden evaluation

## Research decision: retain compiler as an experimental component; do not promote

**Do not replace `submission.py` or `submission.ipynb` with N106.** A deterministic connected-component parser, restricted object DSL, observed-action inverse compiler, two-step guarded executor and B1+N093 PUCT bridge have been implemented and tested. But the required evidence for translating proposed object transformations into new native Level-2 successes is absent. There are **zero new Level-2 wins** and **zero grounded DSL actions** in the five-pair SDK smoke. This is an abstention success, not gameplay improvement.

The earlier N094 source already tried simple object-relative symbolic policy induction, abstained on all evaluated Level-2 actions, and got no new rewards. N106 tests the different question of **inverse native action grounding** with exact transition evidence rather than fitting a short decision tree.

## Key identifiability distinction

A visual DSL renderer computes a desired change `x' = ODSL(x, goal)`. It cannot generally compute the correct native action sequence unless a valid, sufficiently general inverse dynamics map `a* = T^{-1}(x, x')` is learned or supplied. Two native games can present **identical public pixels and legal controls** but have different mappings from the buttons to movement. A fixed geometry-only compiler would choose the same action for both and must be wrong for at least one. No amount of connected-components parsing proves which physical button performs the desired transform.

N106 therefore distinguishes:

1. **Parsing**: produce the object graph from a public `64×64` palette observation; color-homogeneous four-connected components, bounding boxes, centroids, line/solid/hollow classes, enclosed interiors, contact and containment edges. Background is estimated as the modal color, not a privileged game constant.
2. **Pure image semantics**: `Translate(dx,dy)`, `Recolor(c)`, `FloodFill(c)` render counterfactual **desired pixels**, not engine state. Translation refuses overlap/out-of-bounds; filling refuses to overwrite existing foreground objects. Scale is deliberately excluded from the two-primitives deadline scope.
3. **Grounded actuation**: learn an action-to-operation mapping only from Level-1 **charged, legal, observed** actions. Never reuse absolute Level-1 ACTION6 coordinates; learn the click offset **within** the observed object and re-anchor it to the current object. Reject ambiguous effect, ungrounded action, illegal native control, out-of-vocabulary goal, or duplicate indistinguishable target geometry.
4. **Guarded execution**: consume actual SDK actions one at a time; compare the actual outgoing frame to the purely rendered expected frame after each click and abort remaining macro steps on mismatch. The native Level advancement field, not predicted image similarity, defines success.
5. **Fallback**: only a uniquely evidenced source-terminal primitive may nominate a provisional cross-level program. Otherwise the original B1/PUCT chooses, updates empirical Q and remains unchanged. A terminal primitive alone is still correlation, not proof of reward necessity.

## Primary frozen native Level-1 transition audit

N103's frozen legal SDK dataset contains **1,848 charged source transitions** in **60 Level-1 episodes**, **53 rewards**, and five development families: `ar25`, `g50t`, `lp85`, `m0r0`, `tu93`. Exactly **1,570** transitions change at least one palette pixel; 278 are visually silent. The 60 episodes were collected at policy seeds 276–279 with different exploration levels. All native seeds share initial screenshots within each family, so **no unseen-layout generalization** is shown.

| Feature audit | Native count |
|---|---:|
| Exactly a single full-frame object translation | 82 |
| Exactly a single full-frame object recolouring | 2 |
| Exactly a single full-frame flood fill | 0 |
| Visible native transitions expressible as exactly one full-frame DSL primitive | **84 / 1,570 = 5.35%** |
| Rewarded source transitions expressible as exactly one such primitive | **0 / 53** |
| Other nonsilent full-frame transitions: multiple changes, animation, occlusions, or unrepresented physics | 1,486 |

The strict parser identifies only an *observed visual change*. It cannot identify the action that caused a change or a winning goal unless supporting evidence exists.

### Overly permissive matching negative control

If an object can count as translated/recoloured **even when unrelated screen regions change**, local appearance changes are found on **1,319/1,848** native steps and **52/53** reward transitions. However, a coarse source-shape/colour-role/translation signature of these local changes is **not new at reward** in any of the 53 source winning sequences. No completed family has a signature shared by its source terminal transitions **and absent from its sampled nonreward transitions**. Source `m0r0`'s apparent `Recolor:background:solid:a4` signature also appears on 241 nonreward transitions. These 'recolour' labels may describe erasure/occlusion/animation rather than a real recolour operation. High local detection coverage must not be mistaken for high goal precision.

### Action-grounding held-out diagnostic

Fit on *complete source episodes* for policy seeds 276,277,278; evaluate on held-out policy seed 279 (same native layout, not independent game transfer). True desired test operations are recovered by comparing held-out **after** frames — **diagnostic hindsight only**, never available to an acting policy. Of **22** exactly one-primitive held-out events, neither the strict global-effect compiler nor the context-conditioned object-shape compiler has a high-confidence unambiguous rule: **0/22 safe native compilations**. An intentionally invalid optimistic control that ignores nonmatching and silent outcomes claims 18/22 possible operations; this does **not** establish 18 executable actions.

Why even `m0r0` fails safe translation grounding: among 77 strict observations of `ACTION1` moving a same-colour 5×5 square upward by five pixels, the screen contains **two geometrically indistinguishable squares**. The moving one is the leftmost in 35 observations and the rightmost in 42; a keypress does not specify its target in the current object graph. Context conditioning by target shape therefore cannot license `Translate(Square_A, Up)` in a fresh situation. This is a specific unsupported object-target binding, not evidence that every symbolic approach is impossible.

## Native SDK integration check — public training only

Five family × policy-seed-76 **matched pairs** (`ar25`,`g50t`,`lp85`,`m0r0`,`tu93`), original frozen pretrained PUCT, native seed 47, source Level-1 cap 200 and Level-2 smoke cap 100. The same N093 model and Bellman learner are used on both arms; bridge adds object parsing and a fail-closed compiler only.

- **10 native episodes, 1,070 charged SDK actions total, zero explicit native RESET**.
- All five pairs have byte-identical sequences of actions, public frame hashes and native reward events.
- All ten episodes complete Level 1; **0 Level-2 wins** in either arm under the 100-action smoke limit.
- Every bridge reports `terminal_not_one_exact_primitive`, executes **zero compiler actions** and falls back to frozen B1/PUCT.
- This is **not** a full matched 200-action Level-2 experiment; no advantage is claimed.

## What works, what fails

**Established:** the deterministic parser and renderer work on unit examples; observed source actions can ground a native mapping in controlled synthetic settings; two or more individually evidenced translations compile to a bounded action sequence; actual postconditions can halt on a false physics prediction; B1/PUCT parity and native level accounting hold when compiler abstains.

**Not established:** a causal source reward predicate; transferable inverse control map across different physics; reliable selection of object targets among identical components; independent layout generalization; a new native ARC Level-2/3 completion; any Kaggle leaderboard gain. Source data cannot distinguish which of two otherwise identical target objects is selected by a global action when the selection changes silently.

The proposal that RL is *mathematically the wrong paradigm* or that inverse graphics *guarantees a solution* is stronger than the data warrant. Symbolic programs, action-conditioned models and RL can be components in a solver; each still needs grounded transition and reward evidence.

## Decision and upgrade gate

Keep the frozen N093 competition notebook. Do **not** replace it with the new O-DSL branch. A future upgrade requires (i) successful native action-to-object binding on held-out transitions, including new shapes; (ii) a terminal relational condition that survives nonreward controls; (iii) a valid online object-target grounding; and (iv) at least one additional Level-2/3 **native reward event** in a paired 200-action-per-level development test without test-family hindsight, resets, or shadow oracles. Absent these, a compiler can at most generate plausible pixels, not executable game solutions.

Full machine-readable evidence and commands are in `results/`, `README.md`, `PROTOCOL.json`, and source files. No official Kaggle submission or leaderboard score was obtained in N106.