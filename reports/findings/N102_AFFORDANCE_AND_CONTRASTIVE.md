# N102 — Affordance-Augmented Search and Contrastive Goal Extraction

**Research date:** 2026-10-25  
**Status:** Offline hypothesis test completed. **Do not promote to a native ARC policy.**  
**Scope:** No cluster jobs, no new vc33 experiment, no Level-2 ARC policy search, no oracle/shadow simulator, no reset membership queries. The only native SDK calls in this N102 package replay **123 previously recorded Level-1 actions** on the other eight winning training families to verify reward-frame ordering. All N102 search-controller comparisons use disclosed synthetic test fixtures.

## Executive decision

N102's two proposed mechanisms are **not verified as solutions** to the bottlenecks. A paid-action, tri-state estimated affordance signature yields 86/96 completions on the inherited synthetic benchmark versus 84/96 for N101B, but underperforms on the hidden-lock subset (41/48 versus 43/48). Its Bellman backups produce **zero action-trace differences** in 96 no-invalidation cases. Invalidation increases action changes but reduces completion to 78/96, with backups causing **ten losses and zero gains** relative to its matched backup-disabled variant. The strict contrastive terminal predicate grammar finds at least one new first-true candidate at 21/24 archived rewarded Level-1 transitions but also at 156/344 nonreward transitions (45.35% false-positive rate under this diagnostic). The original three policy seeds mostly replay duplicate action trajectories; the positive candidates are not independently validated goals.

## 1. Source provenance and indexing check

- User-supplied **`N100_ACTIVE_FSM_20261025.zip`** is included unaltered in `inputs/`, with SHA-256 `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`.
- Archived action/observation dataset `inputs/l1_native_frame_replay.npz` and `inputs/native_replay_manifest.json` were copied from the previous N101/N097B SHA-verified native source replay. The N102 contrastive analysis **does not query the SDK** for counterfactual worlds.
- An independently rerunnable test, `experiments/check_frame_stack.py`, executes only N093's originally recorded seed-76 Level-1 actions on **eight non-vc33 winning families**, checking each SDK pre- and post-action frame hash against the N093 record, plus the last pre-action and outgoing terminal hashes against the previous audit. Its 123 native SDK actions are replay/verification expenses, **not** an agent's new successes.
- Among the nine other N097B source families, `s5i5` never earned a source Level-1 reward within its archived 50-action attempts and therefore has no positive terminal sample. The eight completed families are `ar25`, `cd82`, `g50t`, `lp85`, `ls20`, `m0r0`, `sc25`, `tu93`.

### 1.1 `frame[-3]` fails as a pre-reward image

| Family | Reward-response frame count (seed 76) | `frame[-3]` valid? | `frame[-3]` equals real pre-action frame? | Difference from real pre-action frame |
| --- | ---: | --- | --- | ---: |
| ar25 | 3 | yes | **no** | 105 pixels |
| cd82 | 16 | yes | **no** | 91 pixels |
| g50t | 9 | yes | **no** | 49 pixels |
| lp85 | 2 | **no** | — | — |
| ls20 | 2 | **no** | — | — |
| m0r0 | 2 | **no** | — | — |
| sc25 | 5 | yes | **no** | 4 pixels |
| tu93 | 9 | yes | **no** | 19 pixels |

For these native replays, the **last outgoing Level-1 reward image is `reward_result.frame[-2]`**, while the **pre-action image must come from the prior SDK observation** stored before the rewarded action. `frame[-3]` is commonly an animation frame, or nonexistent. The indexing rule must be verified for other SDK response variants and is not an unconditional API theorem.

## 2. N102 Affordance-Mask Key: design and evaluation

### 2.1 What can be measured

State identity is `Hash(public-frame-and-level, sorted-current-legal-actions, observed-action-effect-vector)` using a three-valued vector:

- `?`: Not measured recently for this source screenshot/action.
- `0`: The most recent **executed** instance of this action from this source screenshot changed zero pixels.
- `1`: The most recent **executed** instance of this action from this source screenshot changed at least one pixel.

The vector is **not** a free sensor, not a prediction of what actions can currently do, and not a validated sufficient-state statistic. `AffordanceLedger.record` requires an action belonging to the public legal-action set, then compares the actual before/after public frames. One real execution buys at most one observed entry. Untried entries remain `?`. The same frame with identical measured vector produces an identical state key across action-order and history permutations. No source-code state, game ID, hidden mode, or oracle effects enter the controller.

Two treatments:

1. `n102_no_invalidate`: retain last measured effect labels when silent actions occur, acknowledging possible stale status.
2. `n102_invalidate`: after a visually silent action, invalidate old measurements for **other actions** on the identical frame, because silent actions might alter their efficacy; mark them unknown, never automatically set them True.

### 2.2 Matched 96-task synthetic results

Four independent layout replicates, four unlock depths, two visibility settings, three decoy levels; 96 matched source-only calibrated, no-reset environments, each with a strict 18-action Level-2 limit. All family layouts are **synthetic test doubles** modeling buttons/locks, not official ARC game observations. Metrics use actual executed action counts; no hidden lock state is supplied to any controller.

| Controller | Completed / 96 | Hidden prerequisite completed / 48 | Mean capped L2 actions | Bellman increases |
| --- | ---: | ---: | ---: | ---: |
| N101B historical silent-repeat control | 84 | **43** | 9.635 | n/a |
| Repaired visual-only N101 | 79 | 35 | 10.281 | 205 |
| N102 mask, retain last measurements | **86** | 41 | 10.448 | 90 |
| N102 mask, invalidate on silence | 78 | 30 | 11.167 | 300 |
| N102 mask, retain last measurements, **backups disabled** | **86** | 41 | 10.448 | 0 |
| N102 mask, invalidate on silence, **backups disabled** | 88 | 40 | 10.583 | 0 |

**Causal ablation:** Retained-mask controller changed **0/96 action sequences** when learned Bellman updates were disabled. Thus the 90 updates do not provide evidence of a search-driven improvement. Invalidation mode changed **20/96 action sequences**, with **0 new wins and 10 lost wins caused by backups**. These outcomes explicitly fail the acceptance criterion that Bellman backups, rather than key fragmentation, should improve decisions under masked aliasing.

**Proposed True → False lock signal did not occur:** across the 96 tasks, neither N102 mode logged a measured `1 → 0` action-affordance transition for the same visible screenshot; the no-invalidation mode logged 209 `? → 0` measurements, and the invalidation mode 349. Successful movement changes the source image, so the immediately succeeding frame begins with a different (usually unmeasured) vector. A stall therefore usually changes an unknown effect to observed no-effect, rather than flipping a measured true to false.

**Stronger theoretical counterexample (synthetic only):** States `locked_0` and `locked_1` have identical screenshots, identical legal actions, and the same *true instantaneous* binary affordance vector `(reducer=False, enabler=False)`. A silent `enabler` click leaves the screenshot unchanged in both worlds. But a subsequent `reducer` click has a different outcome, because one world has reached the unlock threshold. Therefore not even a privileged perfect one-step Boolean affordance vector would make this particular two-step lock world Markov. This demonstration does **not** prove such perfectly invisible states exist in the archived ARC games. Original N100 reported a *gap-only* alias with different complete frame hashes; it did not prove full-frame invisibility in native ARC.

**Interpretation:** An observed affordance mask is an intervention-conditioned observation summary, not the current physics. It can be useful for exploration while still staling, fragmenting states, aliasing multi-step prerequisites and making backup targets incomparable. Improving a partially observable controller requires a **predictive state representation or learned belief** that distinguishes action-response futures, with intervention costs included. This is a hypothesis for later work, not a result established by N102.

## 3. Contrastive goal extraction on real archived source observations

### 3.1 Fixed, reward-blind predicate grammar

`src/n102_contrastive.py` defines a fixed inventory of Boolean predicates before examining success labels: colour existence/absence, connected components, holes, filled bounding boxes, straight runs, full rows/columns, bilateral symmetry, occupancy bands with predeclared area thresholds, colour contacts and approximate centroid alignment. The palette is frozen from the **first source frame**; terminal-only colours do not become learned features. This deliberately conservative vocabulary may omit a true newly created terminal object.

For a candidate predicate `p` on one source trace, require:

`p(last outgoing Level-1 frame) == True`, AND
`p(s) == False` for **every earlier source observation**, including the state immediately before the reward-producing action.

Evaluate this same criterion for **every intermediate, nonreward transition** by treating its ordinary endpoint as a pseudo-terminal and using only the earlier prefix. No reward is used for feature computation or controller actions; reward labels are used exclusively to score this retrospective extraction.

### 3.2 Results and negative controls

| Evaluation | Latest-transition-only `False→True` | Strict never-before `False→True` |
| --- | ---: | ---: |
| Rewarded transitions with one or more candidates | 24/24 | **21/24** |
| Ordinary nonreward transitions with one or more candidates | 210/344 | **156/344** |
| Negative detection rate | 61.05% | **45.35%** |

The strict rule improves specificity **relative to this simple ablation**, but cannot be called a terminal detector. If any strict candidate were used to predict reward on the pooled archived transitions, its apparent precision would be **21/(21+156) = 11.86%**. The event prevalence is 24/(24+344) = 6.52%; the apparent lift does not establish out-of-family predictive performance. The 24 reward events and 344 nonreward events also contain heavily duplicated source trajectories, so treat these as *trace events*, **not independent statistical samples**.

Per family, with the same results across the three recorded seeds except occasional variation in `tu93`:

| Family | Strict reward candidates (seed 76) | Strict candidates at immediately preceding nonreward transition | Example / interpretation |
| --- | ---: | ---: | --- |
| `ar25` | 1 | 1 | Colour area decreases under a fixed threshold; not unique to win |
| `cd82` | 4 | 1 | Contact and alignment candidates; no causal proof |
| `g50t` | **0** | 0 | No terminal candidate under this grammar |
| `lp85` | 7 | **10** | Strong negative control: nonreward produces more first-flip predicates |
| `ls20` | 3 | 3 | Contact/separation transitions are not uniquely terminal |
| `m0r0` | 3 | 0 | Promising fill/shape candidate but correlation only |
| `sc25` | 4 | 1 | Shape/component candidates, unvalidated trigger |
| `tu93` | 1 | 2 | Disappearance of a colour can be an animation effect |
| `s5i5` | no win | — | No positive label available; cannot infer goal |

### 3.3 Critical independence audit

The three frozen N093 policy seeds (76/77/78) share **one native seed (47)**. Seven of the eight completed families have exactly **the same action list and identical terminal frame for all three policy seeds**; `tu93` has two distinct action traces and terminal frames. Accordingly, the reported 7/8 families with an across-seed common new predicate is largely a tautology of repeated paths, **not three independent wins or robust validation across puzzle layouts**. Additional fresh native success trajectories on different legitimate seeds/layouts would be required to test stability, without accessing sealed families or reset-based membership queries.

### 3.4 Why a strict flip still does not prove the goal

- An action can flip multiple predicates at once: `color vanished`, `component count changed` and `shape aligned` can all be true on the same rewarded transition. One trace cannot identify which was causally required.
- Reward-response outgoing frames can contain animation **after** the engine decided to award reward; changes from the pre-action observation to `frame[-2]` can be post-trigger decoration.
- A monotonic progress measure crossing a predeclared threshold can flip at a nonreward endpoint as readily as a reward endpoint. The exhaustive 344 nonreward transitions demonstrate this failure.
- A predicate that is false before and true at reward might be neither necessary (other winning paths bypass it) nor sufficient (it appears in losing or continuing states). Counterfactual necessity/sufficiency and Level-2 transfer are **untested**.

## 4. Decision gates and next scientifically justified work

1. **Retain N101's mathematical Bellman repair**, but do **not** promote N102 affordance-mask-backed search: the mask alone did not solve partial observability, and backups were inert or harmful in the matched ablation.
2. **Retain N102's pre-action → outgoing terminal contrast and full negative controls** as a useful *candidate nomination* tool, with mandatory abstention when no candidate exists. Do **not** expose these predicates to a live Level-2 planner as established goals yet.
3. On a **diverse training-only cohort**, seek additional legitimate source successes with distinct layout/trajectory seeds. Precommit a family-transfer test and report both first-flip precision and false-positive rate on nonreward steps before learning a goal grammar. `s5i5` must remain unscored for reward terminal extraction until a real source win exists.
4. For partial observability, test predictive equivalence of learned action-response sequences (and their exact native costs), rather than assuming one-step binary affordances identify latent mode. Do not restart a reset-query campaign or game-specific `vc33` policy search.
5. Do not claim whole-game ARC wins, Kaggle scoring improvements, or mathematically identified invariant goals from this package. None were measured.

## 5. Reproduction and artifact register

- `src/n102_affordance.py`: observation-only paid-action tri-state mask, stable hash and repaired Bellman integration.
- `src/n102_contrastive.py`: fixed Boolean geometry/topology predicate library, strict-first-flip and local-flip ablation.
- `src/n101_bellman_fixed.py` and supporting N101 modules: byte-preserved controller baseline carried from the previous source audit.
- `experiments/affordance_benchmark.py`: matched 96 synthetic task benchmark, includes paired backups-on/off comparisons.
- `experiments/contrastive_benchmark.py`: 24 real archived rewarded Level-1 source events and all 344 nonreward negatives; uses only saved public frames.
- `experiments/check_frame_stack.py`: optionally reruns the eight seed-76 N093 archived native Level-1 paths with per-action frame-hash assertions; requires local SDK archive extraction, no network.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: unchanged user-provided N100 predecessor source, retained for reproducible SDK replay.
- `inputs/l1_native_frame_replay.npz`, `inputs/native_replay_manifest.json`: archived SHA-verified N097B/N093 raw public observations.
- `results/affordance_benchmark.json`: all task-level traces, Bellman events, action counts and paired summary.
- `results/contrastive_goals.json`: all event-level predicates, per-family labels and negative controls.
- `results/frame_stack_check.json`: independently replayed public SDK frame indexing.
- `tests/`: **29 local tests** including N101 Bellman regression, N102 affordance semantics, two-mode alias witness and contrastive negative controls.

See `README.md` for full commands. `SHA256SUMS.txt` pins input and output files. All code and results are included in the ZIP; the extracted native SDK `work/` tree is intentionally not duplicated because it is reproducibly obtained from the pinned input ZIP.