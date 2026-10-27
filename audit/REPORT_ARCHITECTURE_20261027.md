# E128 -> next report: eight-page scientific architecture (NO manuscript rewrite)
Date: 27 Oct 2026 SAST. Authoritative rubric: user-provided `RL_Assignment(1).pdf`, five pages; existing paper: `ARC_AGI3_E128_Revised_Research_Paper (1).pdf` 8 main pages + 2 pages references. Supporting audit: `audit/REQUIREMENT_TO_EVIDENCE_MATRIX.md`, `audit/JUDICIAL_ASSESSMENT_20261027.md`, `audit/EXECUTED_EXPERIMENTAL_ANALYSIS_20261027.md`, `audit/EVIDENCE_LEDGER.md`. Research baseline `main@49b966d06afe8ee2a51da100801bf7d5ae63eebf`. **This is a prewriting architecture decision, not an edited LaTeX or paper.**

## Hard constraints and evidence gate
- Use official RLC/RLJ **2026 LaTeX template**, cover disabled as the lecturer specifically requires. No changed margins/font sizes/spacing; maximum eight pages main (all essential figures and tables), references after main excluded. Exact E128 compilation source and `rlj.sty` *not yet verified*. Uploaded `main.tex` is a general RLJ template sample, **not proof** of E128 source provenance.
- Main narrative must directly prove (as far as data permit) **two genuinely trained RL agents**, a baseline and two independently evaluated stage changes **each**, random reference, correct native score, 3 stochastic seeds, budgets, failures, ablations and adaptation/learning curve requirement. Changes need not win, but simple tuning does not qualify.
- **Crucial evidence tier:** six-arm core numerical outcomes in E128 are `REPORTED_ONLY` in the generated 108-row reconstruction; original 72+36 SDK trajectories, optimizer source/checkpoints and team contributions were not verified. Do not write `independently reproduced` or claim the curator's E126 CSV verifies them.
- E126's native public-game **saved-data arithmetic** is verified: 75 matched comparisons, levels 44→48, mean SDK 2.081484→2.225399, six positive score cells in lf52 and s5i5, 28 changed trajectories as reported in archival paired record, 1,125 across 45 arms and 125,220 charged actions. No SDK replay or unseen generalization. Official Kaggle E126 0.33 ID57690887 is **reported but not platform verified**, so present only as clearly identified/unverified unless original receipt is obtained.
- E128 currently admits that its Figure 2 first-win event timing **does not satisfy** genuine learning/adaptation curves. Any proposed replacement must pass a real measured policy-improvement/adaptation gate; no synthetic curve.
- Keep all relevant run failures, actual exposure limitations, DQN-I1 bundle attribution and DQN-I2 substantive uncertainty; avoid portraying the separate E126 empirical Bellman/frozen CNN policy as acting DQN+PPO ensemble.

## A/B/C structure evaluation
Criteria are qualitative editorial assessments, **not numerical rubric marks**:
| Dimension | A. Coursework-first | B. Scientific-question-first | C. Hybrid |
|---|---|---|---|
| Rubric coverage | Very high; checklist-forward | Medium; course stages risk dispersal | Very high; explicit stages and comparisons |
| Original scientific insight | Medium; E126 can become aside | Very high; one effect-vs-goal narrative | High; effect-vs-goal is motive and synthesis |
| Argument coherence | Good but may feel staged | Excellent if evidence uniformly strong | Excellent if separate E126 is labelled |
| Evidence placement | Course table first; later science compressed | N118/E126 interspersed, protocols confusing | Course table/controls first, E126 clearly separated |
| Algorithmic technical clarity | High | Medium | High |
| Eight-page efficiency | High | Medium–low | High |
| Lecturer/reviewer accessibility | Excellent for lecturer; good for research reviewers | Strong for theory reviewer; weaker for marking | Excellent for both |
| Risk E126 mistaken for DQN/PPO | Low | High | Lowest if explicit lineage + section label |
| Weakness | May understate original empirical insight | May fail mandatory two algorithm investigation emphasis | Requires disciplined page and claim boundaries |
**Selected C (hybrid), with coursework-first ordering.** This is an architectural recommendation; does not imply any evidence gap is solved.

## Final title recommendation
**When Visual Change Is Not Progress: Evaluating DQN and PPO in ARC-AGI-3**

Why: retains distinctive scientifically justified theme while placing the two mandated neural learners at the center. Avoid title suggesting E126 is a deployed DQN/PPO hybrid. Short alternative if title space matters: **DQN and PPO in ARC-AGI-3: When Visual Change Is Not Progress**.

### One-sentence thesis
**In the exposed ARC-AGI-3 development games, exploration or action-effect prediction can change actions and observable transitions without reliably increasing native level completion; controlled DQN/PPO stage comparisons and a separately implemented effect-guided controller make those distinctions empirically visible.**

No claim of unexposed-game generalization; `controlled` applies to reported matched evaluation configuration subject to raw-log verification.

### RQs
- **RQ1 (course baseline):** Under a common four-game, three-policy-seed, 256-charged-action native protocol, what do the reported baseline DQN and PPO agents achieve relative to a random reference, accounting for failures, action costs and training?
- **RQ2 (course iterative):** How do two separately evaluated interventions per algorithm affect native progress and action choice, and which effects remain unidentifiable because of bundled changes or limited controls?
- **RQ3 (clearly separate extension):** In the later N118 and N093→E126 research, when do better effect predictions or click-ranking changes correspond to observed native progress, and how narrowly are those gains concentrated across exposed families?
No RQ asserts an official Kaggle gain or hidden-game transfer. Kaggle record is release evidence, not a generalization experiment.

### Genuinely supported contributions, with proof status
1. **Reported six-stage DQN/PPO learning study [SUPPORTED BUT LIMITED, implementation UNVERIFIED].** E128 §3–4 reports 72 game–seed arm runs, DQN 0/2/2 and PPO 0/0/1 completions, random and PPO controls. Reader must be told raw gradient/checkpoint/SDK records are not independently accessible in audited public repo.
2. **Narrow, informative negative coursework comparisons [REPORTED ONLY].** PPO novelty yields no native win; mask-only reproduces the one PPO-I2 `s5i5` win as reported; DQN-I2 stall rule activated but did not add a completion. No claim that the core mathematical implementations have been verified from code.
3. **Source-supported E126 architecture [VERIFIED source].** Separate empirical Bellman N093/N117, online native-Q/local effect/click-contingency evidence; frozen E125 pretrained CNN gated for sparse Level-1 click ranking; Level-2+ delegated to N117.
4. **Independent E126 saved-data reaggregation [VERIFIED arithmetic, not SDK replay].** 75 matched game–seed records: 44→48 levels, mean +0.143915 local SDK, six positive score pairs exclusively in two previously exposed families; source-linked random/salience/contingency controls and descriptive zero-inclusive bootstrap.
5. **N118 predictive/decision mismatch [SUPPORTED BUT LIMITED].** Archived findings report Brier 0.169102→0.151572, false-negative 5.29%→12.22%, same 15 levels; original prediction traces not independently replayed in this report architecture. Do not infer a theorem about all model-based RL.

## Section order and exact page-area budget (8.00 main pages, planning fractions only)
| Section | Page equivalent | Essential content |
|---|---:|---|
| Title, author metadata, abstract | 0.60 | Algorithms first; one honest E126 extension result and qualifications; no unverified official score asserted as fact |
| 1. Introduction, problem, RQs, contribution statement | 0.65 | Observable effect vs native progress, explicit RQ1–RQ3 and what was learned, what wasn't |
| 2. Environment/problem formulation and compact related work | 0.55 | POMDP, 64×64 16-colour observation, 4102 flat actions, legal mask, native progression and SDK score distinction; only high-value citations |
| 3. DQN/PPO baseline implementations | 0.90 | State/history, flat vs factorized click, Double-DQN Bellman eq, PPO clipped objective, GAE, update lifecycle; source provenance status |
| 4. Two iterative improvements per algorithm | 1.05 | Sequence and stage-specific limitation→hypothesis→change→observed outcome, DQN bundle honesty, I2 epsilon uncertainty, PPO novelty reward and mask |
| 5. Experimental protocol | 0.65 | Four exposed families×3 seeds×256 native calls, resets, training versus eval, random control, scorer/version provenance, compute/pretrain fairness |
| 6. Coursework matched results, ablations and final comparison | 1.80 | Core nine-arm Table 1; 108-cell outcome visual with failures; DQN-I2/PPO-I2 paired contrasts; PPO ablations and two success/failure examples; genuine learning curve only if source-valid |
| 7. **Separate research extension:** effect prediction, N093→E126 | 0.95 | One compact source-lineage sentence, N118 negative signal in text, E126 frozen click gate and saved-data effect decomposition + controls, no Kaggle claim without receipt |
| 8. Discussion, limits, reproducibility, contributions, conclusion | 0.85 | Three bottlenecks, exposure and sample dependence, no hidden transfer, empty checkpoint-curve gap, permissions, true member roles, specific conclusion |
| **Total before references** | **8.00** | References separate, not a license to hide mandatory experiments after bibliography |

**Page-by-page physical layout target:** p1 title/abstract + RQs; p2 POMDP, DQN/PPO method; p3 improvement stages; p4 evaluation protocol + result table; p5 compact 9×12 outcome matrix and PPO ablations; p6 final comparison, failures, cost/adaptation diagnostics (if valid), source disclosure; p7 distinct N118→E126 summary + compact paired effect figure; p8 limitations, actual reproducibility and conclusion. Treat this as a layout target, not a claim of LaTeX fit before compiling original official template.

## Exhibit allocation and conditional logic
- **Main Table 1 — mandatory core nine arms** (`random,DQN-V0/I1/I2,PPO-V0/I1/I2,mask-only,no-updates`): grouped label, n, native levels, mean local SDK (NA for controls if unknown), optimizer updates (label reported), charged actions, in-run walltime (missing for controls); explicit note training prior excluded. Source: E128 Table1 and `tables/coursework_arm_summary_REPORTED_ONLY.csv`. **Status: reported only**, do not claim independently replayed.
- **Main Table 2 — compact six-stage intervention chain**: two algorithms×three stages, short **observed limitation → hypothesis/intervention → evaluation result**; avoid reprinting score columns identical to Table1. Candidate text derived from E128 §3.2. If space tight, format as subheaded parallel paragraphs instead.
- **Main Figure 1 — full failed/successful 9×12 game/seed outcome matrix** with first native reward times only where recorded, clear `no completion recorded` not invented `GAME_OVER`, legend `reported-only from E128`, no redundant lower CDF panels. Source: generated `fig1_coursework_reported_outcomes.svg` and 108-row paper-derived table. Fit wide 2-column figure, preserve legibility.
- **Conditional figure slot: actual learning/adaptation curve** only when an authentic budget-indexed measure of improvement is reconstructed with original checkpoint/rollout measurements, source and correct denominator. **If not available, do not fill with first-win CDF**; keep honest one-sentence incompleteness disclosure and devote freed area to verified matched comparison, no fake claim of full rubric closure. Current `fig2_reported_event_timing_NOT_learning.svg` and `fig4_e126_first_reward_attainment_NOT_learning.svg` are allowed only as explicitly descriptive supplemental figures.
- **Main Figure 2 — E126 paired mechanism-to-outcome decomposition**: single compact combination of `28/75 changed trajectories → 6/75 positive local SDK pairs → 4 extra levels` and **two contributing families**; source `e126_matched_75_recomputed.csv`, archived `e126_paired_changes.csv`; annotate that action divergence is reported archived trace evidence not independently replayed. Prefer condensed version of original E128 Fig4, not duplicated E126 separate 5-arm chart.
- **Optional Table 3/inline E126 controls:** `44/45/45/45/48` total native levels across 75 episodes for baseline, contingency, random, salience, trained hybrid, with small `n=75` caption; if page tight present inline or a subpanel in Figure2. Source verified `e126_all_45_arms_verified_saved_data.csv`.
- **N118 prequential result:** one compact 2-row/3-column mini-table or single sentence: Brier none/real, FNR none/real, 15 levels both; DO NOT spend a full figure if E126 already has one.
- **Never add:** separate large generic lineage diagram (old Fig1 bottom), native Q return eq4, dense four-Kaggle-entry comparison unless server receipts, standalone N119/N120 figures, another predictor performance plot without a new inferential point.

## Equations
1. **Necessary:** Double-DQN legal-action target including done mask and online argmax / target evaluation. Preserve original Eq(1) corrected only if original code actually computes it.
2. **Necessary:** PPO clipped objective and one-line type+conditional-coordinate joint log-prob, with mask support consistency; original Eq(2). Use math text for GAE instead of additional displayed equation if verified.
3. **Conditionally necessary (prefer inline):** PPO-I1 shaped training reward, explicitly `r_train = r_native + intrinsic_count_bonus` and coefficient 0.02 / count denominator, enough to separate actual native scoring. Original Eq(3) may be displayed if space available.
4. **Not necessary:** Return-objective Eq(4) in late discussion, because it adds no new measured comparison, and its general point can be conveyed in prose.
5. **POMDP:** notation inline, not a large standalone equation; avoid duplicative textbook RL formulas and irrelevant method survey.

## Content removal and relocation plan
| Current E128 content | Action | Why | Scientific protection |
|---|---|---|---|
| §2 long survey of Rainbow, RND, Go-Explore, options, HER, imagination and Dyna | Compress to references attached to actual DQN/PPO interventions and core effect-vs-reward gap | ~0.3–0.4 page freed; cuts generic background | Keep key DQN, PPO, sparse reward, effect-model objective citations |
| Current Fig1 large double-lineage diagram | Replace by one slim source-lineage sentence/mini-strip in extension | Space and confusion with PPO acting params | Explicit “E126 has no acting PPO/DQN neural weights” |
| Current Fig2 lower cumulative first-win plots | Remove from main or put in appropriately labelled supplement; retain 9×12 outcome matrix | Redundant and not valid learning curve | Preserve each win/failed cell and known first-reward time |
| §5 E015, N119, N120 detailed chronology | Reduce to at most one evidence-backed sentence about nonreward learning/support limits; put full archive references after main | Does not directly satisfy mandatory DQN/PPO rubric | Do not discard genuine nulls; keep code/source links |
| Current Fig3 full-page N118 predictor chart | Replace with mini-table/one sentence | One lesson already conveyed by numbers | Preserve Brier decrease, FNR increase, unchanged native levels, protocol distinction |
| Current Table2 full provenance lifecycle | Compress to compact inline paragraph/mini-table | Too tall for 8 pages | Keep frozen CNN, online Q, Level-1 gate, higher-level fallback, reset and pretrained attribution |
| Current Fig4 E126 complex panels | Keep *one* simplified source-linked 2-part figure | Preserves strongest original mechanistic evidence with less density | 28 changes ≠ 6 score gains ≠ 4 levels; two families, controls and exposure |
| §6 generic value-return display Eq4 and speculative potential future algorithms | Remove display and generic outlook | No additional rubric contribution | Preserve precise interpretation and one compact future limitation |
| List of four official Kaggle submission IDs and public scores | Keep E126 status only if verified receipt, labelled separately; complete list in submission manifest | Official E126 score unverified, cross-run protocols unmatched | No claim of improved Kaggle score if both are reported 0.33 |
| Repeated exposure and caveat paragraphs | Consolidate into one explicit limitations block | Reduces redundancy | Include all essential limitations once |
| Footnotes of exact package versions, hashes, all per-action logs | Move full copy to supplementary source/evidence bundle **without removing essential methods from main** | Source detail is important but need not all be prose | Main must state datasets, seeds, budgets, scorer, model ownership, resets and source link |
| Team contributions placeholder | Replace only with authentic authorship facts when provided | Direct mandatory grading requirement | Never fabricate work allocation |

**Supplementary after references:** full 108-row explicitly paper-derived matrix (do not call verified native raw data), all E126 75 matched and 45 arm tables, source and checkpoint SHA/rebuild logs, long failure examples, detailed N-series negatives, software versions and all 5 plot sources. The main eight pages still must contain *essential conclusions and required comparisons*, not just links.

## Evidence-to-section and rubric coverage
| Evidence ID | Tier | Main placement | Lecturer criterion | Verify before prose finalisation |
|---|---|---|---|---|
| Course DQN/PPO code and 72 core runs | REPORTED ONLY; original implementation UNVERIFIED | §§3–6; Table1; Fig1 | Baselines 20, improvements 25 | Original actual six source files, gradient changes, raw SDK rows, check 361 DQN I1 updates |
| Random and PPO two control groups (36 runs) | REPORTED ONLY | §6 Table1/Fig1; ablations | Baselines 20, rigour 25 | Original random/PPO controls and exact mask-only first-reward timestamp if exists |
| DQN-I1 candidate/dueling/D14/frozen encoder | Reported bundle | §4 | Improvements 25, fairness 25 | Actual code; cannot assign one component credit without ablation |
| DQN-I2 96-step stall and epsilon floor .75 | Reported only; substantive classification unresolved | §4 and §6 | Improvements 25 | Compare exact I1/I2 action code and matched choices; do not assert qualified if only tuning |
| PPO-I1 0.02 count-novelty, PPO-I2 >=65% foreground click mask | Reported only; probability correctness unverified | §§3–4, §6 controls | Baselines and improvements | Check PPO old/new logπ, GAE and rollout support |
| First-win timing, all unsuccessful cells | Reported from E128; terminal cause unknown | Fig1 and §6 | Rigour 25 | Native episode logs, no invented censor type; no false learning-curve label |
| True learning/adaptation performance budget series | **MISSING** | §6 slot if located; otherwise limitation §8 | Rigour 25 | Exact checkpoint/rollout metric and provenance. Never synthesize |
| External pretrained DQN encoder and all-in compute | Disclosed inequality, amount unknown | §5 and §8 | Rigour 25 and report 10 | Data/compute/permissions, different from E125 peer CNN |
| N118 Brier/FNR and unchanged levels | Archived report, not independently replayed in last analysis | §7 compact | Rigour/scientific narrative | Original N118 prediction traces and acting protocol if high confidence needed |
| N093→N117→E124/E125→E126 source | Source VERIFIED | §7 | Research extension/reproducibility | Preserve lineage and reset precision |
| E126 75 matched local scores and four extra levels | Saved CSV arithmetic VERIFIED, native replay not done | §7 Fig2, control row | Rigour 25, scientific extension | Source CSV hash, control selection, avoid withheld Kaggle inference |
| Official Kaggle E126 submission ID 57690887 score .33 | Platform UNVERIFIED; earlier manifest says not submitted | Abstract or §7 only after receipt; else say reported / unavailable | Leaderboard 10 (not quantified) and report 10 | Server score ID timestamp team/code SHA; never infer leaderboard from local SDK |
| RLC 2026 template, eight-page PDF, contributions | Eight-page count VERIFIED, build source and roles UNVERIFIED/MISSING | All sections and §8 | Report 10 | Rebuild from authentic RLC .tex, disable cover and ensure true roles |

## Go/no-go editorial decisions before prose
1. **No change** to actual scientific results or original source.
2. **Pause any statement of independent core neural training verification** until original code/logs found.
3. **Do not promote DQN-I2 as undoubtedly substantive** unless code/adaptation mechanism evidence establishes it. If only conditional epsilon tuning, label accurately and accept unresolved coursework requirement; do not invent new intervention.
4. **Do not draw or label a neural learning curve** from E126 first-win times.
5. **Official Kaggle 0.33 remains unverified**; no new claim of server performance without receipt.
6. **Keep E126 separate in title/abstract/§7**, not mixed into stage-to-stage DQN/PPO table.
7. **Verify exact RLC style source** before touching text or layout; avoid modifying template font/spacing to force eight pages.
8. **Approve architecture only, then write the revised manuscript and compile/inspect** in a later explicit step.

## Architecture-to-rubric gate (before drafting)
- **Problem /10:** §§1–3 address POMDP/history/feedback and both DQN/PPO objectives, citations. PASS structurally.
- **Baselines /20:** §§3,5–6 include both V0 evaluations, 12-run random baseline, numeric Table1 and source notes. PASS structurally; actual source proof UNVERIFIED.
- **Iterative /25:** §4 gives 2 successive changes per algorithm and results in §6; DQN-I2 eligibility not solved. CONDITIONAL structural pass.
- **Rigour /25:** §5–7 matched games/seeds/budgets/actions/native score, ablations, cases, tiny sample, E126 controls and limits. Genuine curves MISSING, not repairable by architecture alone. PARTIAL.
- **Report/repro /10:** Eight-page main, precise methods, meaningful figures, references; actual RLC source/author roles/receipt source missing. CONDITIONAL.
- **Leaderboard /10:** Not inferred from paper/local data; requires genuine eligible class Kaggle rank. UNKNOWN.
**Outcome:** Hybrid architecture is the best structure for truthful grading/verification but does not itself raise the previous provisional 55/90 assessment or resolve evidence blockers.
