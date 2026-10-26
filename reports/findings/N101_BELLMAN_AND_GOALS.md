# N101 Bellman Repair and Nine-Family N097B Goal Evidence Audit

**Date:** 2026-10-25  
**Scope:** Offline/source-replay only. **No `vc33` experiment, no N100 cluster access, no policy promotion, no Kaggle submission.**  
**Input provenance:** original user-provided `N100_ACTIVE_FSM_20261025.zip`, SHA-256 `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`; prior `N101B_EVIDENCE_AUDIT_20261025` source, SHA-256 `5b38dbfd0d3d4e61305f8d649bfc99aaf77a2e0a533177d982764e5f3cd6f45f`.

## Decision in one paragraph

The N101B zero-backup ablation was **an implementation failure, not a scientific counterexample to RTA\***. The original Python implementation used rolling action-history keys that usually prevented identical visible states from sharing values, backed up partially observed successors while ignoring unknown legal actions and no-op edges, and did not propagate changed successors to predecessors. `src/n101_bellman_fixed.py` repairs these defects for a **fully observable deterministic observed graph**, with a separately measured non-Markov alias warning. A matched trap test reaches the goal in **4 vs 18 actions** with backups on/off; a 96-task procedural suite yields **79/96 vs 77/96** completions with the only difference being actual Bellman updates. The N097B reward-frame channel is available on **8/9** other training families, but the original strict alignment program recognizes **0/8**; generic geometry/topology features can be extracted from all 8, **yet nonreward endpoints produce similarly convincing signatures**. Thus **neither a native ARC advantage nor a broadly actionable general terminal-goal program is established**.

## 1. Recovered original N100 status

Read `N100_RESULTS_20261025.md` inside `inputs/N100_ACTIVE_FSM_20261025.zip`: N100 is explicitly an **interim package** with three `vc33` query runs and three other-family smoke tests (`ar25`, `cd82`, `s5i5`), not a completed N100 nine-family comparison. On identical `vc33` starting layouts, a seven-action winning word was found and independently replayed at **68 total charged SDK calls per policy seed**, 11 actual resets, 12 membership queries; N098's historical recovery consumed 13 continuous actions. The seven-action word is **not** a seven-call learned controller. No Slurm dependency exists. This audit neither runs N100 nor attempts its unfinished family experiments.

## 2. N101 source-level fault isolation

See recovered source `src/n101_rta_pre_N101B.py`, N101B inherited source `src/n101_rta.py` and replacement `src/n101_bellman_fixed.py`.

| Fault | Original behavior | Repair | Direct test |
| --- | --- | --- | --- |
| Unstable state identity | `_key()` joins the raw-frame hash with an action/outcome rolling-history digest. The *same frame* gets a different node on every recurrent path. | Stable native frame/level hash as observed-graph state; explicitly flag differing outcomes on the same `(frame, action)` as potential latent aliasing. | `test_hash_stable_under_action_history_and_level_sensitive` |
| Broken coverage condition | Default `backup_requires_full_expansion=False`: `min()` uses only *discovered* successors; untried legal choices are omitted and inflated values masquerade as distance. | Back up only if **all legal controls** for this observed state have an outcome. | `test_complete_action_bellman_formula_and_partial_expansion_guard` |
| No-op wrongly deleted | Original backups remove observation self-loops, although a known one-action self-loop has valid Bellman cost `1+V(s)`. | Include sampled self-loops in the Bellman candidate; grow at most one time per state during one closure call. | `test_one_self_loop_updates_at_most_once_per_step`, `test_bellman_includes_observed_self_loop_cost` |
| No reverse propagation | Local updates modify the departing state but do not push revised downstream costs backward through visited predecessors. | Record reverse adjacency and propagate learned cost increases within a bounded, once-per-state update queue. | `test_predecessor_bellman_propagation_when_expansion_is_complete` |
| Greedy scores ignore learned `V(s)` for untried actions | Tested edges use `V(dest)` but untried actions use the raw geometry estimate `h(s)`. Combined with unstable keys, values don't influence decisions. | Choose among observed `1+V(s')` and untried optimistic `1+max(0,V(s)-predicted_gain)-bonus`. | Paired synthetic trap and 96-task changed-trajectory log |
| Terminal failure classified as distance-zero | Original base `observe()` sets value zero at `GAME_OVER` even without an earned level completion. | Restore source geometric estimate when `GAME_OVER` is *not* a native reward/`WIN`. | `test_game_over_without_reward_not_an_estimated_zero_goal` |

**Exact update in the corrected code:** once every legal action of state `s` has an observed deterministic destination, it computes `T(s) = min_a [1 + V(s'_a)]`, including observed self-loops, and applies the standard monotone online learning form `V(s) := max(V(s), T(s))`. The minimum cost is evaluated over **all legal controls**, not just those incidentally tried first. Terminal native success has value zero. Updates propagate backward through the discovered graph.

**Guarantees remain limited.** The geometric starting heuristic is not proven admissible; the visible frame is not a sufficient Markov state for silent locks; a conflict in identical `(frame,action)` successors disables that state's deterministic backup but does not solve the belief-state inference problem. The closed-graph Bellman proof therefore **does not transfer automatically** to native ARC.

### 2.1 Discriminating synthetic witness

State `S` has two legal actions: `greedy` enters `A` (lower *visual* heuristic), and `detour` enters `B`; `A` can only return to `S`, and `B` reaches `G`. Both policies use exactly the same action set, initial heuristic, action prior `{}`, native observation format and 18-action budget.

- **With backups:** `S -> A -> S -> B -> G`, four actions; after observing `A -> S`, `V(A)` changes **1 -> 3**, so `detour` outranks returning to `A`.
- **Backups disabled:** repeatedly picks `S -> A -> S`, misses `G` within **18 actions**.
- `results/bellman_trap_witness.json` contains every decision score, action and value update. No invisible state or oracle path is supplied to the controller.

A 7x7 cyclic-grid negative-control benchmark completes in **20 actions with and without backups** for the default layout. That confirms the graph-key repair can help navigation without itself proving that every use of the updated V table is useful. The causal backtracking trap is the positive proof.

### 2.2 Fixed-policy procedural cross-check

The original N101B procedural environment was reused **unchanged**, with 96 prespecified test specifications (4 layout seeds x 4 prerequisite depths x 2 visibility modes x 3 decoy counts, with its shared source-only calibration). Same 18-action cap throughout. These environments intentionally model control-like locks and are **not ARC games**.

| Controller | Completed / 96 | Mean capped Level-2 actions | Hidden-condition completions / 48 |
| --- | ---: | ---: | ---: |
| N101 original policy | 77 | 9.969 | 36 |
| N101B (silent-repeat heuristic) | **84** | **9.635** | **43** |
| Repaired graph, backups disabled | 77 | 10.271 | 33 |
| **Repaired graph, backups enabled** | **79** | 10.281 | 35 |

- **205 recorded learned-value increases**, **17/96 action traces altered** by enabling the backups.
- Paired repairs: **3 tasks newly solved, 1 task lost**, net +2; some action choices worsen. Do not report this as monotonic dominance.
- Comparing repaired to original N101 yields 6 gains and 4 losses; comparing to N101B yields 5 gains and 10 losses.
- **34 aliased visible-state flags** across the 96 repaired runs indicate that a screenshot-only graph cannot correctly handle every hidden-prerequisite mechanism. Repairing Bellman arithmetic is not a general POMDP solution.

All original plus new tests: **44/44 passed**. Detailed rows in `results/procedural_repair_ablation.json`; cyclic results in `results/grid_bellman_comparison.json`.

## 3. Nine-family terminal-frame generalization

### 3.1 Exact input and provenance

The original N097B source cohort is `ar25`, `cd82`, `g50t`, `lp85`, `ls20`, `m0r0`, `s5i5`, `sc25`, `tu93`, `vc33`. This audit **excludes `vc33`** entirely. `experiments/recover_native_l1.py` replays the already-frozen N093 PUCT Level-1 action traces with original SDK native seed 47 and policy seeds 76,77,78, verifying **every pre/post frame SHA-256**, level counter and reward result. No new policy decisions, new winning attempts, or Level-2 observations are used.

- **27 source attempts**, **518 locally charged SDK calls**, **24 outgoing Level-1 terminal frames** and 3 failed-to-complete `s5i5` sources (50 actions each).
- `experiments/strict_masked_source_replay.py` independently reruns the **exact original** N097B terminal extractor plus B1 source mask on a fresh replay of seed 76 for the nine families. It reproduces all 8 original masked no-goal results (123 source calls) and correctly abstains on `s5i5`. The frozen original record separately includes three policy seeds per family.
- `experiments/strict_unmasked_recheck.py` applies the same original terminal formula **without** the B1 mask to all 24 valid frame sequences; it also accepts 0. This is an extra diagnostic, not a substitute for the exact masked run.

### 3.2 Critical `frame[0]` vs `frame[-2]` distinction

On an actual Level-1 reward transition, the native SDK returns a **frame stack**: animation frames associated with the outgoing Level 1 and the incoming Level-2 start frame. In these archived observations, `frame[-1]` is incoming Level 2 and `frame[-2]` is the *last* outgoing Level-1 frame. `frame[0]` is **not always identical** to `frame[-2]`.

The two differ in `cd82` (50 pixels), `g50t` (49), `sc25` (4) and `tu93` (18); equal in `ar25`, `lp85`, `ls20`, `m0r0`. **Use `frame[-2]`, not unconditionally `frame[0]`.** This is an observed trace fact, not game internals.

### 3.3 Cross-mechanic evidence table

The visual descriptions below are **tentative characterizations of public screenshots**, *not privileged labels of the actual game rules*.

| Family | Observed graphical pattern | Terminal frames / sources | Original N097B strict AST | Example source-only geometric/topological signal | Scientifically supported conclusion |
| --- | --- | ---: | ---: | --- | --- |
| `ar25` | Movable L-shaped motifs, positions and sizes changing | 3/3 | 0 | Colour-11 occupancy 109 -> 79 -> 55, 14 consistent nonreward reductions | Continuous visual progress; no terminal-specific goal theorem |
| `cd82` | White/black blocks repositioned or stacked | 3/3 | 0 | Colour-15 vertical centroid 20.20 -> 32.53 -> 34.73 | Observable position changes; alignment grammar misses relational structure |
| `g50t` | Maze/track-like region and moving markers | 3/3 | 0 | Colour-9 area 119 -> 111 -> 110 | Progress feature survives reward, but geometry is not the `vc33` relation |
| `lp85` | Multi-colour sequence/ring rearrangement | 3/3 | 0 | Colour-11 bbox width 36 -> 12 -> 8; distance to terminal actually 276 -> 288 | Position/ordering candidates; terminal pixel-template progress is **not** monotonic |
| `ls20` | Corridor/region and moving/filling symbols | 3/3 | 0 | Colour-11 area 84 -> 62 -> 60 | Occupancy/shape changes, not accepted as a goal by original grammar |
| `m0r0` | Bilateral coloured shapes, emerging dark filled regions | 3/3 | 0 | Colour-0 area 0 -> 20 -> 22; area/contact topology grow | Strong *filling-like* source progress signal, not a proven sufficient objective |
| `s5i5` | Bars/tokens; original source policy does not win L1 | **0/3** | 0 (no evidence) | No terminal frame; cannot test terminal extraction | **Unavailable evidence**, not extractor failure |
| `sc25` | Grid whose cell colours change | 3/3 | 0 | Colour-9/10 bbox widths contract; last pre->terminal changes only **4 pixels** | Structured grid change exists; no unique reward predicate isolated |
| `tu93` | Complex multi-cell pattern changing along a path | 3/3 | 0 | Colour-0 occupancy 261 -> 288 -> 298; colour-6 area 64 -> 37 -> 36 | Drawing/fill-like geometry gives a progress gradient, not a verified terminal rule |

**What is legitimately generalized?** The *ability to observe the outgoing terminal image* transfers to eight other families with Level-1 completions. The original **unique X-alignment grammar does not**. Geometry, region size, topology (connected regions, contact edges), centroids and symmetry produce descriptive features in all eight; whether they form **actionable, transferable** goal predicates remains unverified.

### 3.4 Falsification: nonreward pseudo-terminal checkpoints

`experiments/generic_goal_audit.py` uses one fixed feature grammar across all games: per-colour pixel area, centroid, bbox, connected components, largest component, interior holes, 4-neighbour perimeter, bilateral mismatch and pairwise contact edges. A candidate is labelled *robust source progress* if its reward-terminal value is a previously unseen extremum, it moves consistently through enough **nonreward** source transitions, and the signed progress agrees with the terminal direction. This is a deliberately weak, exploratory **candidate** criterion, not a goal certificate.

The audit also pretends every eligible **nonreward** checkpoint is a terminal frame and reruns the same detector on the corresponding source prefix. This is a necessary negative control: if a moving/filling feature generates a seemingly novel target at each action, seeing it again at the actual reward does not isolate what *caused* reward.

| Family | Robust source-progress candidates at actual terminal (seed 76) | Maximum candidates at **nonreward** checkpoints |
| --- | ---: | ---: |
| `ar25` | 6 | 16 |
| `cd82` | 8 | 11 |
| `g50t` | 2 | 16 |
| `lp85` | 6 | 27 |
| `ls20` | 12 | 16 |
| `m0r0` | 8 | 14 |
| `sc25` | 4 | 18 |
| `tu93` | 12 | 13 |

All **eight** can generate candidate progress signatures, but **zero** show a greater number of such signatures at reward than the maximum at a nonreward checkpoint. **This is not a formal statistical test or proof that a true causal goal cannot be isolated:** it is a negative control showing this fixed generic grammar cannot *certify a goal* merely because a feature is monotonic and terminal-associated. The policy seeds all share native seed 47 and therefore do not supply independent layout generalization. The last-reward-frame effect can be an animation or post-win update; do not confuse correlation with sufficient/necessary conditions.

## 4. Research implications and next evidence gate

1. **Keep the Bellman repair.** Its backup function demonstrably influences actions, uses full legal-action coverage, and has deterministic unit tests. It is a research baseline, not a native ARC performance claim.
2. **Do not mistake pixels becoming closer to a terminal screenshot for learning a goal.** Reward-associated source progress occurs in moving, filling and grid/logic-like puzzles, but an active goal must bind roles/components and predict discriminating outcomes that fail at ordinary nonreward endpoints.
3. **Do not promote cross-family goal extraction yet.** Before calling a geometry/topology AST "actionable", test whether its predicate is uniquely evaluated in future native observations, whether controlled actions change that predicate, and whether it predicts an actual new level-completion event; control for animation aliases and unrelated UI updates.
4. **Stop the `vc33` loop.** Nothing here needs N100 Slurm recovery, another active-query controller, or a fresh `vc33` demonstration. Replaying previously frozen Level-1 action lists is explicitly not a new policy evaluation.

## 5. Artifact index

- `src/n101_bellman_fixed.py`: independent corrected online graph controller; original N101B behavior preserved in `src/n101_rta.py`, original-pre-N101B in `src/n101_rta_pre_N101B.py`.
- `tests/test_bellman.py`: deterministic causal value-learning tests; `tests/test_goal_evidence.py`: source/terminal evidence and invalid-goal controls.
- `results/bellman_trap_witness.json`: exact causal policy comparison and Bellman value-change evidence.
- `results/procedural_repair_ablation.json`: 96 paired tasks, with individual wins, failures and action-trace changes.
- `results/grid_bellman_comparison.json`: observable grid safety cross-check.
- `results/native_replay_manifest.json` and `results/l1_native_frame_replay.npz`: 518 SHA-verified native source actions and observed pixel frames, **excluding `vc33`**.
- `results/exact_masked_replay.json`: exact original N097B extractor rerun; `results/strict_original_formula_unmasked.json`: independent no-mask diagnostic.
- `results/goal_signature_audit.json`: all 27 source outputs, per-feature values, all per-family negative-control checkpoints; `results/l1_family_panels.png`: readable visualization of public frames (colours mapped for display, not raw palette fidelity).
- `inputs/N100_ACTIVE_FSM_20261025.zip`: unaltered source supplied by user, hash pinned; `bootstrap_inputs.py` securely extracts it before reproducing native replays.

**No native Level-2 improvement, no proven causal winning condition, and no fresh Kaggle score are claimed.**