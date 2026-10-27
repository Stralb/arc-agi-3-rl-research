# EVIDENCE_LEDGER — ARC-AGI-3 (initial E128 audit)
Date: 2026-10-27 SAST. Phase: source inventory and evidence hierarchy, **not a fresh training/evaluation run**.
Baseline Git revision: `main@49b966d06afe8ee2a51da100801bf7d5ae63eebf`.
Research history branch: `archive/full-research-2026-10-27`.
Paper under review: user-supplied `ARC_AGI3_E128_Revised_Research_Paper (1).pdf` (10 physical pages: eight main pages + two reference pages).
Lecturer specification: user-supplied `RL_Assignment(1).pdf` (five pages; 27 October 2026, 23:59 SAST).

**Vocabulary:** VERIFIED = directly observed in source/file or independently recalculated from source data; not synonymous with native environment replay. SUPPORTED BUT LIMITED = documented by historical results/code, but independent execution or scope is limited. UNVERIFIED = asserted but primary evidence not yet obtained. CONTRADICTED = available sources disagree or direct code conflicts; reconcile version/timestamps. MISSING = required artifact/record not found in the inspected repository snapshot; may exist in owner-held archives.

## Evidence hierarchy
1. **H1:** Official Kaggle submission run ID, associated source artifact/commit, timestamp, returned score, and saved response, if independently accessible. A named ID in a PDF is not H1.
2. **H2:** Original native SDK run logs/traces, observed frames/legal actions, native progress, seed/config, input/output hashes, checkpoints; ideally independently replayed, on fixed protocol.
3. **H3:** Native source/runner + checkpoint + replay instructions + hashes; same-episode independent replay when authorized SDK present.
4. **H4:** Raw per-game or per-seed CSV/JSON aggregated and rechecked against source; not full native replay.
5. **H5:** Research reports, README, manuscript and retrospective explanations; informative but cannot verify their own measurements.
6. **H6:** Earlier chat summaries, proposals and design intentions; hypothesis/provenance only, not experiment proof.
Keep different protocols (DQN/PPO short matched study, N-series, E126 native public evaluation, official Kaggle) separate.

## Claim register
| ID | Claim | Status | Source and examination | Limit |
|---|---|---|---|---|
| EL-001 | GitHub repository is `Stralb/arc-agi-3-rl-research`, public, default `main`. | VERIFIED | GitHub repository metadata via connected owner account | Different from guessed `stralb/arc3`. |
| EL-002 | Main audit base is `49b966d06afe8ee2a51da100801bf7d5ae63eebf` (latest fetched main commit). | VERIFIED | Connected GitHub commit history, fetched commit | Recheck for concurrent changes before integration. |
| EL-003 | Main is curated; archived N-series and negative results are on `archive/full-research-2026-10-27`. | VERIFIED | Both branch names; main and archived README; archive `experiments/INDEX.md` | Full owner-held runtime/trace ZIP is separate. |
| EL-004 | Report is 8 pages main + 2 references and assignment allows maximum 8 main pages. | VERIFIED | Locally inspected E128 PDF and `RL_Assignment(1).pdf` pages 4–5 | Template/style conformance beyond visual appearance not yet confirmed from matching LaTeX source. |
| EL-005 | Assignment requires DQN/course algorithm + PPO/non-course algorithm, each baseline + two substantive evaluated improvements. | VERIFIED | Assignment pp. 2–4 | E126 is *not* a substitute for a second learning algorithm. |
| EL-006 | Paper reports 72 six-arm DQN/PPO native runs, plus random and ablations; DQN levels 0/2/2, PPO 0/0/1. | UNVERIFIED | E128 PDF pp. 1, 3–5 | Neither raw 72 episode records, training scripts, intermediate gradients nor checkpoints located in inspected main/archive indexes. Search owner-held archives/history before concluding absent. |
| EL-007 | DQN/PPO methods, reward and intervention descriptions are present in E128. | VERIFIED | E128 PDF pp. 2–5 | Textual method description is not implementation/training proof. |
| EL-008 | Random reference 12 runs, PPO mask-only and no-updates ablations 12 each. | UNVERIFIED | E128 PDF pp. 4–5 | Need raw runs, code and logs. |
| EL-009 | N093 public 25-game levels: L1=13, L2=1, L3+=0. | VERIFIED | Reaggregated committed `results/n093_public25.csv` (25 rows) | Historical source table only; no new SDK replay. |
| EL-010 | N117 public 25-game levels: L1=13, L2=2, L3+=0. | VERIFIED | Reaggregated `results/n117_public25.csv` (25 rows) | Historical native reports; exposed games. |
| EL-011 | N117 gains an exposed `tu93` Level-2 completion over N093. | SUPPORTED BUT LIMITED | `results/n117_public25.csv`; `src/local_effect_policy.py`; archived `experiments/N117/README.md` | Original complete native trace archive/SDK not in public tree. |
| EL-012 | E126 matched local score/levels are 15→16 (seed 76), 14→16 (77), 15→16 (78). | VERIFIED | Reaggregated `results/e126_per_game.csv` (1125 rows) and checked `results/e126_all_arms.csv` (45 rows) | CSV arithmetic verified, not independently rerun against native SDK. |
| EL-013 | All E126 local score increases concentrate in `s5i5` and `lf52` across the three evaluated seeds. | VERIFIED | Direct per-game baseline-vs-`hybrid_trained` CSV subtraction; all other 23 game families tied | Not evidence of novel-family transfer. |
| EL-014 | E126 reports action selection divergence 28/75, six score-positive comparisons and four extra levels. | SUPPORTED BUT LIMITED | E128 pp. 6–7; archived `experiments/E126/README.md` and audit pointers; per-game CSV confirms four extra levels | No full trace-hash/first-divergence replay was performed for this audit. |
| EL-015 | E126 effect model is a frozen, externally trained effect predictor, used for sparse Level-1 click ranking; Level-2+ defers to N117. | VERIFIED (readable source), SUPPORTED BUT LIMITED (runtime) | `release/e126_template.py`: `eval()`, `requires_grad_(False)`, `_rank_ties` gating at >=0.80 modal color and no direction controls | Large generated files/checkpoint bytes not independently downloaded/tested; teammate permission unresolved. |
| EL-016 | E126 local native score mean rose from 2.081484 to 2.225399. | VERIFIED | Recalculated seed-level means from `results/e126_per_game.csv` | Descriptive public-game gain only. |
| EL-017 | E126 obtained official Kaggle score 0.33, submission ID 57690887. | CONTRADICTED / UNRESOLVED | E128 PDF p. 7 asserts submission; main `README.md`, `release/manifest.json` (`official_kaggle_submission: false`), archived `experiments/E126/README.md` assert **not submitted** | Could be a later official submission after repo snapshot. Must fetch Kaggle submission timestamp, source hash and score; don't claim fabrication without chronology. |
| EL-018 | N117 Kaggle public score 0.33 with submission ID 57675023. | UNVERIFIED | E128 PDF p. 7; repo archive mentions earlier 0.33 without server record | Official Kaggle receipt absent from inspected repo. |
| EL-019 | N118 history effect Brier 0.1691→0.1516 but effect FNR 5.29%→12.22%, 15 levels unchanged. | SUPPORTED BUT LIMITED | E128 PDF pp. 1,5; archived `reports/N118_FINDINGS.md` and output index list raw summary | Recompute against `experiments/N118/prequential/summary.json` and observation records; training/evaluation protocols differ. |
| EL-020 | All 25 public families were exposed during research. | VERIFIED (disclosure) | Current/archived README, `docs/REPRODUCIBILITY.md`, `docs/REPOSITORY_COVERAGE.md`, E128 | No independent holdout generalization claim allowed. |
| EL-021 | Main reproducibility scripts check source hashes, CSV arithmetic, notebook and figure syntax. | VERIFIED (source inspected) | `scripts/verify_repository.py`, `scripts/verify_e126_release.py`, `test_repository.py` | Scripts were read, not executed locally, and explicitly do not run SDK or Kaggle. |
| EL-022 | Full original native SDK/traces, E127/E128 parity 75 episodes/8632 actions, 1125 total episodes/125220 actions are available in owner-held archive. | SUPPORTED BUT LIMITED | Archived `experiments/E126/README.md`, `docs/REPOSITORY_COVERAGE.md` | Public tree not complete; owner's original archives not accessed here. |
| EL-023 | Current paper includes official score and page-compliant sections but lacks confirmed team contribution details. | VERIFIED (paper text) | E128 p. 8: “Team contributions remain to be confirmed.” | Assignment requires a contribution statement. |
| EL-024 | Paper LaTeX source and paper-associated figure-generation scripts are available in the inspected GitHub snapshot. | MISSING | Inspected main README, archived research and submission indexes; no final E128 LaTeX/report source advertised | Do not infer that separate supplied `main.tex` is the E128 source; its header is a generic RLJ template. |
| EL-025 | E126 model permission and source licensing are cleared. | UNVERIFIED | `docs/DATA_AND_LICENSES.md` explicitly requires confirmation | Existing public checkpoint is not proof of redistribution permission. |

## Current inventory anchors
- Main: `README.md`, `src/frozen_n093.py`, `src/best_public_agent.py`, `src/local_effect_policy.py`, `src/e126_submission_agent.py`, `release/{build_candidate.py,e126_template.py,effect_prior_s11.pt,manifest.json}`, `E126_Kaggle_Candidate.ipynb`, `results/*.csv`, `results/plots/*.svg`, `scripts/*.py`, `test_repository.py`, `requirements.txt`.
- Archive: `experiments/{early,N092,N093_frozen,N101..N120,E126}/`, `reports/`, `data/outputs/`, `data/provenance/`, `docs/`, `notebooks/`, original N114/N117 runner and replay code. This is an indexed subset, not a guaranteed exhaustive tree.
- **No evidence yet** that E128's short six-arm DQN/PPO training records are committed, despite a historical DQN-related N-series; don't substitute N117/E126 Bellman controllers for those algorithms.

## Source links
- Repository: https://github.com/Stralb/arc-agi-3-rl-research
- History: https://github.com/Stralb/arc-agi-3-rl-research/tree/archive/full-research-2026-10-27
- E126 release source: https://github.com/Stralb/arc-agi-3-rl-research/blob/main/release/e126_template.py
- Native reproduction boundary: https://github.com/Stralb/arc-agi-3-rl-research/blob/archive/full-research-2026-10-27/docs/REPRODUCIBILITY.md

Updated by initial connected-repository + attached-PDF inspection; preserve these source boundaries in subsequent revisions.

## Assessment-only supplement — 2026-10-27
Full lecturer requirement reconstruction and 44-row mapping: [REQUIREMENT_TO_EVIDENCE_MATRIX.md](REQUIREMENT_TO_EVIDENCE_MATRIX.md).
- EL-026 **VERIFIED assignment requirement:** The lecturer explicitly requires DQN/course-algorithm and PPO/non-course-algorithm baselines, each with baseline and two substantive evaluated improvements; random reference; official score, completions/failures, learning/adaptation curves, compute, and >=3 independent stochastic seeds or justified limitation (assignment pp2–4).
- EL-027 **VERIFIED report state:** E128 documents DQN/PPO 72-run study with 36 extra random/PPO ablations, but explicitly says its cumulative reward-event plot is **not** a proper training/checkpoint curve (E128 p5).
- EL-028 **VERIFIED repository research context:** archived N118, N119, N120 reports contain negative studies and native SDK descriptions; they cannot stand in for missing original DQN/PPO six-arm logs.
- EL-029 **UNVERIFIED Kaggle chronology:** E128 PDF creation 2026-10-27 at 12:00 UTC, whereas last inspected main commit was 09:32 UTC; repo 'not submitted' manifest could predate a later real server submission. Preserve source disagreement pending timestamp/source-hash receipt.
- EL-030 **UNVERIFIED exact RLC build:** E128 has 8-page body and 2-page bibliography; its matching source and template flags were not recovered in repository snapshot.

## Forensic-code supplement — 2026-10-27
Full 30-claim source/result analysis: [FORENSIC_CODE_AND_RESULTS_AUDIT.md](FORENSIC_CODE_AND_RESULTS_AUDIT.md).
- EL-031 VERIFIED source: fetched complete Git blobs N093 `e9e605c`, N117 `eb6f071`, E126 `84a4d30`; `N117.startsWith(N093)` and `E126.startsWith(N117)` passed static checks. No PPO/gradient-update code in the added E126 extension.
- EL-032 VERIFIED source: N093 empirical Bellman transition-count backup with `Q=1` optimistic starting values, `gamma=.985`, no gradient updates in acting core; its `num_updates` is Bellman backup count.
- EL-033 VERIFIED source: E126's trained auxiliary CNN is `eval()`, `requires_grad_(False)` and under `torch.inference_mode()`; activation restricted to Level-1 sparse click states, modal fraction >=0.80; Level-2+ defers to N117.
- EL-034 VERIFIED source: E126 `_Temporal126.forward` does not consume `hist_grid/hist_mask`; only current and previous frames. Do not infer longer history from unused parameters.
- EL-035 VERIFIED saved table arithmetic: E126 has 45*25=1,125 per-game rows and 125,220 summed recorded SDK actions; seed-specific 2872+2873+2887=8,632 E126 actions, 28 changed trajectories, 6 positive SDK pairs, 4 extra levels, 68.5376% of positive SDK gain from `s5i5`. No native SDK replay performed.
- EL-036 VERIFIED saved source summary: N118 `L2+` 1,197 cases, Brier 0.169102→0.151572, false-negative 0.052879→0.122209. Prediction outcome not native control gain.
- EL-037 UNVERIFIED original coursework: exact 72 DQN/PPO training runs and 36 random/PPO controls not retrieved from the connected GitHub tree; an earlier `e078_course_recovery` directory listing exists but is not the raw final study.
- EL-038 FLAG (not disproved): under a simple 16-warmup, every-eight-actions schedule DQN updates are 360 per arm; DQN-I1 reports 361. Native full 3,072-action counts per 12-run arm also require terminal/reset accounting.
- EL-039 UNVERIFIED/conditional: DQN-I2 epsilon escalation after 96 unrewarded steps is potentially a **borderline conditional schedule**, not necessarily a substantive algorithmic innovation. Source and paired changed-action records required; no definitive classification from prose.
- EL-040 UNVERIFIED implementation correctness: PPO-I2 masked new-policy log probabilities must use identical support to stored old-policy sampling. Original rollout tensors/code not available.
- EL-041 UNVERIFIED official Kaggle E126 0.33 / ID57690887; manifest remains `candidate_not_submitted` and paper created later. Avoid declaring false/verified without server receipt.

## Tribunal synthesis — 2026-10-27
Six explicitly **simulated** specialist assessments, each completed before synthesis: [SIX_PERSPECTIVE_TRIBUNAL_20261027.md](SIX_PERSPECTIVE_TRIBUNAL_20261027.md).
- EL-031 **VERIFIED paper omission:** E128 p5 acknowledges Figure 2 is an intra-run reward-event timing chart, not a true independently evaluated learning-curve checkpoint series; the lecturer explicitly requests curves (assignment p3).
- EL-032 **SUPPORTED BUT LIMITED:** Source inspection directly confirms N093 empirical observed-graph Bellman backups, no DQN gradient from N093 runtime, one-step PUCT action ranking, 4102-index action encoding; E126 peer CNN is evaluation-frozen (source `release/e126_template.py`). This does not verify the separate coursework DQN/PPO code.
- EL-033 **UNVERIFIED:** PPO-I2 rollout/update foreground masks and old/new log-prob reconstruction; neural DQN target/backprop/target-sync correctness; DQN-I2 substantive design; raw coursework source not found in current repository indexes.
- EL-034 **VERIFIED reported arithmetic, not SDK replay:** E126 45 arms x25 =1125 episodes, 125220 actions, 28 changed matched trajectories (from archived paired table), six positive game-seed comparisons (from per-game subtraction), four extra levels and 8632 trained-hybrid actions. All positive SDK differences are in s5i5 and lf52; s5i5 contributes 68.54%.
- EL-035 **CONTRADICTED pending chronology:** Paper (E128 p7) identifies E126 official Kaggle ID 57690887=0.33; archived `release/manifest.json` marks candidate unsubmitted. No external Kaggle response inspected. A later submission could reconcile sources; **no misconduct conclusion**.

## Academic prosecution case — 2026-10-27
[Formal 12-charge, ranked prosecution record](CASE_FOR_PROSECUTION_20261027.md) against **submission adequacy**, not authors. Claimed status is precise: established reporting/attribution limits do not mean a research-integrity violation; unavailable source code is not proven absent. 
- EL-036 **VERIFIED from lecturer pp2–5 and E128 p5:** original coursework report does not supply required budget-indexed learning/adaptation curves; first-reward event timing is not an independently evaluated checkpoint learning curve.
- EL-037 **PROBABLE concern, implementation unresolved:** DQN-I2 as described is a 96-no-native-reward trigger and epsilon floor .75; whether this is a substantive strategy or merely conditional hyperparameter schedule requires source inspection.
- EL-038 **VERIFIED scope of limitation:** DQN-I1 bundles legal candidate dueling ranking, D14 exploration and an externally pretrained effect representation; the paper explicitly avoids a unique component-level causal claim.
- EL-039 **VERIFIED documented inequality:** DQN-I1/I2 use external pretrained effects while PPO learns in short matched run; Table1 in-run wall-clock excludes pretraining. Unequal all-in compute is disclosed; not by itself a rule violation.
- EL-040 **ESTABLISHED omission:** E128 p8 leaves team contributions unconfirmed; Paper Track and Moodle receipts are not accessible in the inspected repository. Actual submission status remains UNVERIFIED.
- EL-041 **INFERENCE LIMIT, not misconduct:** 4 exposed coursework families / 3 policy seeds / 3 distinct positive game-seed cells and E126 2/25 families generating all score gains cannot establish population-level new-game advantage. E128 itself disclaims such generalization.

## Defence counsel update — 2026-10-27
[CASE_FOR_DEFENCE_20261027.md](CASE_FOR_DEFENCE_20261027.md) answers all CP-01 to CP-12 using lecturer pp2–5, actual E128 and versioned repo source. New direct checks: `docs/REPOSITORY_COVERAGE.md` (archive) explicitly states GitHub is a curated, incomplete snapshot of 1355-entry offline archive; absent course logs from the public tree do not prove non-execution. `scripts/verify_e126_release.py` validates hashes and 45×25 saved game rows and enforces `official_kaggle_submission is False` for its historical manifest; it does not test a later server upload. `results/e126_robustness.csv` has four positive local SDK deltas and two extra levels, but unchanged initial native frames. **No original DQN/PPO replay or external Kaggle receipt was obtained.**
- EL-042 **VERIFIED lecturer rule:** assignments p2 §3(3) explicitly allow negative improvements to receive credit when motivated, tested and analysed. Hence no-win PPO-I1 / DQN-I2 are not automatically invalid, subject to actual implementation and substantive-change requirements.
- EL-043 **VERIFIED contest distinction:** E126 public native SDK checks do not verify official Kaggle submission; exact build candidate hash and historical submitted-status mismatch remain unresolved.
- EL-044 **VERIFIED scope limitation:** assignment p3 §4(3) calls for heldout split wherever public games permit and truthful exposure disclosure; E128 explicitly admits exposed games. Missing independent transfer remains scientific limitation, not automatically a prohibited test design.

## Cross-examination rulings — 2026-10-27
Full five-step ten-issue hearing: [SCIENTIFIC_CROSS_EXAMINATION_20261027.md](SCIENTIFIC_CROSS_EXAMINATION_20261027.md). Narrow decisions: CX-01 UNRESOLVED; CX-02 RESOLVED (no individual DQN I1 component attribution); CX-03 PARTIALLY RESOLVED; CX-04 RESOLVED (incomplete real curves); CX-05 RESOLVED (seeds do not establish unseen generalisation); CX-06 PARTIALLY RESOLVED; CX-07 RESOLVED (prediction alone insufficient for demonstrated native control); CX-08 RESOLVED (E126 actual code lineage); CX-09 PARTIALLY RESOLVED; CX-10 PARTIALLY RESOLVED.
- EL-045 **VERIFIED code detail:** archived E126 _rank_ties delegates Level 2+ to N117, uses Level-1 trained CNN gate when ACTION6 legal and directional ACTION1–5 absent and modal colour >=.80; ACTION7 is not explicitly gated out. CNN strict load/eval/disable gradients.
- EL-046 **VERIFIED saved numeric arithmetic** (fresh GitHub data reaggregation): 1125 episodes, 125220 actions; E126 three-seed mean 2.2253992392 vs baseline 2.0814840002; six positive game-seed score differences across s5i5 and lf52 and four extra levels. Not a native SDK rerun.
- EL-047 **VERIFIED assignment gap:** E128 first-reward event plots do not discharge lecturer §5 learning OR adaptation curve requirement; the paper admits incompleteness.
- EL-048 **UNVERIFIED:** original DQN-I2 code, PPO-I2 log-prob masking, official E126 Kaggle ID57690887. No confirmed error of those implementations established.


## Judicial assessment — 2026-10-27 (E128; non-leaderboard)
The full judicial disposition, 12 charges and category scores are in [JUDICIAL_ASSESSMENT_20261027.md](JUDICIAL_ASSESSMENT_20261027.md). **55/90 provisional**, plausible evidence-weighted grading range **42–73/90** (not statistical confidence interval); class leaderboard **not assessed**. Based on exact lecturer wording in `RL_Assignment(1).pdf` pp2–5 and independently extracted E128 pp1–8. Assessment is not evidence of native replay or official submission.

- **EL-049 — VERIFIED assessment requirement:** §5 p3 specifically requires **learning or adaptation curves against interaction budget**. E128 p5 expressly acknowledges Figure2 is first native-reward event timing and the required learning/adaptation evidence is incomplete. Judicial CP-04 **SUSTAINED**.
- **EL-050 — VERIFIED manuscript shortcoming:** E128 p8 states “Team contributions remain to be confirmed,” despite assignment §6 p5. CP-03 **PARTIALLY SUSTAINED** because external Moodle/Paper Track receipts may exist outside this snapshot.
- **EL-051 — UNVERIFIED substantive course learning:** E128 reports 72 six-arm and 36 control episodes, 360/361 Double DQN and 768 PPO optimizer updates; original full source/gradient/episode records not independently available in inspected GitHub. CP-01 **INSUFFICIENT EVIDENCE**, CP-06 **PARTIALLY SUSTAINED** as evidence-availability/reproducibility deficiency only, CP-07 **INSUFFICIENT EVIDENCE**.
- **EL-052 — UNVERIFIED DQN-I2 eligibility:** E128 96-step reward-stall trigger with epsilon floor .75 may be a conditional hyperparameter schedule; actual source/choice logs absent. No assertion of disqualification or correct substantive implementation. CP-05 **INSUFFICIENT EVIDENCE**.
- **EL-053 — VERIFIED methodological limitations (not automatic violations):** DQN-I1 bundles concurrent changes (CP-08 **PARTIALLY SUSTAINED**); pretrained DQN effect features mean total resources unequal despite matched native-action ceilings (CP-09 **PARTIALLY SUSTAINED**); PPO mask-only control supplies case-specific nonnecessity of novelty, not general mask effect (CP-10 **PARTIALLY SUSTAINED**).
- **EL-054 — VERIFIED correctly limited generalisation:** Historical exposure and nonindependent game samples are disclosed; E128 explicitly rejects unseen-game transfer. CP-11 **DISMISSED as an allegation of unsupported generalisation or leakage noncompliance**, while retaining actual scientific limitations.
- **EL-055 — SUPPORTED BUT LIMITED editorial deficiency:** E126 has authentic separate code/result evidence and deserves discussion but space trade-off may undercommunicate coursework essentials. CP-12 **PARTIALLY SUSTAINED** without treating additional research as a violation.
- **EL-056 — UNVERIFIED external source record:** E128 E126 official Kaggle submission 57690887/0.33 postdates manifest marked not submitted. Possible chronology; official receipt/hash/class nomination missing. CP-02 **INSUFFICIENT EVIDENCE**; **no misconduct finding**. Class leaderboard cannot be assigned.
- **EL-057 — VERIFIED source/CSV boundaries:** N093/N117/E126 source architecture and E126 1,125-row/125,220-action saved arithmetic are inspectable. They cannot verify DQN/PPO coursework execution, official Kaggle score or generalisation. No confirmed actual implementation defect in the uninspected DQN/PPO algorithms.
