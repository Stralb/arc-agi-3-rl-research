# REPAIR_REGISTER — initial source/evidence audit (2026-10-27)
Working branch: `audit/e128-evidence-20261027`. No paper, native results, checkpoints, or frozen sources have been modified.
Statuses: OPEN, IN PROGRESS, BLOCKED, DONE. Verification terms follow EVIDENCE_LEDGER.md.

| ID | Priority | Problem | Smallest defensible repair | Execution status | Verification/result |
|---|---|---|---|---|---|
| RR-001 | P0 | E128 reports E126 official Kaggle score 0.33 (ID 57690887), but published GitHub manifest explicitly says E126 candidate was not submitted. | Obtain original Kaggle entry receipt with ID, timestamp, score, notebook version and matching SHA; establish whether submitted *after* snapshot; correct repository metadata/report to match exact version only after evidence. | OPEN | CONTRADICTED between sources; no server receipt inspected. |
| RR-002 | P0 | E128's 72-run DQN/PPO coursework study is not located in current published experimental indexes. | Search commit history, archive branch, original owner-held experiment ZIPs/scripts/logs/checkpoints; verify 72 + 12 random + 24 ablations and per-run provenance. | IN PROGRESS | Reported PDF Table 1; raw evidence UNVERIFIED. |
| RR-003 | P0 | Moodle package needs source notebooks, PDF, Kaggle and Paper Track receipts; GitHub checklist says incomplete. | Create definitive manifest, include exact selected code, final PDF, receipts, links, team contributions and anonymized credential scan. | OPEN | Submission completeness MISSING. |
| RR-004 | P0 | E128 ends with “Team contributions remain to be confirmed.” | Obtain actual contributor roles and add a factual statement. Do not invent. | BLOCKED (specific authorship evidence) | VERIFIED omission in paper. |
| RR-005 | P0 | Teammate E125 effect checkpoint redistribution permission unresolved. | Establish rights/permission and dependencies before public or Kaggle reuse; document exact provenance/license. | OPEN | UNVERIFIED, explicit repo license warning. |
| RR-006 | P1 | No original SDK/game binaries or full raw action/frame archives in public GitHub subset. | Inspect authorized owner-held `N100_ACTIVE_FSM_20261025.zip`, original N114/N117 records, and E126 8.75 MB native evidence without modifying originals; independently replay if available. | OPEN | Repo explicitly documents absence. |
| RR-007 | P1 | Paper uses the wording “confirmed E126 official score” without receipt and local comparisons have only exposed games. | Split assertions into local SDK, reported Kaggle, directly server-verified; retain the explicit development-exposure limitation. | OPEN | Source mismatch; local arithmetic independently checked. |
| RR-008 | P1 | Core matched comparison uses DQN-I1 bundled changes and externally pretrained effect CNN. | Reconcile source/config and annotate that the full package, not individual effects, is tested; document all-in pretraining cost separately. | OPEN | Paper discloses confounding; underlying source not yet found. |
| RR-009 | P1 | Required learning/adaptation curves from intermediate evaluated checkpoints are unavailable. | Locate checkpoint traces in owner-held history; if unavailable explicitly disclose and maximize supported within-run evidence without fabricating checkpoint curves. | OPEN | Paper itself flags gap. |
| RR-010 | P1 | Latest repo main is a deliberately curated subset, potentially hiding original experiments from review. | Preserve archive branch and add evidence mapping for DQN, PPO, E126, raw runs, checkpoints, plotting, notebook release. | IN PROGRESS | Archived indexes read; many N-series files available. |
| RR-011 | P1 | Main release verifier asserts `official_kaggle_submission == False` and hence intentionally cannot verify E128 official claim. | Keep verifier truthful; add separately documented *external server* record and cross-version source hash check if obtainable. | OPEN | Verified code/manifest contradiction; do not rewrite test to pass artificially. |
| RR-012 | P2 | Main code under `src/local_effect_policy.py` had stale import, repaired in main latest commit. | Keep fix; preserve frozen N093/N117 sources; validate unit tests when a local checkout is available. | DONE (source change existed) | Commit `49b966d` fixes import; execution of tests not independently rerun here. |
| RR-013 | P2 | Existing diagrams may have incomplete provenance and older charts were removed during repo cleanup. | Regenerate supported figures from original CSV using scripts; never recreate unsupported chart counts. | OPEN | Latest commit archives unsupported charts; no local regeneration yet. |
| RR-014 | P2 | E128 main text appears to fit 8-page maximum; source/template parity unestablished. | Find actual E128 .tex, style and figure scripts; verify exact PDF build and disabled RLJ cover. | OPEN | PDF inspected: 8 pages main + 2 references. |

## Grading-specification update — 2026-10-27
See [full 44-row matrix](REQUIREMENT_TO_EVIDENCE_MATRIX.md). No scientific results were modified.
- RR-015 [P0, OPEN]: Recover raw DQN/PPO 72-run sources, 12 random and 24 PPO ablation trajectories, gradient updates/checkpoints and native scorer versions; do not promote N117/E126 as PPO.
- RR-016 [P0, OPEN]: Recover proper policy-checkpoint learning or measured adaptation curves. Figure 2 of E128 is within-run event timing, **not** the required checkpoint-learning curve.
- RR-017 [P0, OPEN]: Resolve author contributions and Moodle/Paper Track/Kaggle nomination receipts. Leaderboard 10 cannot be scored without eligible class rank.
- RR-018 [P1, OPEN]: Verify PPO masked log-prob and action legality; verify DQN-I2 conditional-stall policy is substantive rather than pure hyperparameter tuning; disclose frozen effect-model pretraining.
- RR-019 [P1, OPEN]: Reconcile E126 server receipt/version *chronologically*: current E128 PDF postdates public main commit, so contradicting status descriptions do not themselves prove a false claim.

## Forensic-code repair update — 2026-10-27
Linked full audit: [FORENSIC_CODE_AND_RESULTS_AUDIT.md](FORENSIC_CODE_AND_RESULTS_AUDIT.md). No source/report rewriting; no native training.
- RR-020 [P0, OPEN]: Source-level DQN-I2 review. Verify threshold, counter reset, actual action changes vs I1, exploration scheduling and whether the intervention is substantive beyond epsilon tuning. **Current conclusion conditional/borderline, not proven.**
- RR-021 [P0, OPEN]: PPO-I2 actor/rollout mask audit. Ensure mask consistency between old sampling and new-policy logprob, click-type factorisation, entropy, GAE, terminal/truncation and correct optimizer steps.
- RR-022 [P0, OPEN]: Inspect original coursework run files and explain DQN-I1 361 updates vs simple 360 expectation; investigate all arms' exact 3,072 calls versus possible early GAME_OVER/reset. Recompute real runtime and native score from per-run records.
- RR-023 [P1, DONE static check only]: Confirmed N093→N117→E126 source-prefix inheritance, E126 no PPO gradients, frozen CNN and sparse gate. Native execution remains unverified.
- RR-024 [P1, DONE recorded-data arithmetic only]: Independently reaggregated 1,125 E126 records and 36 paired-difference rows; no unexpected arithmetic discrepancies found. Original frame-hash replay remains open.
- RR-025 [P1, OPEN]: Verify E126 `s5i5` first divergent same-frame action 3 and complete 8,632-action trace against owner-held `E124_E125_E126_FULL_NATIVE_EVIDENCE.zip`.

## Six-perspective review additions — 2026-10-27
Full separate and cross-review report: [SIX_PERSPECTIVE_TRIBUNAL_20261027.md](SIX_PERSPECTIVE_TRIBUNAL_20261027.md).
- RR-020 | P0 | UNVERIFIED: PPO-I2 masked old/new log-probability ratio and conditional click support | Audit exact rollout/update code with stored/recomputed mask, legal actions, entropy, log-prob values | OPEN; original source not yet located.
- RR-021 | P0 | UNVERIFIED: DQN target-bootstrap terminal/legal masks, actual gradient updates and DQN-I2 exploration branch | Inspect source and event triggers, compare I1/I2 matched actions, reject pure tuning as substantive without stronger mechanism | OPEN.
- RR-022 | P0 | VERIFIED missing paper evidence: true learning/adaptation checkpoint curves | Search original records; no fabricated surrogate from first-reward timing | OPEN.
- RR-023 | P1 | E126 changed choices 28/75 vs only six positive score pairs and four extra levels, all gains from two exposed families | Keep descriptive inference and leave-one-family analysis | OPEN (paper already cautiously reports core limitation).
- RR-024 | P0 | Official Kaggle provenance mismatch and missing submission/team receipts | Verify platform server records with version/time/SHA, author contributions and Moodle/Paper Track status | OPEN; not a misconduct finding.
- RR-025 | P1 | E126 offline verification is not fresh SDK replay; original owner-held trace files absent | Reconstruct authorized SDK and verify source/frame hashes if available | OPEN.
- RR-026 | P1 | Report balance: separate E126 narrative outweighs core six-stage coursework evidence | Only after science verification, prioritize rubric-critical evidence within eight main pages | OPEN; paper unchanged.

## Formal academic prosecution 2026-10-27
[Ranked case and exact dismissal tests](CASE_FOR_PROSECUTION_20261027.md), CP-01 through CP-12. No manuscript or source changes.
- RR-027 [P0 OPEN] Close CP-01/06/07: recover and audit six-stage DQN/PPO source, train/eval split, 108 total original logged episodes, scorer version, optimizer and target/log-prob invariants; investigate 361 DQN-I1 versus nominal 360 update schedule.
- RR-028 [P0 OPEN] Close CP-04: recover genuine budget-indexed learning/adaptation trace; do not relabel cumulative first win figure.
- RR-029 [P0 OPEN] Close CP-05: source-review DQN-I2 stall-state logic and matched epsilon controls; prove substantive or classify honestly as tuning.
- RR-030 [P0 OPEN] Close CP-02/03: reconcile E126 Kaggle ID 57690887 with earlier manifest, team nomination/class rank, author contributions, Paper Track and Moodle receipts.
- RR-031 [P1 OPEN] Close CP-08/09/10: report DQN-I1 as a bundled causal treatment; verify original PPO mask-only control; document separately pretraining/online/eval costs and teammate checkpoint rights.
- RR-032 [P2 OPEN] Close CP-11/12 through cautious generalization language and evidence-led page prioritization, with no unjustified promise of new holdout.

## Defence disposition — 2026-10-27
[CASE_FOR_DEFENCE_20261027.md](CASE_FOR_DEFENCE_20261027.md) does not close any unverified claim with manuscript text alone.
- CP-01/02/06/07: **STILL UNCERTAIN** — recover original course evidence and Kaggle server receipt; no source-level acquittal inferred.
- CP-03: **VALID, potentially administrative repair** — factual roles and true external submission receipts, if available.
- CP-04: **VALID, potentially substantial work** — actual budget-indexed learning/adaptation data; cumulative win timing is insufficient.
- CP-05/08/09/10/11/12: **PARTIALLY REBUTTED** — preserve precise narrow concerns (conditional epsilon-tuning, bundles, all-in compute, single-case ablations, generalization and narrative emphasis); reject accusations that null result or disclosure is a scientific error.
No paper/code/checkpoint/result changes in this update.

## Moderator dispositions — 2026-10-27
[SCIENTIFIC_CROSS_EXAMINATION_20261027.md](SCIENTIFIC_CROSS_EXAMINATION_20261027.md) establishes **no confirmed defect** in uninspected DQN/PPO training source. It establishes missing learning/adaptation curves and no individual DQN-I1 component attribution; E126 architecture confirmed. **P0** recover original six-arm source/108 trial records, check PPO mask ratios and DQN-I2 conditional schedule; obtain legitimate budget-indexed curves and Kaggle receipt. **P1** reconcile all-in pretraining and source/checkpoint lifecycle; original SDK E126 traces. No manuscript alteration performed.
