# N101B empirical findings and research decision

Date: 2026-10-25. All new experiments are deterministic synthetic diagnostics.

## 1. Source recovery audit

- The *actual* previous N101 source and records existed under
  `/mnt/data/N101_RTA_ZERO_RESET`; its 18/18 tests were rerun successfully.
- Previous assistant claims tying N100's missing family outcomes to Wits Slurm
  were wrong. N100 belongs to a different ChatGPT conversation. Its genuine
  family statuses/output were not in this accessible file workspace or
  retrieved prior-conversation context. Do not infer failure/success.
- The original fixture's buttons are `(2,46)` and `(2,26)`, the same two
  coordinates as the historical N098 seven-action oracle description.
  The test gave the correct moving-button action an explicit gain prior.
  This was a narrow synthetic sanity check, not independent game generalization.
- The original `n101_gate.py` will approve ten plausible hand-authored JSON
  family reports, even when these are synthetic mocks. It validates claimed
  fields, not the original experimental logs. The old N100 status's cluster
  rationale is ungrounded, not endorsed by this package.

## 2. Audited procedural task generator

Each of the 18 layout replicates crosses four hidden-prerequisite depths
0–3, two visibility conditions, and three decoy counts. Every environment
renders 64×64 `frame[0]`, with moving/static referents of unique colors and
arbitrary edge controls; some have a legal non-spatial enabler. All action
selection is through the public observation object. Environment-private
mechanism state is used **only to execute and score** the synthetic test.
The candidate detector reads observed border components; the heuristic is a
vectorized equivalent of `AlignedX` (the equality is unit-tested).

The mover prior is obtained from **charged synthetic Level-1 observations**,
by testing legal controls and observing actual changes in geometric gap.
It is shared across all compared policies. The one-hypothesis N101B change is
an opt-in bonus for one additional silent alternative action after a known
geometry-reducing control stalls on a visually identical frame. It never
receives the hidden depth, role labels, or the oracle action sequence.

This generator tests a **class deliberately resembling the proposed lock
mechanism**. It is not a random sample of ARC games, independent external
validation, native ARC source, or official Kaggle scoring.

## 3. Fixed-policy paired results (18 replicates, 432 cases per policy)

| Controller | Completed | <13 actions | Mean capped L2 calls (all 432) |
|---|---:|---:|---:|
| Recovered N101 | 305 | 268 | 11.146 |
| N101B silent-trial treatment | 336 | 283 | 10.898 |
| N101C observed graph key + gated backups | 321 | 260 | 11.002 |
| N101C observed graph key + no backups | 321 | 260 | 11.002 |
| No history | 312 | 261 | 11.236 |
| No L1 prior | 218 | 149 | 14.176 |
| N101 without H backups | 305 | 268 | 11.146 |

No resets. All variants used the same 18-action cap, observations, and
procedural task specifications. All 432 recovered-N101 and no-backup control
action traces matched **exactly by hash**. The code and full per-case rows are
included for independent verification.

### Held-out evaluation

After an exploratory pilot on 3 layout replicates, the N101B dose cap
(two consecutive silent tries) and bonus (1.7 score units) were fixed.
On 15 later layout replicates (360 cases):

| Metric | N101 | N101B | Paired treatment effect |
|---|---:|---:|---:|
| Completed | 256/360 | 280/360 | +24, +6.67 percentage points |
| Completed in fewer than 13 L2 actions | 225/360 | 237/360 | +12, +3.33 percentage points |
| Capped mean L2 actions | — | — | -0.233 calls per task |
| Both completed, B faster | — | — | 27 cases |
| Both completed, B slower | — | — | 39 cases |
| Newly solved by B | — | — | 24 cases |
| Solved by N101 but lost by B | — | — | 0 cases |

Cluster bootstrap 95% intervals (15 replicate groups, 12,000 draws):
completion-rate difference **+5.00 to +8.06 pp**; <13 success difference
**+2.22 to +4.44 pp**; difference in mean capped actions **-0.303 to -0.161**.
These intervals reflect procedural generator variation. They do not model
native ARC family or evaluator uncertainty, and should not be generalized.

### Mechanism-specific costs

- Invisible depth-2: N101B gains 12 additional held-out completions; invisible
  depth-3 gains 12. Depth-3 also gains 12 cases under the <13 threshold.
- Invisible depth-1: both solve the same 39/45, but N101B needlessly spends
  an additional 0.867 mean calls per task. This is an unavoidable uncertainty
  cost unless a signal or transferred prerequisite estimate differentiates
  a one-dose gate from a two-dose gate.
- Visible prerequisites or zero-dose tasks: N101B changes no results in
  this particular generator.
- Without any decoys, both variants solve all held-out tasks; performance
  differences emerge under mixed-action competition, not an oracle-equivalent
  two-button fixture.

## 4. Structural RTA* claim audit

**Original N101 backups are inert on the generated hidden-lock suite.**
The belief key combines the raw frame with a rolling hash of three recent
native action/outcome events. These keys virtually never recur when the
same rendered pixels have differing action histories. All 432 original N101
traces are identical to a control in which the H-backup table is cleared
after each step. Consequently, the observed gains in N101B are attributable
to a *silent-trial scheduling heuristic*, **not** verified RTA* backup learning.

The second diagnostic is an observable 7×7 cyclic grid with a misleading
Manhattan-distance goal around a wall. It demonstrates a separate issue:
raising H from **only observed successor edges** while legal alternatives
remain unexplored can erroneously inflate search estimates:

| Synthetic cyclic controller | Reached goal? | Actions |
|---|---|---:|
| Original rolling-history N101 | No (80-action limit) | 80 |
| Original with H updates disabled | Yes | 75 |
| N101C stable visible nodes, old unsafe backups | No (80-action limit) | 80 |
| N101C stable visible nodes, H disabled | Yes | 20 |
| N101C stable visible nodes, backup only after full local action coverage | Yes | 20 |

The safe-coverage controller made no H increases on this successful case,
so the result only establishes avoidance of a failure, **not evidence that
useful heuristic learning occurred**. N101C's reduced aliasing also caused
regression against N101B on the hidden-lock suite (321/432 vs 336/432;
<13: 260/432 vs 283/432). **Reject N101C as a blanket replacement.**

## 5. Identifiability bound (not an empirical score)

Consider two synthetic mechanisms whose frame and legal action set are
identical until an alternative click is tried: mechanism A requires one
visually silent enabler, mechanism B requires two. With the same five
required subsequent geometry-reducing moves, their retrospective oracle
paths cost 6 and 7 actions respectively. A source-only controller that lacks
a distinguishing signal cannot simultaneously avoid a redundant second
enabler in A and a wasted premature reducer test in B. Hence a universal
7-action trajectory for unknown latent mechanisms is not implied by a
7-action *retrospective oracle* path on one game.

## 6. Research decision

**Keep N101B as a local, experimentally supported hypothesis for repeated
silent prerequisites; do not yet promote to a native/general controller.**
The test family was intentionally designed to exercise that mechanism,
so this does not validate native `vc33` or Kaggle competition performance.

**Reject the current "verified RTA*" label.** Future graph-search revisions
must demonstrate (i) a value update that actually changes a decision,
(ii) a correct optimistic treatment of unknown legal successor actions,
(iii) latent-state aliasing protection, and (iv) better native depth / cost
without regression versus the unchanged N101 and N098 references.

### Actual remaining N100 dependency

Recover N100's ORIGINAL previous-chat nine-family completion report, source
logs and reset/replay diagnostics. Do not substitute Slurm checks or a synthetic
N100 JSON mock. Then check whether the N097B L1 component-binding outputs and
N098 exact 13-action trace are available under the same native evaluation
contract. Only then is a controlled live L2 run scientifically interpretable.

No native `vc33` experiment, independent native replay, hidden game source
reading, official scoring, or Kaggle submission occurred in this package.