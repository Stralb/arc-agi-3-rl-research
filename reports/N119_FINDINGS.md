# Delayed Native-Reward Credit and Observed State-Return Risk

**Date:** 26 October 2026. **Status:** Research completed; no deployment promotion.

## Research decision

**Do not replace frozen B1 + N093.** The best observed experimental 25-public-game result remains **13 Level-1 wins, 2 Level-2 wins (`tu93` and `vc33`), 0 Level-3 wins**, compared with frozen **13/1/0**. N119 contributes **no new native completion** beyond the earlier local-effect candidate. Its credits changed decisions, but the tested state-return penalty had no causal effect on selected trajectories.

All 25 public games are historically exposed development environments; there are no new independent layouts. There is no official Kaggle private score or human-reference RHAE for this work. A terminal `GAME_OVER` is not assumed to occur at a universal fixed action count. Every native action was charged and capped at 200 **per level**.

## Hypotheses and mechanisms

N118 showed that history improves prediction of visible pixel changes without improving native gameplay. N119 tests two additional signals using strictly previously observed, charged SDK transitions, rather than a further screen-prediction model.

1. **Delayed native-reward eligibility (association, not causal credit).** When and only when a real SDK level-completion reward arrives, associate that reward with the last at most six action descriptors, decaying by 0.65 for each step of separation. Descriptors use the **existing frozen B1 HypothesisMemory** abstraction. Carry the association to the next level with a 0.70 discount. At Level 2 onward, assign a **bounded 0 to +0.055 selection-score bonus**, never a Bellman reward. This is deliberately not a memorized physical coordinate sequence.
2. **Empirical state-return risk.** When a charged, nonterminal, nonreward transition changes pixels but returns to a recently observed *full-frame digest*, mark that action descriptor as associated with a state-return cycle. Use only previously observed outcomes, at least two samples and Beta smoothing for a **soft bounded penalty**. This is not a hard mask, not a generic no-op penalty, and not proof of task regress.
3. **Misattribution control.** Reassociate effects and credits with a deterministic alternative legal action descriptor before scoring, to test whether the correct observation/action attribution matters.

All variants retain frozen B1 Level 1, N093 pretrained PUCT and unchanged empirical Bellman updates. Native level advancement remains the only Bellman reward. No game name or family-specific action code enters the actor, and it never inspects hidden game state, SDK game implementation, oracle frames or a shadow simulator. The runner uses game identifiers only to select public environments for evaluation.

## Full native 25-family results

| Acting controller | L1 | L2 | L3+ | Total levels | Charged SDK actions | New L2 families |
|---|---:|---:|---:|---:|---:|---|
| Frozen B1 + N093 (N114 reference) | 13 | 1 | 0 | 14 | 2,982 | `vc33` only |
| Previous N117 local + online effect (reverified N118 no-history record) | 13 | 2 | 0 | 15 | 2,706 | `vc33`, `tu93` |
| N119 delayed native-reward credit | 13 | 2 | 0 | 15 | 2,750 | None beyond previous |
| N119 observed state-return risk | 13 | 2 | 0 | 15 | 2,706 | None beyond previous |
| N119 combined credit + return risk | 13 | 2 | 0 | 15 | 2,750 | None beyond previous |
| N119 misattributed-evidence control | 13 | 2 | 0 | 15 | 2,753 | None beyond previous |

- **100 newly run public native episodes, 10,959 SDK actions; all replayed independently and exactly.** No trial ended from an experiment exception.
- The frozen Level-1 trajectory is unchanged action-for-action and frame-for-frame for **100/100 newly run family/arm episodes** against N114 original source.
- The risk-only actor's **25/25 entire trajectories** match the earlier local-effect policy exactly (2,706 actions). The combined actor's 25/25 trajectories match delayed credit alone exactly.
- Credit changes full trajectories in **11/25 families** versus local effect, without changing the number of native rewards.
- In `tu93`, delayed credit clears Level 2 after 26 actions and ends Level 3 after 35 actions. Local effect cleared Level 2 after 23 and ended Level 3 after 27. These are different failure durations, not demonstrated puzzle progress.
- Across N119 arms, there are roughly 82–83 observed non-no-op returns to recently visited full-frame states per 25-game run. In the risk-only arm, a nonzero selected-action risk penalty occurred three times, but none altered the physical trajectory. Thus the risk feature did not demonstrate a benefit.
- Credit association records 34 rewarded-descriptor associations over the 25 games. Reward credit is **not** proof a preceding control caused completion; it is a small selection prior derived from true native rewards.

Lower aggregate action counts are not presumed more efficient: a game can terminate early. Game-relative human reference efficiencies are unavailable; **official RHAE was not computed.** All public cases have been historically exposed.

## Family-held-out five-step terminal-window diagnostic

A *separate offline audit* tests whether recent observable action histories improve prediction of `GAME_OVER` occurring within the next five charged actions **under the archived behavior policy**. Training uses N118's already-charged, 75 native histories and leaves *all examples from the evaluated family* out of fitting. This diagnostic never influences N119 acting-time decisions.

| Cross-family-held-out metric | Time-in-level only | Time + action/effect history |
|---|---:|---:|
| Native transition decisions | 3,668 | 3,668 |
| Terminal-window positive examples | 180 | 180 |
| ROC AUC (higher better) | 0.5892 | 0.6011 |
| Brier error (lower better) | **0.05008** | 0.05970 |
| Log loss (lower better) | **0.20604** | 0.22791 |

This is **not a reliable causal action-risk estimator**. Although relative discrimination increases slightly, both calibration measures worsen. More fundamentally, an impending-game-over label depends on the *future behavior policy* as well as game state; observations of one action per state cannot reveal the outcome of unchosen legal alternatives. Within-family and across-policy transitions also are not independent samples.

The test excludes censored last-five transitions from episodes stopped by the research-level 200-action cap and never uses an observed terminal outcome before it occurs at evaluation time. See `hazard_audit.py`, `results/hazard/summary.json`, and the family-level CSV for the exact protocol.

## Seed and standalone correctness controls

- Two extra policy seeds (77 and 78) for three acting arms (`delayed_credit`, `credit_plus_risk`, `attribution_placebo`) on `tu93` and `vc33`: **12 native episodes, 1,043 SDK actions**. All independently replayed exactly.
- Both correctly attributed credit arms retained the two historically known Level-2 successes for the tested seeds, and **no Level 3** was completed. The placebo lost `tu93` Level 2 at seed 78. These repeats use an exposed layout and **do not establish generalization**.
- The standalone `candidate_submission.py` generated by embedding N119 into the unchanged frozen source reproduced action/frame/reward tuples in **4/4** acting-time tests: `vc33`, `tu93`, `ar25`, `lp85`.
- The embedded notebook is **research only** and has not been submitted on Kaggle. This is not a private competition score. The frozen source and notebook are preserved byte-for-byte.

## Evidence provenance and limitations

- Original frozen source: `inputs/submission.py`, SHA-256 `e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d`.
- Original frozen notebook: `inputs/submission.ipynb`, SHA-256 `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`.
- Public test SDK: `inputs/N100_ACTIVE_FSM_20261025.zip`, extracted by `prepare_runtime.py`, never used as a physics oracle by the actor.
- Frozen N114 reference: `inputs/N114_public25_native_traces.json` and `inputs/N114_public25_matrix.csv`.
- Previously charged N118 trajectories: `inputs/n118_logged_native25/`, for a strict cross-family predictive audit and exact baseline parity.
- N119 live action traces and all rewards: `results/native25/`, `results/policy_seed_77/`, `results/policy_seed_78/`.
- Independent replay: `results/native25_independent_replay.log` and `results/seed_independent_replay.log`.
- Per-family results: `results/analysis/per_family_25.csv`; seed results: `results/analysis/seed_study.csv`.

**Deployment decision: retain frozen N093.** The learned local-effect policy remains the strongest experimental Level-2 candidate, but its sole added `tu93` Level-2 completion remains limited to a historically exposed layout. Future progress requires genuinely independent game configurations and causal, action-dependent evidence about survival/progress, not another positive prediction metric divorced from real rewards.