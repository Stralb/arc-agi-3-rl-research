# N105 — Macro-Action Search: Verified Native Test and Negative Result

25 October 2026 · frozen B1/N093 source · no cluster or test-family execution

## Decision

**Do not replace `submission.py` or `submission.ipynb`.** N105 implements actual repeated-action options, safe termination rules, and option-level semi-Markov Bellman backups. However, in the audited eight-family development comparison, **zero new Level-2 completions** were obtained. The experiment does not demonstrate an ability to reach Level 3 or increase Kaggle's score. The frozen B1 + N093 pretrained PUCT remains the measured safer deployment candidate.

## Why the proposed depth collapse is not a theorem

A state-terminating option `o = repeat a until visual-delta=0` occupies `d >= 1` **charged native SDK actions**. Treating it as a single meta-decision reduces the number of choices made by the controller, not the number of environment interactions. A correct macro-level Bellman equation requires the semi-Markov duration term:

`Q(s,o) <- E[ R + (1-terminal) * gamma**d * max_o' Q(s',o') ]`

where R is **real SDK level advancement**, not a visual progress pseudoreward. This study uses gamma=0.985, initializes untried options optimistically to Q=1, and retains B1's original atomic Bellman updates for every charged click.

The option endpoints are **not generally Markov**. Two invisible prerequisite states can display identical frames, share identical legal actions and produce zero visible delta on the first enabler click, yet require one versus two more clicks before the next control can move. Thus the exact same state-terminating option ends in visually identical observations with different future transition distributions. The package includes this constructive counterexample.

Another structural problem: historical N093's `vc33` *Level-1* successful action block is `ACTION6(61,33) x3`; its historical Level-2 winning trace uses **different** controls. Exclusive repetition of the only source block cannot reproduce the historical solution. This is **analysis of archived traces only**: N105 did not run new `vc33` experiments.

## Implementation

1. Execute frozen B1 exactly on Level 1, logging each chosen action and before/after screen. Awarded Level-1 completion alone authorizes source-block synthesis. Split the successful trajectory into *contiguous exact control identity* blocks; create one option per distinct source control, retaining lengths and effect counts as metadata. For ACTION6, source identity is the native coordinate, not a learned cross-layout rebinding map. This is an explicit limitation.
2. Starting on Level 2, `source_only` chooses exclusively among these source options. `open` adds at most two on-screen B1+pretrained-PUCT candidate options; `open_novel` filters those to previously absent controls (secondary ablation). No family-name dispatch exists in the acting source.
3. Every selected option repeatedly sends **the same legal native action** and calls the B1 atomic learner after each step. It stops at the first pixel delta of exactly zero, a visible-state cycle, 12 charged steps, real reward, native game termination, action becoming illegal, or 200 charged Level-2 actions.
4. At option termination, update the semi-Markov empirical Q table and its observed predecessor links; use optimistic Q plus a source-order/exploration tie break to choose the next option. No shadow stepping, resets, cloned SDK, privileged reward oracle, or hand-written Level-2 sequence.

This is **semi-Markov option-level Bellman search**, not a verified RTA\* implementation with admissible heuristic, optimality or full-POMDP planning guarantees.

## Primary matched native experiment

- 8 public training families: `ar25, cd82, g50t, lp85, ls20, m0r0, sc25, tu93`.
- 2 N093 policy seeds per family: 76 and 77; native seed fixed at 47.
- 3 arms each: B1+N093 PUCT baseline, `source_only`, and `open`.
- 200 actions *per level* (not the original N093 200-total-action study), 12-action macro cap, real SDK reward only.
- The initial long process was interrupted after 40 results; the remaining 8 unique arm/seed cases were completed separately. Three overlapping sc25/76 reruns were excluded from primary counts. Exactly **48 unique primary runs** are analyzed.

| Arm | Episodes with native Level-1 completion | Episodes with native Level-2 completion | Charged Level-2 actions | Multi-step options | Option terminations |
|---|---:|---:|---:|---:|---:|
| Frozen B1 + pretrained PUCT | 16/16 | **0/16** | 1,826 | n/a | n/a |
| Source Level-1 options only | 16/16 | **0/16** | 1,846 | 356 | 1,182 |
| Source options + current B1 candidates | 16/16 | **0/16** | 1,604 | 376 | 756 |

These are counts of actions before native terminal/game stop or budget, **not** a measure of whether one policy is closer to a goal. More/fewer actions without a win is not a progress claim.

`source_only` option stopping: 1,146 zero-delta, 24 duration-cap and 12 game-terminal stops. `open`: 702 zero-delta, 40 duration-cap and 14 game-terminal stops. The macro actions are real: many execute more than one native step. Nevertheless, neither arm earns another Level-2 completion.

**Effective independence:** In *all eight families*, seeds 76 and 77 yielded identical complete action-and-frame trajectories within each of the three arms. There are **eight distinct per-family scenarios**, not 16 independent successes/failures. They also share the same native seed and level layout.

## Paired ablations

### Disable the option Bellman backups, preserve everything else

Eight families × one seed × two option arms = 16 paired comparisons.

- Backups changed the native action trajectory in **3/16** pairs: `ar25/source_only`, `ar25/open`, `lp85/open`.
- **0** new native Level-2 successes appeared with backups enabled.
- The backup-enabled version recorded state-action value changes and actual action differences; it is not the earlier inert-Bellman bug. That does not prove option endpoints have correct Markov semantics.

### Force consideration of distinct new B1 actions

Eight families × two seeds: 16 additional `open_novel` native runs.

- **0/16** Level-2 successes.
- These 16 action trajectories were **identical** to the original `open` variant despite the altered proposal menu.
- 30 options were selected from outside the Level-1 source vocabulary; this expansion did not rescue the search on these scenarios.

## Provenance and replay

- Original frozen N100 source archive SHA-256: `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`.
- Original frozen N093 network checkpoint SHA-256: `42996eed8eea3581971b054a499cf9063d82862147222d8d79c6c0d632e6c5f3`.
- Level-1 parity: **48/48 source arms matched N093's originally archived actions, before/after frame hashes and native rewards**, totaling **738 Level-1 charged actions**.
- Independent replay from action requests alone: **80/80 unique runs and 9,838 native actions**, including all primary, disabled-backup and open-novel arms; every available legality, before/after hash and recorded native level result matched. No neural model or macro controller was instantiated for replay.
- Unit tests cover block parsing, stable/zero-delta/cycle/cap termination, real native reward, option-duration discounting, disabled-backup control, option vocabulary legality and latent-state aliasing.
- No new `vc33` native experiment, no held-out Kaggle evaluation and **no Level-3 win** in these runs.

## Scientific interpretation and next decision

State-terminating control blocks can reduce meta-decision counts. They do not remove aliasing unless the resulting option endpoint observation is sufficient to predict every relevant future. A `delta==0` outcome can mean a lock, a silent prerequisite increment, a click on an irrelevant object, a lost control, or a temporarily static animation. Likewise, Level-1 successful blocks do not identify which new action roles exist in Level 2.

The evidence rules out **promoting the tested N105 source-only and open-option policies as superior submission replacements**. More versions or longer macro caps should not be credited without an actual held-out native Level-2/3 completion under matched total action budgets. Retain the untouched frozen submission until a genuine reward improvement is verified.