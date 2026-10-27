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


## Judicial order and revised priorities — 2026-10-27
Full 12-charge judgment and evidence-grounded marks: [JUDICIAL_ASSESSMENT_20261027.md](JUDICIAL_ASSESSMENT_20261027.md). **No prior repair is considered completed solely because it was described in the report.** Charge dispositions: CP-04 SUSTAINED; CP-03/06/08/09/10/12 PARTIALLY SUSTAINED; CP-11 DISMISSED as charge of unsupported unseen generalisation; CP-01/02/05/07 INSUFFICIENT EVIDENCE. All **OPEN** technical steps below are safe evidence-recovery/verification tasks, not authorization to invent, overwrite or publish proprietary assets.

| Repair ID | Priority | Judicial action | Status | Closure evidence |
|---|---|---|---|---|
| RR-033 | P0 | Recover **all six original coursework** DQN/PPO sources, frozen configs/checkpoints and all 72+12+24 episodes; independently recompute score/action/walltime/update and verify environment/scorer | OPEN | Primary files SHA, verified training/eval and raw-to-table reconciliation |
| RR-034 | P0 | Determine DQN-I2 substantive vs epsilon tuning by inspecting branch, counters, resets, matched I1/I2 decision consequences | OPEN | Source + matched action diagnostics, optionally original epsilon-only control |
| RR-035 | P0 | Check PPO masked log-prob type/coordinate support at collection/update, old/new ratio, GAE terminal/truncation and true parameter updates | OPEN | Invariant tests and original rollout/optimizer source |
| RR-036 | P0 | Find genuine learning/adaptation measurements vs charged interaction budget; do not substitute time-to-first-reward as learning curve | OPEN | Verified original budget-indexed series or candid disclosure of unresolved requirement |
| RR-037 | P0 | Obtain official E126 Kaggle submission ID57690887 receipt, successful score and SAST timestamp, source/hash and nominated class-team eligibility | OPEN | Platform record; reconcile historical manifest chronology, no invented receipt |
| RR-038 | P0 | Finalise actual member contribution statement, Paper Track link + saved text and Moodle ZIP/receipt; verify code/no secrets | OPEN | Authentic external submission records and manifest |
| RR-039 | P1 | Record DQN-I1 pretrained model rights/origin/data exposure/training compute distinct from E126 peer CNN; isolate online/evaluation budgets | OPEN | Licence/permissions and grounded cost/provenance accounting |
| RR-040 | P1 | Once primary evidence recovered, rebalance 8-page main only as scientifically supported: six-stage coursework central, genuine curves, bundles/control limits, E126 separate | BLOCKED pending RR-033/036 | Consistent source-linked report without deleting genuine nulls |


## Executable improvement plan — 2026-10-27
The [15-task REPAIR_PLAN_20261027.md](REPAIR_PLAN_20261027.md) makes judicial RR-033 through RR-040 actionable. **P0 (8 tasks):** RP-01 retrieve/freeze exact course provenance (BLOCKED ORIGINAL ARCHIVE); RP-02 DQN correctness (BLOCKED RP-01); RP-03 PPO masked probability correctness (BLOCKED RP-01); RP-04 classify DQN-I2 substance (BLOCKED RP-01/02); RP-05 reconcile all 108 original runs (BLOCKED RP-01); RP-06 budget-indexed curve feasibility (screening READY, core data BLOCKED); RP-07 official Kaggle receipt/class nomination (BLOCKED PLATFORM); RP-08 team roles/receipts/packaging (PARTLY READY).
**P1:** RP-09 failure/success evidence (N-series READY; coursework BLOCKED); RP-10 matched DQN/PPO analysis (BLOCKED RP-05); RP-11 ablation-to-mechanism mapping (N-series READY; PPO BLOCKED); RP-12 two-model pretraining/cost/permissions (E126 READY; DQN/rights BLOCKED).
**P2:** RP-13 eight-page E126 condensation outline (READY, constrained by missing coursework findings); RP-14 original E128 LaTeX/figures/build parity (BLOCKED on exact source).
**P3 conditional only:** RP-15 tiny isolated test if RP-04 reveals a scientifically important unanswered change, archives cannot resolve it, legal budget/time exist. **No large retraining by default.**
Acceptance and per-task source/verification requirements are in the plan. Existing RR items remain OPEN until genuine evidence/tests close them; plan creation itself closes none.


## Executed analyses and partial closures — 2026-10-27
[Execution record](EXECUTED_EXPERIMENTAL_ANALYSIS_20261027.md), generated ZIP `arc3_experimental_audit_20261027.zip` (SHA256 `0610fcb1a5243d6ed67b388dca49b8b74234f9c0cfb83e11d3c43c72d8c31c7e`), **14 offline pytest PASSED**.

| Task | Updated execution status | Scope and verification |
|---|---|---|
| RP-01 | BLOCKED | Exact 72-run DQN/PPO source/checkpoints and 36 control runs not in inspected GitHub subset or mounted files; earlier E078 or Phase3N protocols differ; no substitution. |
| RP-02/03 | BLOCKED | Original DQN gradient and PPO masked log-prob sources unavailable; no source-level pass or bug claim. |
| RP-04 | OPEN/UNVERIFIED | Paper-only DQN-I2 stall epsilon trigger 1769/3072; still cannot adjudicate substantive requirement. |
| RP-05 | PARTIALLY COMPLETED | E126 75 paired games and E124–E126 45-arm summaries independently recomputed from GitHub files; 108 coursework cells reconstructed **only from E128 paper**, not original logs. |
| RP-06 | INCOMPLETE REQUIREMENT | Two within-run first reward/attainment figures generated and correctly labelled **NOT learning curves**. No independent policy-checkpoint/adaptation-performance histories obtained. |
| RP-09 | PARTIALLY COMPLETED | E126 s5i5/lf52 win/failure cases and N118 tu93 early GAME_OVER described with source; core coursework exact failure traces absent. |
| RP-10 | PARTIALLY COMPLETED | Reconstructed 12-cell DQN-I2 vs PPO-I2 result matrix; two DQN-only, one PPO-only, nine tied cells; no unjustified significance or efficiency claim. |
| RP-11 | PARTIALLY COMPLETED | Original E126 baseline/contingency/random/salience/trained controls verified from 45-row GitHub summary (44/45/45/45/48 levels). Original PPO mask-only and no-grad code/logs unverified. |
| RP-12 | OPEN | Externally pretrained coursework effect encoder and E125 peer CNN are different; full compute/licence data not obtained. |
| RP-07/08 | OPEN | No independent Kaggle server receipt, team role list, Paper Track or Moodle confirmation. |
| RP-13/14 | NOT STARTED (paper remains unchanged) | Generated figures are candidates only; no E128 LaTeX source or final manuscript rewrite. |

No task was marked fully closed merely on paper-derived data. All original experimental assets preserved; no SDK game actions, new training, or Kaggle submissions performed.


## Eight-page scientific architecture (2026-10-27)
The paper redesign architecture is fixed **in outline only** at [REPORT_ARCHITECTURE_20261027.md](REPORT_ARCHITECTURE_20261027.md), without editing manuscript or changing data. Recommended selection: hybrid with mandated DQN/PPO baseline→I1→I2 evidence before distinct N118→E126 extension. Proposed page equivalent: 0.60 title/abstract; 0.65 introduction; 0.55 task/prior work; 0.90 baselines; 1.05 interventions; 0.65 protocol; 1.80 matched results/ablations; 0.95 extension; 0.85 limitations/conclusion = 8.00. Candidate main figures: 108-cell course outcomes (reported-only), compact E126 score/control decomposition (verified saved arithmetic); reserve actual curves **only if source-valid**. RP-13 **PLANNING COMPLETED**, RP-14 **OPEN** for genuine E128 LaTeX/RLC rebuild/figure provenance; RP-01/04/06/07 blockers remain OPEN. Do not infer grade improvement merely from architecture.

## E129 review manuscript compilation and QA (27 October 2026)
**Execution:** A standalone review reconstruction, rather than a line-edit of the lost E128 LaTeX, has been created in this conversation as `ARC_AGI3_E129_Review_Project.zip`, standalone `ARC_AGI3_E129_Revised_Review.tex`, and compiled `ARC_AGI3_E129_Revised_Review.pdf`. It was reconstructed from E128 PDF, user-provided *generic* RLJ 2026.1 main.tex, approved architecture, and the already verified E126 data tables. The exact E128 `.tex` and byte-identical lecturer-issued `rlj.sty` **remain unverified**, so no claim of editing the original E128 source or meeting exact upstream style hashes is made. A 2026.1 formatting-compatible style is included and cover macro is disabled. Original repositories, neural code, checkpoints and experiments untouched.

**Changes made:** coursework-first introduction and RQ1/RQ2, direct DQN/PPO learning targets/update descriptions, limitation→hypothesis→intervention→evaluation→interpretation for all four interventions, nine-arm native result table, 108-cell *paper-reported-only* outcome matrix retaining all zero outcomes, paired final DQN-I2 vs PPO-I2 comparison, conditional DQN-I2 and PPO mask caveats, clearly separate N118→E126 narrative, exact E126 preserved arithmetic and compact figure, explicit lack of genuine neural learning curves and Kaggle confirmation, complete citation list.

**Verified file production:** `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` PASS in authoring directory **and on a clean extracted source ZIP**; PDF 7 total pages (main ≤8; references on p7 after conclusion); 7 pages raster-rendered and main pages manually inspected; prior E126 exhibit float-before-section and mid-sentence float interruption corrected; no overfull boxes/undefined citations; 13/13 citation keys resolve and 13/13 cited references listed; 22/22 local QA checks PASS, including numeric source-tier checks. Two publication-size figures supplied as source-linked PDF/SVG/PNG with generation script; published coursework values explicitly marked report-only. ZIP integrity test PASS.

**Task progress:** RP-13 **DONE as review architecture implementation**, not final scientific evidence closure. RP-14 **PARTIAL** (rebuild/figures/QA done, original exact E128 project and official byte-identical style still unavailable). RP-05/RP-10/RP-11 **PARTIAL manuscript presentations** (original DQN/PPO source/logs still missing; E126 saved arithmetic verified). RP-06 **OPEN** (no genuine budget-indexed learning/adaptation curves). RP-01/02/03/04 **OPEN** (original six-arm RL training, PPO mask and DQN-I2 mechanism remain unverified). RP-07/08 **OPEN** (official Kaggle 57690887/0.33 receipt, Paper Track, Moodle and genuine team role statement not certified). RP-12 **OPEN** (pretrained model rights and full offline cost). No unsupported claim was upgraded to independently verified.

**Checksum (standalone PDF):** `d961b8423369bc47014276d0e5a982123fe63f3de0cf1aeaddae624df9b04d13`; standalone `main.tex` `617d110a4eeed5814bc46bbf86c10cbea86ac1570848848073c3b698dd5a608d`. These are local generated artifacts, not GitHub-hosted source files. Follow-up must verify official class RLC 2026 template assets and actual team contributions before submission.


## E129 LaTeX review-reconstruction execution — 27 October 2026
**Review deliverables actually created in conversation:** `ARC_AGI3_E129_Review_Paper_FINAL.pdf`, `ARC_AGI3_E129_Review_LaTeX_FINAL.tex`, and `ARC_AGI3_E129_Review_Project_FINAL.zip` (sandbox conversation artifacts; not official Kaggle/Moodle/Paper Track submissions). PDF SHA256 `1b90cc9d70ec4aba6e08b194456ae83dd9c076bccc27affbc35951207e9d9ed5`; LaTeX SHA256 `862f232e4649e8bbb94bfac7ce1d972850721fdda123fe3858bb7eba50a9c132`.
- **RP-13 COMPLETED for review copy:** Implemented hybrid coursework-first presentation with accurate DQN/PPO conceptual exposition, explicit V0/I1/I2 interventions and negative outcomes, nine-arm table, 108-cell report-only outcomes, final-pair comparison and separate compressed N118→E126 research.
- **RP-14 PARTIALLY COMPLETED:** Built review source + two reproducible figures under public RLJ/RLC 2026.1 style copy; disabled cover. `latexmk` compiled seven total pages; all seven pages rendered and checked; E126 table/figure were corrected to stay in their own section; **33/33 automated verification assertions passed**. Extracted LaTeX/PDF text was identical after a clean-directory reconstruction, also 33/33. **Exact original E128 .tex and byte-identical lecturer official style are still unavailable; do not claim direct source edit or certified template parity.**
- **RP-05/06 remain PARTIAL/OPEN:** E126 saved-data arithmetic correctly supported (44→48 levels, 75 matched pairs, positive score cells only `lf52`/`s5i5`). Coursework numbers and per-cell outcomes remain *reported only* from E128, not native replay. No genuine budget-indexed learner effectiveness curve was recovered; manuscript explicitly admits it.
- **RP-03/04/07/08/12 remain OPEN:** PPO mask log probabilities and DQN-I2 substantive code unverified; all-in pretrained costs/permission unverified; official Kaggle ID57690887/score0.33, author contributions, Paper Track and Moodle receipts unverified. No results or submitted artifacts were overwritten.


## E130 second review applied corrections (2026-10-27)
Details, evidence and hearing: [SECOND_ADVERSARIAL_REVIEW_E130_20261027.md](SECOND_ADVERSARIAL_REVIEW_E130_20261027.md). **Review source/PDF package actually compiled, visually checked all eight pages, 41/41 QA passed, clean ZIP rebuild text-identical, saved E126 bootstrap script executed.** No original research data or official submissions modified.
| Repair | Status | Verified action / acceptance remaining |
|---|---|---|
| RP-13 report architecture | COMPLETE in review copy | Core DQN/PPO results central; separate E126 study retained. |
| RP-14 publication source/layout | PARTIALLY COMPLETE | E130 proper Table1/figure1 order, two legible figures, eight total/seven main pages, no LaTeX errors; exact **official** 2026 style hash still unverified. |
| E130-F1 E129 caption self-reference | CLOSED | Removed opaque “E128 Table1/Fig2” source from publication caption while retaining reported-only data tier. |
| E130-F2 reported-vs-measured claims | CLOSED at language level | Removed unverified assertion that background-click failures were counted; PPO update described as reported; scorer version absence disclosed. |
| E130-F3 historic mechanism controls | CLOSED at paper-evidence level | Restored N118 corrupted-history Brier 0.162504 and E126 s5i5 step3 divergence with noncausal interpretation. |
| E130-F4 saved-statistic reproducibility | CLOSED for offline data | `scripts/verify_statistics.py` reproduces 75 matched pairs, 45 controls, 20k family CI from derived source-tagged CSV, **not** SDK replay. |
| RP-01/02/03/04/05 original coursework and DQN/PPO correctness | OPEN | No original neural training/checkpoints, 108 SDK run logs, mask probability or I2 substantive evidence recovered. |
| RP-06 learning or adaptation curve | OPEN confirmed requirement gap | No genuine budget-indexed neural learning/adaptation series. |
| RP-07/08 external submission, member contribution | OPEN | Kaggle class nomination and ID57690887 receipt, Moodle/Paper Track, real author roles not verified. |
| RP-12 pretrained components | OPEN | Full DQN offline training cost and peer CNN licence/permissions unknown. |
The judicial 55/90 provisional non-leaderboard assessment is **unchanged**; leaderboard 10 unknown. E130 is review-ready, not certified final submission.
