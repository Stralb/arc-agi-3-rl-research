# N108 — Runtime Action-Grammar Calibration: Native Evidence

**Date:** 2026-10-25  
**Disposition:** Negative native result. **Do not replace the frozen Kaggle `submission.ipynb`.**

## Research question

Can a small, legal, Level-1 calibration budget identify the interaction grammar needed to translate N107's object-centric options into real Level-2 native actions, and thereby solve a non-`vc33` Level 2 without random search?

**Measured answer:** Not with the tested two-click UI-palette/canvas grammar and the available real SDK observations. N108 executed **zero** grounded Level-2 options, matched the frozen policy's completed levels, and used **32 more** native actions in total.

## Frozen experiment protocol

- Ten **historically exposed N093 development families**: `ar25`, `cd82`, `g50t`, `lp85`, `ls20`, `m0r0`, `s5i5`, `sc25`, `tu93`, `vc33`; these are NOT ten untouched training examples. In particular `vc33` has previously been exposed as a protected test family. This suite is suitable only for a retrospective development comparison.
- Original frozen B1 Q-learner and N093 pretrained PUCT, policy seed **76**, native SDK seed **47**; deterministic single layout; one scenario per family, not independent seeds/configurations.
- 200 **charged SDK actions per level**, stop after Level 2 completes or the native episode/budget stops; no explicit RESET calls; no off-policy SDK probes, LLMs/VLMs, privileged game state, source-game introspection in policy, or reward fabrication.
- N108 Level-1 calibration: at most four two-click pairs (**eight native actions**), choosing potential small peripheral UI components and larger canvas objects using the visible 64×64 N106 component parser. ACTION6 availability is mandatory. Click coordinates are derived from the current image, not transferred from source-game absolute coordinates.
- The first UI click must leave the rest of the canvas nearly unchanged, permitting small UI highlighting. The second click must produce a unique **exact one-object** N106 Translate/Recolor/FloodFill effect. A candidate grammar requires at least two distinct before-canvas frame hashes with a consistent UI role, target type, action effect and no contradictory observation.
- Only licensed pairs may enter the SMDP option execution queue; B1/PUCT handles unsupported actions, and its ordinary native Bellman updates remain active. N107's meta-Q is retained across level transitions. No unexecuted option receives a fake reward. Native rewards are obtained only from increases in `levels_completed`.

## Results — 20 native A/B episodes

| Metric | Frozen B1 + N093 PUCT | N108 |
|---|---:|---:|
| Level-1 completions | **9/10** | **9/10** |
| Level-2 completions | **1/10** | **1/10** |
| Non-`vc33` Level-2 completions | **0** | **0** |
| Charged native SDK actions | **1,116** | **1,148** |
| Level-1 calibration actions | 0 | **42** |
| Completed UI/canvas calibration pairs | — | **18** |
| Exact clicked-target transformations recovered | — | **0** |
| Provisional grammar rules | — | **0** |
| Licensed and executable Level-2 rules | — | **0** |
| Executed native Level-2 option actions | — | **0** |
| Native SMDP option Q updates | — | **0** |
| Native rewarded SMDP option updates | — | **0** |
| SDK reset probes | **0** | **0** |

The only Level-2 win is the previously exposed `vc33` case, common to both arms. Total additional action cost is **32** (rather than 42) because extra probes can replace ordinary policy actions or hit existing episode termination/caps.

### Family detail

| Family | Legal ACTION6 at start | Calibration clicks | Completed pairs | Exact primitives | New Level-2 wins |
|---|---|---:|---:|---:|---:|
| ar25 | No | 0 | 0 | 0 | 0 |
| cd82 | Yes | 6 | 2 | 0 | 0 |
| g50t | No | 0 | 0 | 0 | 0 |
| lp85 | Yes | 8 | 4 | 0 | 0 |
| ls20 | No | 0 | 0 | 0 | 0 |
| m0r0 | Yes | 8 | 4 | 0 | 0 |
| s5i5 | Yes | 8 | 4 | 0 | 0 |
| sc25 | Yes | 8 | 4 | 0 | 0 |
| tu93 | No | 0 | 0 | 0 | 0 |
| vc33 | Yes | 4 | 0 | 0 | 0 |

The 18 complete pairs failed because:
- **9** were visually silent after the canvas click (`lp85` 4, `m0r0` 1, `sc25` 4).
- **5** changed the image in ways not explainable by a unique exact single-object primitive (`cd82` 2, `m0r0` 3).
- **4** had an ambiguous canvas object under component topology (`s5i5` 4).
- There were **6** aborts after the UI click changed parts of the canvas outside the local UI neighborhood (`cd82` 2, `vc33` 4).

These categories total 18 completed pairs plus 6 aborted probes; the remaining probe actions are accounted for as first clicks in those aborts.

## Passive control — 60 frozen N103 Level-1 episodes, five families

Instead of issuing new actions, a separate analysis scanned N103's **1,848** original charged Level-1 transitions, grouped by episode (not random individual steps):

- 111 adjacent ACTION6/ACTION6 pairs; 12 had a candidate peripheral first click with local/no visual effect.
- All 12 eligible disjoint pairs failed the exact target primitive check.
- **0** candidate grammar rules; **0** licensed rules.

This is additional negative *observational* evidence, not a new native win or an independent hidden-layout benchmark. `results/passive_five_families.json` contains the exact denominator and reasons.

## Mechanism controls and limitations

1. **Positive synthetic compiler control:** Two genuinely distinct source frames with an exact two-action recolouring effect can license one pair under `min_support=2`; the compiler re-localizes both palette and canvas coordinates in a differently positioned and differently coloured test frame. The SMDP integration test verifies an executed two-click option's duration-two Bellman reward update and meta-Q retention. **These are controlled unit demonstrations, not ARC completions.**
2. **No causality from an action sequence alone:** A passive UI click followed by a target click can appear to establish a "palette -> target" rule even if the target click alone would have had exactly the same effect. Without an intervention/control, the observed pair is only an association. This is tested explicitly.
3. **The static-UI hypothesis is unverified:** Perimeter/shape grouping yields *candidate* interface glyphs. The suite contains games without coordinate clicks and objects that change when probed. Four families have no legal ACTION6 at Level 1, so the proposed UI-click grammar does not cover them at all.
4. **Strict effect grammar is low-recall by design:** Many real ARC effects involve animation, multiple objects, internal mode changes and delayed effects; a single exact N106 object transform rejects them. Zero licensed rules is evidence against this *specific* compiler and probing schedule, not proof that no symbolic grounding is possible.
5. **No independent Level-2 generalization:** Same source seed/layout, previously exposed families, one policy seed, no fresh held-out native configurations, and no Kaggle submission. No claim is made that this is a mathematical upper bound of ARC algorithms.

## Independent replay and source integrity

A fresh real SDK replay of all recorded **unique physical action/observation trajectories**, ignoring controller-side mode labels, verified **16 unique trajectories and 1,751 charged native SDK actions**. **Four** of the 20 episodes duplicate another arm's physical trace. Each replay matched the native before-frame SHA, after-frame SHA, legal action, reward and level count. There were **zero mismatches**. See `results/replay_validation.json`.

- Original N100 input SHA-256: `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`.
- Frozen Kaggle notebook SHA-256: `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`.
- N108 standalone tests: **19/19 passed**. Checksums and clean extraction are part of release verification.

## Decision

**Do not deploy N108.** The existing frozen B1+N093 PUCT notebook remains unmodified. The next improvement, if attempted, would need observed **multi-action success conditions and matched causal controls** rather than more unsupervised guesses about which coloured peripheral rectangles are palettes. No additional native Level-2 completions were achieved.