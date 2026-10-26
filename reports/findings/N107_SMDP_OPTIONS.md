# N107 — SMDP Meta-RL over Object-Centric Options: Evidence Report

Date: 2026-10-25. **Research-only; do not replace the frozen Kaggle notebook.**

## Research question

Can five visually invariant, object-centric options learned through native Level 1 provide a transferable SMDP action-value abstraction that solves a **non-`vc33` Level 2** without blind raw-click exploration?

**Answer from the current experiment: no.** A source-grounded intra-option controller cannot execute any of those options natively, so it cannot earn option-level native rewards or transfer learned meta-Q to Level 2. This is a failure of the strict grounding gate, not a proof that all options-based RL is impossible.

## Architecture implemented

1. N106 four-connected, 64×64 object parser with foreground components, hole/bounding-box/shape metadata and modal-background approximation.
2. Five deterministic high-level options: `Fill_Hollow_With_Border_Color`, `Recolor_Small_Outlier_To_Majority`, `Translate_To_Nearest_Same_Color`, `Translate_Toward_Row_Alignment`, `Recolor_Small_Outlier_To_Background`. Translation can request a path of up to eight native steps. Goals are **hypotheses**, not known terminal conditions.
3. The original N106 `NativeCompiler` serves as a **strict** intra-option action model. It requires consistent, distinct observed Level-1 visual transitions for the same native effect. Its guarded executor compares the SDK's actual outgoing frame with the predicted state **after each charged action** and stops on disagreement. No engine code is inspected for acting and no simulated SDK probe determines the chosen action.
4. A separate `MetaQ` updates actual executed **option durations** with the semi-Markov return:

   `Q(s,o) <- Q(s,o) + alpha [sum_{i=0}^{tau-1}(gamma^i * r_{t+i}) + 1[not terminal] gamma^tau max_o' Q(s',o') - Q(s,o)]`.

   `gamma=0.985`, `alpha=0.45`; the new meta-Q initial value is `0.5`. B1's frozen **native-action** Q initialization `1.0` and its Bellman updates remain unchanged. A coarse colour- and coordinate-invariant object signature keys local meta values, backed by a separate **global per-option value**. Neither abstraction is asserted to be Markov or bisimulation-valid.
5. Meta-Q is **not cleared on level transition**; B1's original native-pixel nodes *are* cleared, for the original B1 Bellman logic to remain valid. B1's pretrained PUCT logits are over **native actions**, so they are **not** reused as fictitious option logits; candidate option exploration uses an explicitly uniform bonus. B1/PUCT remains available as source bootstrap and fail-closed fallback.

### Crucial difference from the literal request

A rejected option has **zero native action duration**. The requested negative native-reward Bellman transition would be imaginary and ill-defined as an SMDP step. N107 records and down-ranks its rejection in selection counters instead; it **does not** record fake environment penalties or credit a B1 fallback action to an unexecuted option. This is necessary to keep the learning signal faithful to the SDK.

## Native experiment — 10 previously exposed N093 development families

- Families: `ar25`, `cd82`, `g50t`, `lp85`, `ls20`, `m0r0`, `s5i5`, `sc25`, `tu93`, `vc33`.
- One policy seed **76**, native configuration seed **47**, **200 charged SDK actions maximum per level**. Stop after the second level advances or when the game ends/budget is exhausted. No explicit SDK RESET action, oracle, LLM/VLM, hidden transition state, or test-family observations used for decisions.
- Matched comparison: **20 native episodes** (10 families × frozen baseline and experimental N107).

| Measured outcome | Frozen B1 + N093 pretrained PUCT | N107 SMDP option hybrid |
|---|---:|---:|
| Native Level-1 completions | 9/10 | 9/10 |
| Native Level-2 completions | 1/10 | 1/10 |
| Level-2 wins on non-`vc33` families | **0** | **0** |
| Charged SDK actions | **1,116** | **1,116** |
| Executed compiled option actions | n/a | **0** |
| Executed SMDP option updates | n/a | **0** |
| Reward-bearing option Q updates | n/a | **0** |
| Level-1 action/frame parity | reference | **10/10** |

All 10 complete action-and-observation trajectories (not only Level 1) match the frozen control. In the experiment N106's strict compiler never authorized an option; the experimental arm therefore used only the frozen B1/PUCT policy. Its meta-Q remained at initial values; **native Level-1 wins credited no option**, which is the correct attribution.

**Independent provenance:** One fresh real-SDK replay was performed for each of the ten distinct matched family action traces: **1,116/1,116** charged actions reproduced the frozen pre-/post-frame hashes, level counts, legal actions and rewards. The two policy arms already share those traces; this is **ten unique replayed sequences**, not twenty independent scenarios. Counting the original A/B runs plus independent replay gives 3,348 SDK steps. No uncharged test-time simulator lookahead was used.

### Comparability limit

The original N093 report used 200 *total* actions per game, three policy seeds and a fixed native layout. N107's paired experiment instead uses a cap of 200 **per level**, one policy seed, and the same fixed layout. **Only matched arms in this new study should be compared directly**; do not compare its total action denominator to N093's previously published 3-seed totals. `vc33` was already known/exposed and is not evidence of unseen-family transfer. The other N093 families include validation names from earlier projects and should likewise not be re-labelled untouched test data.

## Mechanism-positive *synthetic* control

A distinct and fully disclosed two-level toy makes ACTION1 translate a specific small object downward. Two **synthetic, observed** before/action/after transitions calibrate the *same* N106 compiler. Two separately positioned and recoloured scenes require four downward clicks to align the movable object with a larger anchor.

- The first Level's four-click `Translate_Toward_Row_Alignment` option executes and receives the synthetic binary terminal reward on click 4; the second Level uses different colours and positions with **no additional calibration** and likewise executes four clicks.
- Both options make genuine SMDP updates with `tau=4`, observed toy rewards `[0,0,0,1]`, target `gamma^3=0.955671625` and global option Q values `0.500000 -> 0.705052 -> 0.817831`.
- The learned meta values persist into Level 2, while the separate B1 native-state nodes clear.
- This proves the **implemented machinery** can compile and credit an option when the action model is already known. It is **not a native ARC win**, not evidence of novel-physics transfer, and not evidence of net advantage over B1 on that toy. The calibrated dynamics are given by a toy environment, not learned from N093's real Level-1 ledger.

## Scientific interpretation

1. **SMDP is a valid temporal abstraction, not a free action compiler.** An abstract goal such as “fill the hollow region” does not supply its own native policy. The strict N106 source says exactly that the mapping is missing.
2. **The unlearned-table transfer is vacuous.** Keeping `meta_q` across levels is implemented and unit-tested, but in the native evaluation no grounded option executed, so no meta-Q value was learned from native rewards.
3. **Colour/coordinate invariance is not causal dynamics invariance.** Reusing an abstract state signature and global option value in a new level is a candidate inductive bias, not a proof the option still works; the next level can have different controls or hidden prerequisites.
4. **No misleading pseudo-reward.** Assigning a negative environment reward to an unexecuted option would silently replace the native reward process with shaping; assigning the native L1 reward to the last *fallback* click as if it came from an option is false provenance.
5. **No promotion.** N107 adds useful, tested SMDP code but **zero native policy changes and zero new Level-2 completions**. The frozen `submission.ipynb` remains the correct deployment baseline until a matched, prospective real SDK improvement can be demonstrated.

## Verification

- **24/24** automated deterministic tests; parser/option grammar, exact compiler, 4-step guarded execution, SMDP discount, native-only reward, zero-duration rejection, fallback credit isolation, and retained meta values across recoloured layouts.
- Native 10-family matched A/B source results: `results/native_ten_families.json`.
- Real SDK 10 unique trace replays: `results/replay_validation.json`.
- Synthetic 2-level executable option experiment: `results/synthetic_transfer.json`.
- Original N100 source ZIP is included unmodified under `inputs/`.
- No hidden Kaggle run and no remote competition submission performed.