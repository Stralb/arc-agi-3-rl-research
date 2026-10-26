# N111 — Global Grid Transformations: Exact-Program Synthesis vs Native Execution

**Date:** 2026-10-25  
**Decision:** Do not deploy. Retain the original frozen B1 + N093 PUCT Kaggle submission unchanged.

## Research question

Can a short, whole-observation array program, learned solely from a native Level-1 initial screenshot and its genuinely rewarded outgoing terminal screenshot, generate an executable Level-2 target without rediscovering the puzzle's action mechanics?

**Answer under the tested constraints: no.** Of nine genuine Level-1 rewarded pairs, none is exactly representable by the tested depth-three library. Eight searches fully exhausted their unique reachable states; `lp85` hit the 5,000-state search-expansion cap. No fitted Level-1 program was available to transfer. More fundamentally, ARC-AGI-3 exposes interactive actions, not arbitrary screen-pixel writing; predicting a target grid does not define native input actions that attain it.

## The underlying category error

Static ARC-AGI-1/2 grid transduction is a function from input arrays to output arrays. **ARC-AGI-3 is an interactive environment**. A 64×64 image encodes a momentary screen, often including interactive UI, animation and controls. Native actions are directional/buttons and optionally `ACTION6(x,y)` clicks. The latter accepts coordinates but **no target colour**. It is not `SetPixel(x,y,c)`.

N111 faithfully implements the requested array DSL, but only as a *candidate target predictor*. The proposed subsequent instruction, “click all mismatched pixels until the screen equals the target”, has no general grounding in the actual action interface and therefore was not silently installed into the Kaggle agent.

## Frozen source and data provenance

- **15 original training-split families:** `ar25`, `bp35`, `cn04`, `dc22`, `g50t`, `ka59`, `lf52`, `lp85`, `m0r0`, `re86`, `sb26`, `sp80`, `tn36`, `tu93`, `wa30`.
- One native seed 47, frozen B1 Level-1 policy seed 76, at most 200 charged actions per Level 1; no explicit reset queries and no protected held-out family interaction.
- **912 charged native Level-1 SDK actions** across 15 fresh game instances. **9 genuine Level-1 rewards**. The other six have no terminal-state training pair; they cannot be counted as failed program fits.
- Winning families: `ar25`, `dc22`, `g50t`, `lf52`, `lp85`, `m0r0`, `sp80`, `tn36`, `tu93`.
- Initial screenshot: first actual Level-1 observation. Output: the last outgoing Level-1 screen at native reward (`frame[-2]`), **not** the incoming Level-2 screen (`frame[-1]`). This detail was established in prior N101/N102 reward-stack audits; the current collector verifies the relevant recorded frame hashes.
- Five of nine source/terminal pairs (`ar25`, `g50t`, `lp85`, `m0r0`, `tu93`) independently match the archived N101 observation frames bit-for-bit.
- Frozen source archive SHA-256: `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`.
- Frozen Kaggle notebook SHA-256: `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`.

## Implemented DSL and exact search

The library operates on the **whole 64×64 uint8 observation**; no object parser, bounding-box matching, code-specific dispatch or level-source reconstruction.

1. `Rotate90(k)` with 90/180/270-degree rotation.
2. `Reflect(axis)` with horizontal/vertical reflection.
3. `ColorMap(a,b)` replacing one palette index throughout the entire screen.
4. `FloodFill_Background(c)` filling enclosed modal-background regions with a specified index; modal background selected from the screen border.
5. `Gravity_Shift_Pixels(direction)` stably packing nonbackground pixels to one of four edges along rows/columns.

Colours are selected from those visible in the Level-1 source/target; observing the rewarded target during offline Level-1 program learning is allowed. No Level-2 observations or rewards influence the search program. The grammar semantics are completely specified in `src/n111_dsl.py`, including ambiguous choices of background and packing order. The search is a **FIFO breadth-first search** over unique exact output arrays, retaining the shortest discovered program (up to three operations) and stopping at a maximum 5,000 expanded unique states per rewarded pair. It reports search exhaustion separately from search truncation.

## Measured native Level-1 and synthesis results

| Family | L1 reward? | Native L1 actions | Source → terminal changed pixels | Closest mismatched pixels under searched programs | Exact short program? | Search outcome |
|:--|:--:|--:|--:|--:|:--:|:--|
| `ar25` | Yes | 15 | 189 | 139 | No | Exhausted |
| `bp35` | No | 34 | — | — | N/A | Missing target |
| `cn04` | No | 75 | — | — | N/A | Missing target |
| `dc22` | Yes | 56 | 198 | 98 | No | Exhausted |
| `g50t` | Yes | 17 | 161 | 153 | No | Exhausted |
| `ka59` | No | 100 | — | — | N/A | Missing target |
| `lf52` | Yes | 44 | 92 | 56 | No | Exhausted |
| `lp85` | Yes | 6 | 276 | 228 | No | **Hit state cap** |
| `m0r0` | Yes | 25 | 97 | 47 | No | Exhausted |
| `re86` | No | 100 | — | — | N/A | Missing target |
| `sb26` | No | 200 | — | — | N/A | Missing target |
| `sp80` | Yes | 4 | 729 | 537 | No | Exhausted |
| `tn36` | Yes | 14 | 60 | 42 | No | Exhausted |
| `tu93` | Yes | 22 | 46 | 29 | No | Exhausted |
| `wa30` | No | 200 | — | — | N/A | Missing target |

The closest pixel mismatch is **not** a winning goal, reward prediction or executable plan. Truncation on `lp85` prevents claiming no length-three program exists for that family under this DSL; the other eight exhaust the selected grammar and length bound.

## Native Level-2 action-interface audit

A separate SDK replay executed the *same archived Level-1 actions*, checking every before/after observation hash and outgoing reward-frame hash, and then inspected only the first incoming Level-2 observation. **203 additional charged QA replay actions** are not included in the 912 policy-data collection calls.

| Measurement | Outcome |
|:--|:--|
| Independently replayed Level-1 actions | 203 (all nine winners) |
| Legitimately reached Level-2 observations | 9 |
| `ACTION6` coordinate click legal on first Level-2 observation | 7/9 |
| `ACTION6` unavailable | 2/9 (`g50t`, `tu93`) |
| Exact level-one programs available for Level-2 targets | **0/9** |
| N111 Level-2 execution calls | **0** |
| Level-2 completions attributable to N111 | **Not measured** (no legal grounded program/executor) |

**No native Level-2 improvement is established.** The absence of a learned exact program and of a colour-setting actuator prevent executing the requested diff-click plan. This is not an experiment that tried and failed nine native Level-2 plans; **there were zero such plans**.

A hypothetical one-pixel-per-click canvas would also require 276 and 729 writes for the observed Level-1 source/target pixel diffs of `lp85` and `sp80`, respectively, exceeding the 200-action cap. ARC click effects are not guaranteed one-pixel writes, so this is only a conditional budget diagnostic, not a lower bound on actual SDK moves.

## Interpretive limits and research decision

- No evidence that a *different* longer DSL, a localized canvas transform, or an interactive policy model would necessarily fail. In particular, the present DSL transforms the whole HUD-containing observation, not an inferred canvas crop.
- No direct screen-painting API exists in the tested SDK action grammar; a true executor still needs a learned or known mapping from desired pixel changes to action outcomes.
- Only a single native layout/seed was evaluated; source pairs are not independent examples of broad generalization.
- B1/PUCT remains the only frozen submission candidate with previous native completions. N111 is a **negative offline diagnostic**, not an alternative Kaggle submission and not a claimed leaderboard result.

## Artifacts

- `PROTOCOL.json`: frozen evaluation protocol and split.
- `src/n111_dsl.py`: array DSL, exact-search implementation, target diff diagnostic (explicitly not an SDK actuator).
- `experiments/collect_training_l1.py`: native source-only dataset collector.
- `experiments/evaluate_programs.py`: exact bounded BFS and per-family accounting.
- `experiments/audit_level2_interface.py`: independent native replay and first Level-2 legal action audit.
- `results/training_level1_native.npz` and `results/training_level1_manifest.json`: exact source/target pixels, charged action traces and frame hashes.
- `results/dsl_bfs_results.json` and `results/per_family.csv`: complete search results, including best approximate mismatch and capping information.
- `results/level2_interface_audit.json`: replay provenance, legal actions and nonexecution of ungroundable pixel-write commands.
- `tests/test_dsl.py`: controlled positive and negative DSL/solver tests.
- `verify_results.py`, `SHA256SUMS.txt`: reproducibility and integrity verification.
- `inputs/N100_ACTIVE_FSM_20261025.zip`, `inputs/frozen_submission.ipynb`: original unmodified sources.