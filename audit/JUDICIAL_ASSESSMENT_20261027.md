# PRESIDING JUDGE — EVIDENCE-BASED ACADEMIC ASSESSMENT

**Date:** 2026-10-27 SAST. **Report assessed:** uploaded `ARC_AGI3_E128_Revised_Research_Paper (1).pdf` (eight pages main + two pages references), not separately available E127. **Authority:** uploaded `RL_Assignment(1).pdf` pp.1–5, especially §3, §4, §5 rubric and §6. **Research source:** `Stralb/arc-agi-3-rl-research` main baseline `49b966d06afe8ee2a51da100801bf7d5ae63eebf`, `archive/full-research-2026-10-27`. **Companion evidence:** [ledger](EVIDENCE_LEDGER.md), [repair register](REPAIR_REGISTER.md), [prosecution](CASE_FOR_PROSECUTION_20261027.md), [defence](CASE_FOR_DEFENCE_20261027.md), [cross-examination](SCIENTIFIC_CROSS_EXAMINATION_20261027.md).

**This is an evidence-weighted provisional assessment, not an official lecturer mark or a fresh native run.** 10 class leaderboard marks are excluded because eligible class-team ranking and official nomination were not verified. Disposition meanings: SUSTAINED = established material defect; PARTIALLY SUSTAINED = narrower established evidentiary/assessment limitation but broader allegation not proved; DISMISSED = allegation of breached requirement/unsupported claim not supported; INSUFFICIENT EVIDENCE = decisive primary source unavailable. Overlapping charges never imply additive point deductions.

## 1. Findings of fact

- Lecturer requires two genuinely trained algorithms, baseline and two substantive evaluated improvements for each, a random/inexpensive sanity reference, fair protocol, native official-method score, failures, 3 independent stochastic seeds (or justified limits), learning or adaptation curves, proper resource accounting and original submission evidence; honest negative experiments can earn marks (§3–6).
- E128 reports 72 coursework runs (four historically exposed families ×3 policy seeds×6 arms), with DQN completion counts 0/2/2 and PPO 0/0/1; random 12 and PPO controls 24; implementation and original per-run execution are UNVERIFIED, not contradicted.
- E128 itself admits no proper learning/adaptation curves, and p8 contributor roles remain unconfirmed. E128 has eight main pages/two references; RLC exact LaTeX source parity not established.
- Source inspection verifies N093 optimistic empirical Bellman/PUCT, N117 local effects and E126 inherited frozen CNN click ranking, not a DQN/PPO ensemble. Main source/checkpoint/table verification is NOT original SDK replay.
- E126 saved CSVs were independently reaggregated: 1125 recorded episodes, 125220 counted actions across 45 arms, local three-seed means 2.081484 (N117) vs 2.225399 (E126), 28 changed matched trajectories, six positive local score game–seed pairs and four additional levels across s5i5/lf52. These cannot establish hidden generalisation.
- Reported Kaggle E126 submission ID 57690887=0.33 is unverified from the Kaggle platform; earlier GitHub manifest marks candidate not submitted, possibly before a later submission. No misconduct conclusion follows.

## 2. Rulings on prosecution charges

| Charge | Ruling | Evidence determining ruling | Evidence that could change it |
|---|---|---|---|
| **CP-01** | **INSUFFICIENT EVIDENCE** | Whether both reported coursework agents were genuinely and correctly trained cannot be adjudicated from the curated N-series/E126 GitHub tree. E128 §3 describes Double DQN/PPO and reports updates, but the original six-arm source and associated optimizer traces remain unrecovered. An access gap is verified, not a failed implementation. | Find six exact stage scripts, frozen configs, checkpoint SHA, gradients/parameter deltas and source-linked native episodes. |
| **CP-02** | **INSUFFICIENT EVIDENCE** | E128 p7 reports official E126 Kaggle ID 57690887 and 0.33; main release/manifest.json asserts its earlier candidate was not submitted. E128 postdates that GitHub snapshot. A later successful submission is possible, but no authenticated Kaggle receipt or class nomination was retrieved. | Official successful submission ID/timestamp/score, source notebook hash, nomination, eligible class-team rank. |
| **CP-03** | **PARTIALLY SUSTAINED** | E128 p8 explicitly leaves individual team contributions unconfirmed, a lecturer §6 requirement. Missing external Moodle/Paper Track receipts from the inspected GitHub repository does not prove those submissions failed. | Truthful per-author contributions; exact final ZIP/notebook, Paper Track link and text, Moodle receipts. |
| **CP-04** | **SUSTAINED** | Lecturer §5 p3 explicitly requires learning OR adaptation curves against interaction budget. E128 Fig2 p5 is first-native-reward-event timing, and the paper itself states the required evidence remains incomplete. | Real logged budget-indexed learning or adaptation performance curves; otherwise truthful limitation and accept scoring exposure. |
| **CP-05** | **INSUFFICIENT EVIDENCE** | E128 describes epsilon floor 0.75 after 96 unrewarded actions and reports 1769/3072 active decisions, but no actual DQN-I2 source or paired decision log was recovered. Conditional schedules may be substantive depending on mechanism, or merely tuning; unchanged completions do not decide it. | Inspect actual trigger, state, reset and choice code; matched I1/I2 decisions and epsilon-only control if possible. |
| **CP-06** | **PARTIALLY SUSTAINED** | The audit cannot independently recompute 72 core + 12 random + 24 PPO control original SDK episodes, timing and updates from the public snapshot. Manuscript totals are internally coherent; DQN I1 361 vs baseline 360 updates needs code-level explanation. This is a reproducibility gap, not proof of invalid numeric values. | Acquire 108 per-run records, raw reward/actions, scorer version, wall-time records, optimizer events; independently recompute Table1/Fig2. |
| **CP-07** | **INSUFFICIENT EVIDENCE** | PPO mask inconsistency is a legitimate potential failure mode, but E128 correctly states factorised action probabilities and stored masked old log-probability; original code was not located and no defect was demonstrated. | Unit-test masked old/new log-prob, legal support, entropy, GAE bootstrap and PPO gradient/parameter change. |
| **CP-08** | **PARTIALLY SUSTAINED** | E128 explicitly combines legal candidate ranking, D14 exploration, dueling scoring and effect features in DQN-I1. No component-level causal identification follows from a single bundle treatment; the lecturer does not prohibit an evaluated bundle as one substantive change. | Limit causal claim to I1 entire package or supply real isolated ablations. |
| **CP-09** | **PARTIALLY SUSTAINED** | E128 §4 reports matched 4-game × 3-seed × 256-action in-run ceilings, but DQN I1/I2 use an externally pretrained representation and the table excludes its earlier training cost. This inequality is disclosed and permitted if justified, but total learning compute/exposure cannot be compared as equal. | Document prior training data, cost, provenance, and separately reported online training and inference/evaluation budgets. |
| **CP-10** | **PARTIALLY SUSTAINED** | As reported, the PPO mask-only arm reproduces the sole PPO-I2 success, so novelty is not necessary for that case. The paper says so and reports the negative PPO-I1 result. However, a single control success does not identify broad mask effects and original PPO control trajectories are unverified. | Recover original mask-only/novelty-only/full/no-updates controls; test masked ratio and restrict conclusion to observed game/seed. |
| **CP-11** | **DISMISSED** | As a charge that the report improperly claims unseen-game generalisation or violates leakage disclosure, the objection fails: E128 §§4–6 openly identifies historically exposed families, fixed layouts, post hoc gate, zero-inclusive bootstrap interval and no unseen generalisation. The small exposed sample remains a legitimate limitation relevant to rigour, not a false claim or automatic rule breach. | No retrospective data can prove unseen transfer. Keep cautious interpretation; prospectively frozen new-game study only if available and compliant. |
| **CP-12** | **PARTIALLY SUSTAINED** | E128 devotes material space to distinct N118–E126 mechanisms while required DQN/PPO curves and primary run provenance remain thin. Nevertheless E126 is a pertinent final competition controller with independently auditable source/tables and an explicitly separate lineage. The concern is rubric emphasis, not scientific irrelevance. | Once coursework evidence is recovered, prioritise it within eight main pages while retaining concise, truthful E126 controls. |

## 3. Non-leaderboard rubric assessment

| Lecturer category | Provisional mark | Plausible range | Judicial rationale |
|---|---:|---:|---|
| Problem formulation and understanding | **8/10** | 7–9/10 | Accurate POMDP, legal-action and reward distinctions, Double DQN/PPO equations, prior work. Minor action/reset/specification details and implementation linkage remain unverified. |
| Baseline implementation and evaluation | **11/20** | 7–17/20 | Six-arm baseline and random control are clearly reported, but source, gradient updates and original 108 episodes have not been independently inspected. |
| Iterative improvements | **14/25** | 11–20/25 | Four named, evaluated interventions with negative results; no unique DQN-I1 component effects, DQN-I2 substantive classification unresolved, PPO controls raw evidence unavailable. |
| Experimental rigour and analysis | **15/25** | 12–19/25 | Matched reported actions/seeds, visible failures, careful uncertainty/exposure disclosure and E126 saved arithmetic; missing proper curves, tiny positive sample, unequal pretraining and unverified core logs. |
| Report quality and reproducibility | **7/10** | 5–8/10 | Clear eight-page technical report and references; template/build source, original coursework reproduction and individual contributions/submission evidence incomplete. |

**TOTAL: 55/90** (evidence-weighted range **42–73/90**). Category lower endpoints sum to 42 and upper endpoints to 73; this is an uncertainty interval for plausible lecturer scoring, **not** a sampling confidence interval. The unknown leaderboard 10 marks remain **UNSCORED**, not zero, and the worldwide Kaggle score does not directly determine them.

## 4. Sustained deficiencies and dismissed objections

- **Sustained:** Missing authentic budget-indexed learning/adaptation curve (CP-04).
- **Partially sustained:** Unconfirmed contributor statement and missing supporting external records in inspected dossier (CP-03); inaccessible original core numerical source (CP-06); bundle confounding (CP-08); unequal pretraining/compute scope (CP-09); limited PPO component attribution (CP-10); course-vs-E126 report emphasis (CP-12).
- **Dismissed as a grading violation or unsupported claim:** CP-11 allegation of falsely implying held-out generalisation; paper openly disclaims it. Also dismiss any unsupported extrapolation that low scores violate the assignment, that E126 is a DQN/PPO ensemble, or that unavailable public files establish fabrication/nonexecution.
- **Insufficient evidence:** actual course learner correctness CP-01, official Kaggle platform success CP-02, DQN-I2 substantive code CP-05, PPO-I2 masked-ratio correctness CP-07.
- **Confirmed DQN/PPO implementation defects:** **NONE** demonstrated; their source still not independently inspected. No definite misconduct finding.

## 5. Genuine strengths retained

1. Correctly framed POMDP and separation of pixel change, intrinsic training reward, Bellman reward, local SDK score and Kaggle public score.
2. Both algorithm families, baseline/improvement sequencing, fixed action budgets and full negative outcomes visibly reported.
3. Negative controls and honest interpretations, including the PPO mask-only ablation and N118 prediction-vs-progress contradiction.
4. Source-supported N093→N117→E126 architecture with frozen weights, exact source/notebook hashes and multiple control arms.
5. Explicit disclosure of exposed games, concentrated successes, confounded components, zero-including interval and no new-game generalisation.

## 6. Eight highest-impact lawful corrections (without fabricating results)

1. **P0:** Recover/verify genuine original DQN/PPO six-stage source, exact configs/checkpoints, per-run 72 core +12 random +24 control episodes, native scorer version, gradients and trace-to-table reconciliation. If unavailable, document limits and narrow claims.
2. **P0:** Inspect DQN-I2 exact conditional exploration code and matched choice logs. Determine whether it is a substantive mechanism or conditional epsilon schedule; do not overstate qualification. Use an existing separately evaluated substantive DQN change only if genuinely evidenced.
3. **P0:** Audit PPO-I2 old/new log-prob under identical foreground support, click/legal normalization, GAE terminal/truncation rules and actual optimizer deltas; verify mask-only source/controls.
4. **P0:** Recover real learning/adaptation performance against interaction budget; if no valid underlying series, preserve the omission rather than relabel first-reward timing.
5. **P0:** Authenticate the official Kaggle ID57690887 scored result, accepted source SHA and timestamp, class nominated eligible submission/team; do not conflate with the saved local SDK mean.
6. **P0:** Finalize truthful individual team contributions, exact source notebook and correctly named Moodle ZIP, Paper Track URL and saved short text, real submission receipts; inspect credentials.
7. **P1:** Source and license the reused pretrained representations/peer CNN and record offline pretraining data/compute separate from online task updates and evaluation walltime.
8. **P1:** After evidence recovery, make only evidence-supported presentation changes: foreground core course comparison/ablations/legible budget plots, state DQN-I1 as a bundle, keep narrow failures and explicit independent E126 provenance within eight main pages.

## 7. Readiness verdict

**Research manuscript: substantive, scientifically cautious and structurally aligned, but NOT YET EVIDENCE-VERIFIED FOR FULL-CREDIT SUBMISSION.** The central unresolved risk is whether original six-stage DQN/PPO implementations/108 run logs substantiate the report, not whether the best controller achieves a higher leaderboard number. **Course logistics: completion/receipts unverified**; their absence from GitHub must not be conflated with failure to submit. **Scientific publication: development-exposed mechanistic case study only; no independently established unseen-game transfer.** No report, code, checkpoint or original experimental data was modified by this judgment.
