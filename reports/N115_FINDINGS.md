# N115: empirical findings and decision

## Source correction

N098 did **not** clear ARC-AGI-3 Level 3. Its seven-action privileged shadow
search cleared **`vc33` Level 2** after spending 373 additional shadow SDK
transitions. N098's legal observation-only counterpart took ten SDK Level-2
actions and did not increase the level-completion count over frozen N093.
The seven-action laboratory oracle is **not** an input to N115.

## Precommitted experimental design

- Environment: **25 public ARC-AGI-3 games** from the bundled SDK, not the
  400+400 static ARC-AGI-1 tasks.
- Same native seed **47**, policy seed **76**, 200 charged SDK actions per level.
- One observed trajectory per family and arm; all 25 cases were already
  historically exposed in this research project. No untouched holdout claim.
- Frozen N093 Level-1 policy, candidate action grammar, network weights,
  native-reward Q-learning and PUCT prior. No post-N093 algorithm used.
- Five arms: mixed fixed bi-grams; different-control pairs; same-control
  repeated pairs; mixed with pair Bellman backups disabled; second click
  selected from *observed* post-first-click candidates (adaptive).
- Every SDK click charged. Stop on native reward/game over. No shadow SDK,
  future-state oracle, game-specific route, full-game reset or source-code
  introspection in the acting policy.

## Measured 25-game outcomes

| Controller | Level 1 | Level 2 | Level 3+ | SDK calls | completed options | option reward events |
|---|---:|---:|---:|---:|---:|---:|
| Frozen B1 + N093 PUCT | 13 | 1 | 0 | 2,982 | - | - |
| Mixed precommitted bi-grams | 13 | 1 | 0 | 2,975 | 288 | 0 |
| Different-control bi-grams | 13 | 1 | 0 | 2,966 | 281 | 0 |
| Repeated-action bi-grams | 13 | 1 | 0 | 3,006 | 288 | 0 |
| Mixed pairs, pair Bellman disabled | 13 | 1 | 0 | 2,969 | 288 | 0 |
| Observed-second adaptive pairs | 13 | **0** | 0 | 2,879 | 278 | 0 |

All five experimental arms preserve 25/25 exact action and frame-hash parity
on Level 1. Only `vc33` advances beyond Level 2 in the frozen and three fixed-
pair arms; the adaptive arm loses even this known Level-2 success. **No Level-3
completion occurs in any arm.**

The mixed arm reaches the `vc33` Level-2 reward at overall SDK call **26**,
versus **30** for N093. Its Level 3 still ends at `GAME_OVER` after **75**
additional actions. Cross-control pairs reach Level 2 at call **37** and
repeated-action pairs at **28**. Those development-layout differences are not
proof of transferable joint-control discovery.

## Causal ablation and failure mechanism

Disabling pair Bellman backups while keeping the pair proposal and visit logic
fixed changed native trajectories in **5/25** families: `ar25`, `dc22`,
`g50t`, `ls20`, and `sp80`. This confirms that the pair Q-values sometimes
influence control, unlike the wholly inert N101B backup ablation.

But **zero successful level transitions occur during a completed two-action
option**. All rewarded transitions in N115 are caused by the atomic B1 fallback.
The proposed pairs have no direct positive reward evidence, so their value
updates mostly discount optimistic continuation values. Reducing controller
decision count also does not reduce charged SDK calls.

The adaptive arm selects its second action from the *actual SDK observation*
after the first. Its result is worse (13 Level-1, **0 Level-2**), demonstrating
that extra reactivity alone does not solve the multi-step UI grammar.

Some shorter runs terminate earlier in GAME_OVER; total SDK calls must never
be interpreted as sample-efficiency improvement without the reward counts.

## Verification

- The native acting loop uses `env.step` exactly once per charged action.
- All **125 new experimental episodes** and **14,795 charged SDK actions** were
  independently replayed via the public SDK, with exact pre/post frame hashes,
  legal action membership, level counters, native rewards and game states.
- First-level archived frozen N093 parity holds for all 25 public families,
  with unchanged checkpoint and frozen notebook checksums.
- Unit tests check option duration and discounting; missing prior actions;
  action legal flags; illegal-second penalty with no extra native charge;
  reward-on-first-action termination; backup-disabled behavior; and native
  `vc33` integration without Level-3 hallucinations.

## Decision

**N115 is a valid, executable, action-pair SMDP experiment with an observed
causal effect on some action selections. It fails the native Level-2 breadth
and Level-3 win gates. Do not promote it to the frozen competition notebook.**

The data do not prove action pairs are inherently unsuitable. They specifically
show that these candidate-generation and exploration rules, on one historically
exposed public starting layout per game, fail to recover the needed UI grammar.