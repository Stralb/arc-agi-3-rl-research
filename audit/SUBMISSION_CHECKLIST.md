# SUBMISSION_CHECKLIST — initial E128 audit (2026-10-27)
Course: COMS4061A/COMS7071A. Authoritative deadline 27 October 2026, 23:59 SAST.
This is a traceable **audit**, not a claim that Moodle, Kaggle or Paper Track submissions were performed. Base `main@49b966d06afe8ee2a51da100801bf7d5ae63eebf`.
Key: VERIFIED, SUPPORTED BUT LIMITED, UNVERIFIED, CONTRADICTED, MISSING. All external submission statuses require genuine platform evidence.

| ID | Lecturer requirement / artifact | Status | Evidence and next check |
|---|---|---|---|
| SC-001 | Team size <= 4, report author names/student-number emails | VERIFIED for report list | E128 lists three authors and student emails; check actual Kaggle team membership. |
| SC-002 | Report maximum 8 pages of main content, references excluded | VERIFIED as page count | E128 10 physical pages: 8 main + 2 references. |
| SC-003 | Official RLC 2026 LaTeX template, cover disabled, fonts/margins unchanged | UNVERIFIED | PDF visually formatted but exact LaTeX source/build not located. |
| SC-004 | Clear POMDP/MDP formulation, legal action/observation/reward/termination | VERIFIED in report description | E128 pp. 2–3; source implementation consistency still requires deeper check. |
| SC-005 | One course algorithm DQN and a distinct non-course PPO genuinely trained | UNVERIFIED in raw execution | E128 reports gradient updates and objectives; original matched scripts/logs/checkpoints not yet located. |
| SC-006 | DQN baseline + two substantive separately evaluated modifications | UNVERIFIED in raw execution | Report V0/I1/I2, scores 0/2/2; need source and native run records. |
| SC-007 | PPO baseline + two substantive separately evaluated modifications | UNVERIFIED in raw execution | Report V0/I1/I2, scores 0/0/1; need source, GAE/ratio implementation and native run records. |
| SC-008 | Reproducible random action baseline sanity check | UNVERIFIED in raw execution | Report 12 random native episodes; needs records/source. |
| SC-009 | Same games/seeds/action budgets and disclosed training cost | SUPPORTED BUT LIMITED | E128 states 4 games × 3 policy seeds × 256 calls, but DQN-I1 pretrained encoder and full training cost excluded. |
| SC-010 | Native official-style score distinct from shaped training reward | VERIFIED in paper; execution unverified | PPO intrinsic bonus explicitly separated; E126 SDK vs Kaggle distinguished conceptually. |
| SC-011 | Level completions and actions including failures, variability >=3 seeds | SUPPORTED BUT LIMITED | E128 summary and exact outcome figure; core raw source data unverified. |
| SC-012 | Learning or adaptation curves against interaction budget | MISSING/incomplete | E128 expressly says not a real checkpoint learning curve. |
| SC-013 | Ablations isolating major improvements | SUPPORTED BUT LIMITED | PPO mask-only/no-update reported; N117/E126 tables available; DQN-I1 bundled changes not isolated. |
| SC-014 | Runtime, hardware, update counts and fair resource comparison | SUPPORTED BUT LIMITED | E128 Table 1 reports task in-run wall time, updates and CPU resources; pretrained cost absent. |
| SC-015 | Train/development vs held-out exposure honesty | VERIFIED disclosure | E128 says public games previously exposed, no unseen-game generalization claim. |
| SC-016 | Clearly separate DQN/PPO and E126 lineage | VERIFIED in paper and E126 extension source | E128 Fig. 1, E126 code. |
| SC-017 | Citations, pretrained checkpoint origin, reused code attribution | UNVERIFIED full compliance | Paper cites relevant literature but permission/license still unresolved. |
| SC-018 | Original report PDF included in Moodle ZIP `Kaggle-team-name.zip` | MISSING confirmation | User-uploaded E128 PDF exists; final named ZIP and Moodle receipt not verified. |
| SC-019 | Executable Kaggle notebook code, no secrets | SUPPORTED BUT LIMITED | Main E126 notebook exists and deterministic builder present; official rerun not verified. |
| SC-020 | One eligible official Kaggle code submission by deadline, ID/score/time | CONTRADICTED/UNRESOLVED | E128 reports E126 ID 57690887, score 0.33; repo release manifest claims unsubmitted. Obtain platform evidence. |
| SC-021 | Class leaderboard nominated entry and matching code on Moodle | MISSING | No nomination or Moodle receipt located. |
| SC-022 | Paper Track write-up link and saved submitted text (<1500 words) | MISSING | No specific submission receipt/link verified. |
| SC-023 | Each member's contribution statement | MISSING | E128 explicitly says unconfirmed. |
| SC-024 | End-to-end reproducibility with SDK versions, resets, checkpoints, scripts and log provenance | SUPPORTED BUT LIMITED | Repo hashes/runner code/CSV; original SDK/traces held outside public GitHub. |
| SC-025 | Submission matches what linked code demonstrates | UNVERIFIED | E128 may describe later E126 submission; reconcile platform record with SHA. |

**Deadline priority:** SC-020/21/22 and SC-018/23, then SC-005/06/07 original evidence recovery, then other methodological completeness. Never claim an official submission without platform receipt.

## Requirement matrix reference — 2026-10-27
The assignment was re-read in full, including restrictions, official scoring, qualitative rubric bands and leaderboard formula. Full 44-line classification and the provisional **55/90** (uncertainty 42–73) are in [REQUIREMENT_TO_EVIDENCE_MATRIX.md](REQUIREMENT_TO_EVIDENCE_MATRIX.md).
- Course deadline: 27 October 2026, 23:59 SAST.
- Main body maximum 8 pages; bibliography and optional post-reference supplemental pages excluded, but required evidence must be in the body.
- Leaderboard: official public score of nominated eligible class-team code submission by deadline; `10*(N-r)/(N-1)` for N>1; all tied get 10; missing/invalid 0; valid zero-score remains eligible. **Unknown, not presumed zero.**
- RLC 2026 official template / disabled cover / unchanged fonts,margins,spacing; `Kaggle-team-name.zip` PDF+matching notebook+evidence+team roles; Paper Track writeup link and saved text; no credentials.
- E128 paper is available; named E127 PDF unavailable in inspected user attachments. No direct version comparison asserted.

## Forensic source-status update — 2026-10-27
Read [FORENSIC_CODE_AND_RESULTS_AUDIT.md](FORENSIC_CODE_AND_RESULTS_AUDIT.md) for 30 claim-specific checks.
- Six-arm DQN/PPO source and per-episode gradient logs: **UNVERIFIED**; do not count N093/N117/E126 as PPO.
- DQN I2 substantive-improvement qualification: **OPEN** pending actual code; current described conditional epsilon escalation is borderline.
- PPO I2 masked-ratio mathematical correctness: **OPEN** pending actual rollout implementation.
- Exact 3,072 recorded SDK calls per arm, DQN-I1 361 vs expected simple schedule 360: **OPEN** reconciliation; manuscript arithmetic alone passes.
- E126 28 changed trajectories, 6 score-gaining pairs, 4 levels, 8,632 actions and reported mean SDK gain: **VERIFIED saved-table arithmetic**; native replay, hidden generalisation and official Kaggle score remain unverified.
- Kaggle platform receipt for E126 ID57690887: **UNVERIFIED**; later paper and earlier not-submitted manifest disagree but may reflect different timestamps.

## Six-perspective review note — 2026-10-27
[Full six-review record](SIX_PERSPECTIVE_TRIBUNAL_20261027.md). All earlier mandatory checks remain open/closed as previously recorded; **no new lecturer requirements were invented**.
- VERIFIED from PDF: Eight main pages, two reference pages; RLC exact source/template still UNVERIFIED.
- VERIFIED omission: Figure 2 is acknowledged as first-reward timing, not full checkpoint learning curves.
- UNVERIFIED: raw six-arm coursework training and evaluation runs; correctness of PPO masked log-probs and DQN-I2 mechanism.
- UNVERIFIED/CONTRADICTED across snapshots: E126 official Kaggle ID 57690887 and 0.33 must be independently confirmed; earlier manifest predates possible submission.
- MISSING: actual contribution statement, Paper Track and Moodle success receipts, class nominated rank.

## Assessment follow-up (27 October 2026)
Full 12-item academic assessment case: [CASE_FOR_PROSECUTION_20261027.md](CASE_FOR_PROSECUTION_20261027.md).
- Learning or adaptation curves: incomplete in E128; source recovery remains open.
- Coursework DQN/PPO code and original episode records: verification pending.
- Official Kaggle version and class nomination: platform confirmation pending.
- Team contribution statement, Paper Track record and Moodle receipt: follow-up pending.
- No report, checkpoint or experimental result was changed during this review.

## Defence brief checkpoint — 2026-10-27
[CASE_FOR_DEFENCE_20261027.md](CASE_FOR_DEFENCE_20261027.md) cross-references all twelve original charges. No submission confirmations were obtained or asserted by this defence. The verified source subset and historical manifest remain distinct from original cluster evidence and official platform records. Missing learning/adaptation curves and confirmed contribution statements remain open. All initial course requirements and deadline statuses are unchanged.

## Cross-examination checkpoint — 2026-10-27
[Formal moderator rulings](SCIENTIFIC_CROSS_EXAMINATION_20261027.md). Confirmed report deficit: full learning/adaptation curve. Confirmed paper placeholder: actual contribution statement. Course DQN/PPO verification and Kaggle class nomination remain open, not proved absent. No class leaderboard marks assigned. No source/experiment/paper rewrite or submission was performed.


## Judicial readiness checkpoint — 2026-10-27
[Final judicial assessment](JUDICIAL_ASSESSMENT_20261027.md) rates the **non-leaderboard** submission provisionally 55/90 (plausible 42–73/90; not official marks). **Leaderboard 10 remains unscored** pending nominated eligible class rank and authenticated Kaggle entry. Original six-arm source and 108 episode records: unverified. Learning/adaptation curves: confirmed incomplete. Actual contribution statement: confirmed unfinished in manuscript. Paper Track, Moodle, Kaggle external platform records: not independently checked. No paper/research modifications or platform submissions occurred in the audit.


## Deadline-focused repair queue — 27 October 2026
[15-task repair plan](REPAIR_PLAN_20261027.md) starts with source recovery instead of large retraining. Required artifacts not verified remain OPEN: original DQN/PPO core/control evidence, genuine curves, the later E126 official Kaggle platform receipt and nomination, real individual contributions, Paper Track records, Moodle ZIP and exact E128 LaTeX source. E126 local saved scores are not the class leaderboard score. No manuscript or actual competition entry was submitted or altered by creating the plan.


## Executed experimental evidence checkpoint — 2026-10-27
[Offline analysis execution record](EXECUTED_EXPERIMENTAL_ANALYSIS_20261027.md) documents **14 passing tests, five generated candidate figures, E126 saved-data arithmetic verification and all 108 paper-reported coursework outcome cells preserved**. Original coursework source/logs and genuine learning/adaptation curves remain UNVERIFIED/MISSING; native SDK was not replayed. Official Kaggle ID57690887/0.33, class team rank, Moodle, Paper Track and author contributions remain open. No submitted report was modified; figures are candidates, not inserted. Do not treat new analysis package as proof of verified DQN/PPO training.


## Manuscript-architecture check (2026-10-27)
[Proposed layout](REPORT_ARCHITECTURE_20261027.md) budgets exactly eight main-page equivalents and references afterward. It explicitly preserves all mandated coursework sections and locates separate E126 extension. Official RLJ/RLC 2026 template and disabled cover must be verified from **actual compiling source**, not an unrelated general template; do not shrink template fonts/margins. Original six-arm DQN/PPO source, genuine learning curve, author contribution statement, Paper Track, Kaggle server record and Moodle receipts remain open. No report text modified by this architecture plan.


## E129 review compilation checkpoint — 27 October 2026
Reviewed LaTeX/PDF source package created: seven physical pages, two primary figures, two tables, **no cover page**, RLJ/RLC 2026.1 style copy, 33/33 QA checks and independent clean-folder build with identical extracted PDF text. This is **not a certification of actual lecturer official style byte parity** (original E128 .tex and authoritative downloadable style unavailable) or of official submission. The paper openly retains missing neural learning/adaptation curves, unavailable original DQN/PPO 108-run source/logs, unverified DQN-I2/PPO masked updates, author contributions, pretrained rights, and official Kaggle/Paper Track/Moodle receipts. No external upload or model training was carried out.


## E130 verified review build (2026-10-27)
[Second-review result](SECOND_ADVERSARIAL_REVIEW_E130_20261027.md) and the generated E130 package provide reviewed/compiled LaTeX, 8 physical pages (7 main before references), default 2026.1 style copy without cover, two figures/tables, 41/41 QA, identical clean-room rebuild text, and source-tagged saved E126 arithmetic with bootstrap. These do **not** constitute official template byte verification, neural DQN/PPO source replay, a real learning curve, completed contributions, or Kaggle/Paper Track/Moodle submissions. Those requirements remain OPEN; leaderboard class mark not inferred.

## E131 urgent report (2026-10-27)
Compiled 8 total pages with references on p8; included RLJ/RLC 2026.1 style copy and commented-out cover, 36/36 manuscript/figure/citation/data QA checks, E129 original files preserved in delivery ZIP. Actual official lecturer style identity unverified. Main coursework performance figures are from documented contemporary report results and NOT independent SDK replay; true checkpoint/adaptation curve still missing. Individual contributions, official Kaggle receipt/class rank, Paper Track and Moodle records remain OPEN. See [execution record](E131_URGENT_REWRITE_20261027.md).

## E132 figures status — 2026-10-27
Three required *native-progress-versus-interaction-budget* displays added and verified in E132 PDF, with exact 12-run denominator and no synthetic events. They are explicitly NOT verified checkpoint-learning curves, and separate lecturer learning/adaptation-evidence requirement remains only partially addressed. Paper uses included RLJ 2026.1 review style copy, eight main pages/references p9; original E129/E131 files preserved. See [E132 record](E132_THREE_NATIVE_CURVES_20261027.md). Official lecturer style SHA, team contributions and platform submissions remain unresolved.

## E133 review-copy check (2026-10-27)
[Compiled results revision](E133_RESULTS_DISCUSSION_20261027.md): E133 PDF, LaTeX and zip, nine physical pages with references starting page eight; main body within eight pages; included 2026.1 style copy cover disabled; 45/45 curve tests and 61/61 manuscript QA with clean rebuild match. This is a technically verified review artifact, **not** independently verified course training, official template identity or official competition/Moodle/Paper Track submission. Actual contribution statement and Kaggle class rank remain pending.
