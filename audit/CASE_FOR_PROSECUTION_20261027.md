# CASE FOR THE PROSECUTION — COMS4061A/COMS7071A ARC-AGI-3
**Date:** 27 October 2026 (SAST)  
**Target:** Adequacy of the academic research submission as evidence for full marks, never the character or intentions of its authors.  
**Authority:** `RL_Assignment(1).pdf` pp.1–5. **Report examined:** `ARC_AGI3_E128_Revised_Research_Paper (1).pdf` pp.1–10. E127 paper itself is not separately available; do not claim direct E127 comparison. **Technical evidence:** `Stralb/arc-agi-3-rl-research`, main baseline `49b966d06afe8ee2a51da100801bf7d5ae63eebf`, `archive/full-research-2026-10-27`, existing audit ledger and six-perspective simulation. **No code execution or new native replay is claimed here.**

## Evidentiary standard
- **ESTABLISHED:** The precisely framed deficiency is directly observable in the paper, assignment or inspected primary source. It does **not** imply wrongdoing.
- **PROBABLE:** Specific evidence supports an assessment concern, but important verification remains.
- **UNRESOLVED:** Evidence does not establish whether the substantive allegation is true or false; absence from inspected GitHub is not absence from the original cluster/archive.
- **NOT SUBSTANTIATED:** The available primary sources undercut the allegation.  
No fixed per-charge mark deduction is prescribed by the lecturer; affected categories overlap, so impacts below must **not** be added together.
- **Prosecution's burden:** Prove an omission if alleging an omission. To allege a false result, broken algorithm or invalid submission, require the original run/code/platform evidence, not a missing file or chronology mismatch.

## Ranked charge register
| Rank | Charge ID | Precisely alleged deficiency | Classification | Likely affected rubric category | Priority |
|---:|---|---|---|---|---|
| 1 | CP-01 | Six-arm trained DQN/PPO claim lacks accessible end-to-end code→gradient→trace verification | UNRESOLVED | Baselines 20, improvements 25, report 10 | P0 |
| 2 | CP-02 | Reported official E126 submission and class nomination lack independently reconciled Kaggle record | UNRESOLVED | Leaderboard 10, report 10 | P0 |
| 3 | CP-03 | Mandatory contribution and external submission **evidence in assessed materials** incomplete | ESTABLISHED | Report 10, eligibility | P0 |
| 4 | CP-04 | Required learning/adaptation curves not present as such | ESTABLISHED | Rigour 25 | P0 |
| 5 | CP-05 | DQN-I2's claimed second substantive change may be conditional epsilon tuning | PROBABLE | Improvements 25 | P0 |
| 6 | CP-06 | Full 72+12+24 coursework outcome, runtime and update evidence not independently recalculated | UNRESOLVED | Baselines 20, improvements 25, rigour 25 | P0 |
| 7 | CP-07 | PPO-I2 mask-conditioned log-probability/GAE/ratio correctness not established | UNRESOLVED | Baselines 20, improvements 25 | P0 |
| 8 | CP-08 | DQN-I1 bundle does not isolate which changed component caused the gain | ESTABLISHED | Improvements 25, rigour 25 | P1 |
| 9 | CP-09 | DQN/PPO compute comparability is limited by inherited effect pretraining | ESTABLISHED | Rigour 25, report 10 | P1 |
| 10 | CP-10 | PPO-I1 novelty benefit and PPO-I2 component effects not uniquely attributable | ESTABLISHED (narrow attribution limit) | Improvements 25, rigour 25 | P1 |
| 11 | CP-11 | Small exposed-game sample cannot support an independently held-out advantage | ESTABLISHED (inference limit, not breach) | Rigour 25 | P1 |
| 12 | CP-12 | Disproportionate space for distinct N118–E126 lineage leaves coursework evidence thin | PROBABLE | Improvements 25, report 10 | P2 |

### CP-01 — Qualifying neural learners not independently verified
1. **Allegation:** The report says DQN and PPO were both genuinely trained, but the inspected GitHub snapshot does not furnish a complete original source-to-checkpoint-to-outcome chain for the six coursework stages.
2. **Authority:** Assignment p2 §3(1)–(3): two baseline learning algorithms, including one course and one outside algorithm, and two evaluated improvements each; rubric p4 “Two functioning learning baselines”.
3. **Implicated:** E128 abstract p1, §3.1 pp3–4, Table1 p4, conclusion p8; matched-study implementation apparently owner-held.
4. **Primary evidence for:** Repository `main` and research-history indexed sources focus on N093–E126; matching original E128 72-run DQN/PPO training implementation, traces and full checkpoints were not recovered during connected GitHub inspection. Original cluster paths referred to `e078_course_recovery` in historical file evidence but contents not inspected.
5. **Counterevidence:** E128 gives credible algorithm objectives, seeds, optimizer counts and concrete native wins. The paper explicitly says the evidence pack preserves matched study scripts. Repository incompleteness is documented; earlier cluster experiment directory names exist.
6. **Uncertain:** Whether the archived code contains actual online gradient updates, target network, PPO GAE and matching run files.
7. **Consequence:** Major uncertainty affecting marks for baselines, improvements and reproducibility; **not proof the algorithms were not implemented**.
8. **Dismissal test:** Obtain original six runner implementations, fixed configs, exact execution logs, network/checkpoint SHA, optimizer and parameter-delta proof, 72 records (4 games×3 policy seeds×6 arms), then independently verify a chosen native replay where SDK permits.

### CP-02 — Kaggle official record/version not independently reconciled
1. **Allegation:** The asserted official E126 public 0.33 and ID 57690887 cannot presently be tied to a successful eligible platform submission and its exact source from inspected primary evidence.
2. **Authority:** Assignment p4 Class Leaderboard: successful nominated submission by Moodle deadline, ID/score evidence and matching code; p5 §6(3): timestamp, nominated entry and Paper Track evidence.
3. **Implicated:** E128 abstract, pp7–8; `release/manifest.json`, `experiments/E126/results/E127_AUDIT.md` (archive), source `src/e126_submission_agent.py`.
4. **Primary evidence for:** E128 reports ID 57690887=0.33 as submitted on 27 Oct; repository manifest records `candidate_not_submitted` and `official_kaggle_submission=false`; archived E126 audit says no Kaggle submission as of its snapshot. No Kaggle server receipt independently inspected.
5. **Counterevidence:** The paper's specific ID, date and agent SHA `84f27a25...7005178c` are independently testable. E128 PDF was produced after the last inspected main commit, making a later real submission plausible. No source proves the server record invalid.
6. **Uncertain:** Platform submission success, timestamp in SAST, public score, accepted notebook SHA, team eligibility/nomination/class rank.
7. **Consequence:** Up to the separate 10 leaderboard marks depend on class eligibility/rank. Do **not** assume zero or score from global rank. Possible credibility issue only if original server evidence contradicts the exact claim.
8. **Dismissal test:** Genuine Kaggle submission receipt with ID, competition, scored status, official public score and timestamp; source/notebook SHA comparison to deployed artifact; class nomination and eligible team roster. Reconcile earlier snapshot chronologically.

### CP-03 — Required contribution and submission evidence incomplete in assessed dossier
1. **Allegation:** The assessed manuscript and audited repository do not yet contain a confirmed team-contribution statement or verifiable Paper Track and Moodle receipt/package; **this is a documentation deficiency, not a conclusion that nothing was submitted**.
2. **Authority:** Assignment p5 §6(1)–(3): `Kaggle-team-name.zip`, eight-page RLC PDF, source notebook, official competition evidence, Paper Track write-up link plus saved text, and brief each-member contribution statement; deadline 27 Oct 23:59 SAST.
3. **Implicated:** E128 §6 p8; `audit/SUBMISSION_CHECKLIST.md`.
4. **Primary evidence for:** E128 p8 explicitly says “Team contributions remain to be confirmed.” No official Paper Track submission receipt, complete correctly named final ZIP or Moodle confirmation was located in the audited repository snapshot.
5. **Counterevidence:** Three named authors and student emails appear; E128 PDF and E126 Kaggle notebook exist; Moodle and Kaggle are separate platforms and may already contain later receipts.
6. **Uncertain:** Actual author roles, final team registration, Paper Track success, Moodle upload, matching version and final ZIP content.
7. **Consequence:** Strong grounds to withhold *full report/reproducibility or submission-evidence credit* until artifacts are supplied; not an allegation of nonparticipation.
8. **Dismissal test:** Truthful signed-off contribution statement; exact final ZIP manifest; Paper Track URL and saved text; Moodle confirmation and timestamp; no secrets in included notebook.

### CP-04 — Genuine learning/adaptation curves are missing
1. **Allegation:** Figure2 shows cumulative native win event times within one episode, not policy performance measured over increasing learning or adaptation budget.
2. **Authority:** Assignment p3 §5 bullet 3 explicitly calls for “Learning or adaptation curves against interaction budget”; p4 rigour descriptors.
3. **Implicated:** E128 Figure2 and text p5, Table1 p4.
4. **Primary evidence for:** E128 explicitly admits “No reliable series of independently evaluated intermediate saved policy checkpoints is available ... required learning/adaptation-curve evidence remains incomplete.”
5. **Counterevidence:** Exact first native-reward timings are useful within-episode progress measurements; gradients/update counts and controlled 256-action budgets are reported. Lecturer does not say checkpoint evaluation is the only allowable form of *adaptation* curve.
6. **Uncertain:** Whether archived records allow an independently defensible within-run adaptation metric or actual checkpoint learning series.
7. **Consequence:** Established rubric omission; reasonable experimental-rigour mark reduction, **not** automatic rejection of all results.
8. **Dismissal test:** Verified performance/adaptation series across charged interactions, with clear measured quantity, matching runs/seeds, failures and source reproducibility. Do not relabel first reward timings or raw loss curves as validated improvement curves.

### CP-05 — DQN-I2 may not qualify as substantive
1. **Allegation:** The second DQN change may chiefly modify epsilon according to a fixed time-without-reward rule, a conditional hyperparameter schedule rather than a substantive exploration method.
2. **Authority:** Assignment p2 §3(4) “Merely changing hyperparameters is insufficient”; p2 two substantive improvements and evaluated stages.
3. **Implicated:** E128 §3.2 p3, Table1 p4; DQN-I2 source not located.
4. **Primary evidence for:** Paper says DQN-I2 retains I1, changes its structured explorer epsilon floor to 0.75 after 96 unrewarded actions, and preserves Bellman reward and network target. 1,769/3,072 decisions triggered the rule; level completions remain 2, equal to I1.
5. **Counterevidence:** State-dependent, measured-reward stall response differs from replacing epsilon by a single constant; meaningful adaptive exploration can earn credit without increased score. The implementation might contain additional logic not described.
6. **Uncertain:** Exact trigger, reset dynamics, action-type/click distribution, adaptation to evidence, and matched behavior versus a fixed epsilon control.
7. **Consequence:** Possible non-qualification of the second DQN improvement, impacting 25-mark iterative category. Classification **PROBABLE concern**, not proven violation.
8. **Dismissal test:** Source-level mechanistic demonstration that I2 materially changes an exploration strategy beyond nominal schedule tuning, with matched I1 vs I2 action diagnostics, a constant-epsilon control if available and actual evaluation records. If only schedule tuning, do not assert fully substantive.

### CP-06 — Exact original coursework results lack independent recomputation
1. **Allegation:** Table1/Figure2 core numbers cannot be independently verified at the native action, runtime and optimizer level from the inspected archive.
2. **Authority:** Assignment pp2–4 requires matched baseline/improvement evaluations, failure cases, native score and scoring version, resource use and reproducibility.
3. **Implicated:** E128 Table1/Fig2 pp4–5 and reported separate control archive.
4. **Primary evidence for:** No original 72 core + 12 random + 24 PPO-ablation per-episode records in inspected GitHub indexes. Numerical schedule predicts 360 DQN update opportunities per arm with 16 warmup, every eight actions, and 3072 actions (subject to actual boundary logic), while DQN-I1 Table1 reports 361. No source presently resolves one-step difference.
5. **Counterevidence:** Manuscript internal arithmetic is coherent: 6×4×3=72; +3 control groups×12=108; 12×256=3072 actions/arm. PPO 768 recorded updates is compatible with four 64-step rollouts×four epochs×four minibatches per game, although that does not prove execution. Appendix/evidence pack may contain original rows.
6. **Uncertain:** Whether DQN-I1 361 is legitimate extra flush/transition, if all 3072 charges correspond to identical protocol, exact scorer/version, stop/censor, first-reward timing and wall-time provenance.
7. **Consequence:** Unresolved outcome and comparison verification; not an identified numerical falsification.
8. **Dismissal test:** Parse every original episode and CPU/memory/task log, verify totals/means and exact first reward time, reconcile 361 vs 360 with executable code, reproduce scorer outputs with version hash, confirm no training/evaluation conflation.

### CP-07 — PPO-I2 probability/GAE correctness remains unverified
1. **Allegation:** The paper does not prove that the masked conditional click sampling distribution and old/new log-probabilities are mathematically consistent through PPO optimisation.
2. **Authority:** Assignment p2 §3(1), p4 baseline correctness (“correctly implemented”) and meaningful improvement testing; PPO clipped objective requires a valid importance ratio.
3. **Implicated:** E128 Eq(2) and §3.1–3.2 p3; stored-log-prob claim; absent original PPO implementation.
4. **Primary evidence for:** Paper reports foreground mask when modal colour≥65% and at least four other-colour click positions remain; says selected action and masked log-prob are retained but does not show invariant source/test proving rollout and update use the same conditioned action support. No original PPO source examined.
5. **Counterevidence:** Factorised `logπ(type)+1_click logπ(coordinate|type)` is mathematically valid; E128 knows the need to store masked log-prob and may implement it correctly.
6. **Uncertain:** Whether conditional support is deterministic/reconstructible at replay, whether legal type masks are consistent, and if GAE bootstraps truncated horizons correctly.
7. **Consequence:** If wrong, serious baseline/improvement validity issue. At present **UNRESOLVED**, not an established bug.
8. **Dismissal test:** Source plus deterministic unit tests comparing old log-prob collected versus recomputed before update on identical rollout data, matching masked support/entropy, finite importance ratios, correct GAE terminal/truncation, gradient parameter changes and click-action legality.

### CP-08 — DQN-I1's causal attribution is confounded
1. **Allegation:** The improvement cannot be attributed uniquely to dueling architecture, legal-candidate ranking, D14 exploration or frozen effect representation.
2. **Authority:** Assignment p2 §3(3)/(5): evidence-motivated intervention and ablations isolating main improvements; p4 clear attribution for high marks. This **does not** ban a substantive bundle.
3. **Implicated:** E128 §3.2 p3, Discussion p8.
4. **Primary evidence for:** E128 explicitly says I1 simultaneously replaces the flat head, uses D14 structured exploration and introduces external effect features. One bundled condition yielded two recorded `vc33` Level-1 wins. No isolated DQN I1 factor ablation in Table1.
5. **Counterevidence:** The report expressly identifies I1 as a package intervention and does not claim a uniquely identified component. A tested bundle may still be a valid substantive improvement; previous E014/015 studies give surrounding historical evidence.
6. **Uncertain:** Whether source archive contains additional DQN I1 component ablations, or whether practical resources allowed them.
7. **Consequence:** Established limitation on **component-level causal attribution**, not established requirement violation; full “clear attribution” marks may be withheld if overstated.
8. **Dismissal test:** Isolated version/drop-one-component ablations under same budget and training regime, or explicitly restrict claim to whole-bundle effect while preserving prior baseline motivation.

### CP-09 — Unequal total training budget
1. **Allegation:** The core comparison equalises evaluation calls but not learning opportunity or complete compute, limiting any conclusion that DQN is intrinsically better or more efficient than PPO.
2. **Authority:** Assignment p3 §4(5): fair comparisons on same games and comparable interaction/compute budgets; report training cost separately; disclose and justify unequal budgets.
3. **Implicated:** E128 §4 Table1 pp4–5, §6 p8; DQN-I1 pretrained frozen effect encoder; `release/e126_template.py` applies to later *separate* CNN and must not be conflated with the DQN-I1 encoder.
4. **Primary evidence for:** E128 states DQN-I1/I2 inherit an externally pretrained effect encoder; PPO learns from current runs; Table1 runtime explicitly excludes prior training. This is a genuine unequal all-in budget.
5. **Counterevidence:** The unequal pretraining is disclosed plainly, and same native evaluation game/seed/action ceilings provide a useful *deployment budget* comparison. The lecturer permits unequal budgets if disclosed and justified.
6. **Uncertain:** Exact pretrained feature data exposure, steps/hardware, licence, and whether reported downstream inference overhead is complete.
7. **Consequence:** Established **comparability limitation**, not a concealment or automatic disqualification. Full rigour/efficiency marks may require cost/accounting and narrower claims.
8. **Dismissal test:** Provenance and cost table separating pretrained model learning, online task training and scoring inference, frozen-effect source/checkpoint checksum/licence, justified comparison target.

### CP-10 — PPO novelty and mask components lack unique treatment attribution
1. **Allegation:** The one PPO-I2 win does not demonstrate incremental value from PPO-I1 novelty; evidence for mask-specific improvement remains thin.
2. **Authority:** Assignment p2 §3(3)/(5): iterative motivation, individual evaluation, ablations isolating main effects; p4 experimental rigour.
3. **Implicated:** E128 §3.2, Table1, Figure2 and paragraph following p5.
4. **Primary evidence for:** PPO V0=0, PPO I1=0, PPO I2=1; a mask-only control also records one `s5i5` win at policy seed302. Updates-disabled control reports zero. The mask-only win has **no recorded first-reward step** in Figure2; original control traces absent.
5. **Counterevidence:** E128 **already concludes** that novelty was not required for that case and avoids claiming a reliable mask main effect. A negative novelty experiment is valuable and can count as a properly tested improvement.
6. **Uncertain:** Whether full PPO control runner preserves all other settings, if mask-only updates equal I2 updates, raw success trajectory and confidence over seeds.
7. **Consequence:** Established narrow attribution limitation; not proof of an invalid algorithm or an impermissible negative result. Weakens high-confidence evidence of additive effects.
8. **Dismissal test:** Recover full per-run controls with exact same seeded protocol, inspect no-novelty vs novelty-only vs mask-only vs combined actions, log-prob/gradient correctness, first-reward action or documented missing-timestamp reason.

### CP-11 — Small exposed-family sample cannot prove held-out generalisation
1. **Allegation:** The data do not identify broad unseen-game advantage or robust superiority, and should not be used to support either.
2. **Authority:** Assignment p2 §3(5) asks for comparison of ability to adapt to held-out environments; p3 §4(3) says split where public set permits, disclose exposure, avoid claims of generalisation after repeated testing; p4 rigour requires conclusions supported by results.
3. **Implicated:** E128 §4/5/6; `results/e126_per_game.csv` and archived `experiments/E126/results/integrated_audit.json`.
4. **Primary evidence for:** Core study has four exposed families and three fixed native-layout policy seeds, with all five successes in three distinct game-seed cells. E126 has 25 exposed families, 28/75 changed trajectories, six score-positive pairs, four extra levels all from two families; family-bootstrap interval [0,.386] includes zero. `s5i5` supplies 68.54% of E126 positive local score difference.
5. **Counterevidence:** E128 explicitly and repeatedly disclaims unseen-game transfer, notes exposure and selection, and says modest score improvement on public tests only. Three stochastic seeds exist as reported, even though they do not create independent game layouts. Assignment allows limitations where split unavailable.
6. **Uncertain:** Existence of untouched environments at experiment-design time, the degree of model exposure before selection, original exact family split and prospective tests.
7. **Consequence:** **ESTABLISHED inference limitation, NOT an established coursework breach or proof of low research quality.** An honestly presented negative/sparse result need not cost marks by itself; generalisation analysis can still be strong if limitations are rigorous.
8. **Dismissal test:** A genuinely untouched, predeclared family/test split with frozen methods, compute and thresholds, matched comparisons and uncertainty. Short of this, maintain narrow descriptive claims.

### CP-12 — Non-coursework E126 dominates narrative relative to course-critical evidence
1. **Allegation:** A separate later empirical-controller study consumes a substantial proportion of an eight-page main paper while the central six DQN/PPO agents have incomplete curves and weaker trace-level exposition.
2. **Authority:** Assignment p5: self-contained eight-page main with essential evidence; pp2–4 focus on two learning agents, two successive improvements each, evaluation and ablations. No requirement forbids later research.
3. **Implicated:** E128 §§1–4 pp1–5 versus §5, parts §6 pp5–8; four figures; N118–E126 materials.
4. **Primary evidence for:** §5 supplies longer mechanistic evidence on N118, N119, N120, N093→E126 and Figure3/4, whereas six-course-stage source/curve evidence remains incomplete. Distinct 4-family/256 action vs 25-family/200-per-level (historical N-series) protocols cannot be pooled. Table2 documents different controller lineage.
5. **Counterevidence:** The manuscript explicitly separates algorithm lineages (Figure1, §§1–2), E126 is the deployed competition candidate and directly supports thesis, and its E126 records are substantially more auditable than core DQN/PPO records. Reporting advanced separate experiments can improve scientific quality.
6. **Uncertain:** Whether recoverable course evidence would materially rebalance eight-page content and whether lecturers value full separate deployed-contest description.
7. **Consequence:** **PROBABLE presentation and rubric-weighting concern**, not a technical violation. Risk of losing clarity/reproducibility points by underprioritising core grading evidence.
8. **Dismissal test:** Demonstrate the eight-page report already contains every essential course evidence component or present a verified page-allocation plan that foregrounds them without dropping supported E126 contribution. No immediate rewrite authorised.

## Allegations that SHOULD NOT be pressed without new evidence
- **Falsehood, plagiarism or misconduct:** NOT SUBSTANTIATED. A source-availability gap and two snapshots disagreeing on Kaggle status do not establish deliberate wrongdoing.
- **E126 is a DQN/PPO ensemble:** NOT SUBSTANTIATED, and contradicted by source: inherited N093/N117 empirical Bellman controller, frozen pretrained neural priors, no PPO acting network. E128 expressly corrects this.
- **Visible changes are counted as native wins:** NOT SUBSTANTIATED. E128 differentiates changed pixels, action divergence, local SDK score, native level advancement and official Kaggle public score.
- **Sparse or negative RL outcomes themselves violate the assignment:** NOT SUBSTANTIATED. Lecturer p2 explicitly values tested and analysed unsuccessful improvements.
- **No held-out evidence automatically violates the instruction:** NOT SUBSTANTIATED as categorical allegation. Lecturer asks separation where available and truthful disclosure; E128 acknowledges all public-game exposure.

## Prosecutorial disposition
The most serious *established report defect* is the missing required learning/adaptation curve (CP-04); the most serious *unresolved technical question* is actual six-arm DQN/PPO reproducibility (CP-01, CP-06, CP-07). DQN-I2 (CP-05) is a **probable borderline improvement**, not a proven nonqualifier. Unequal pretraining and bundled changes (CP-08/09) are admitted limitations; legal submission evidence (CP-02/03) requires primary platform records rather than assumptions. The original non-leaderboard **55/90** assessment was provisional, not a statutory deduction or evidence of unperformed experiments; retain uncertainty until the original source and Kaggle receipts are inspected.

**Minimum dismissal package before full-credit claim:** (i) complete six-arm source + hash/config + raw run/replay + optimiser evidence and versioned scorer, (ii) genuine budget-indexed adaptation/learning measurement, (iii) DQN-I2 source-level mechanism classification and PPO mask probability check, (iv) honest all-in pretraining cost and causal limitations, and (v) verifiable Kaggle, Paper Track, Moodle and contributions records. Preserve original paper and research artifacts until forensic closure.
