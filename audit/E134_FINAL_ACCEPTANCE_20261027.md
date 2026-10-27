# E134 Final Lecturer-Requirement Acceptance Test — 27 October 2026

**Binding source:** user-uploaded `RL_Assignment (7).pdf`, actual five-page COMS4061A/COMS7071A specification, dated 15 September 2026, deadline 27 October 23:59 SAST. **Review product:** `ARC_AGI3_E134_Final_Checked_Paper.pdf`, `ARC_AGI3_E134_Final_Checked_LaTeX.tex`, `ARC_AGI3_E134_Final_Checked_Project.zip`, and 22-row `ARC_AGI3_E134_Final_Rubric_Matrix.md/.csv` generated and supplied in this conversation.

**Numerical acceptance outcomes:** 6 requirements **PASS** (2, 4, 5, 7, 17, 20), 14 **PARTIAL** (1, 3, 6, 9–16, 18–19, 21), 2 **FAIL** (8, 22). No **UNVERIFIED** as an entire category: decisive missing source is explicitly described in each pertinent PARTIAL/FAIL row. These are coverage statuses, **not an additive numerical grade**.

## Requirement-by-requirement status

| # | Lecturer requirement | Status | Grounded location or blocker |
|---:|---|---|---|
|1|Two distinct functioning learning baselines|PARTIAL|§2 pp2, §4 p3; original trained six-arm code not supplied|
|2|Learning method/update/decision explanation|PASS|§2.2–2.3 p2; Double-DQN and PPO objectives|
|3|Protocol reproducible and before improvements|PARTIAL|§3 p3; scorer/software version and native traces absent|
|4|Random-action sanity check|PASS|§4 p3, Fig A p4, Table1|
|5|Three evaluated versions per algorithm|PASS|Table1 p3, §§5–6 pp4–6, E128 reported outcomes|
|6|At least two substantive improvements each|PARTIAL|DQN-I2 epsilon schedule not proven substantive|
|7|Observed limitation/hypothesis/research rationale|PASS|§§5–6 pp4–6; cited intervention rationale|
|8|Changes beyond hyperparameter adjustment|FAIL|DQN-I2 documented solely as conditional epsilon floor after 96 unrewarded actions|
|9|Official native SDK score, evaluation set/version|PARTIAL|Table1 p3; scorer/version source absent|
|10|Completions/actions/failures|PARTIAL|Table1 p3, Table3 p7; raw action/terminal records not verified|
|11|Learning or adaptation curves vs budget|PARTIAL|Figs A p4, B p5, C p6 are valid within-run native-attainment reconstructions, **not** independently evaluated checkpoint-learning curves|
|12|At least three independent seeds/variability|PARTIAL|Seeds 301–303 reported, native seed47 fixed; individual failures/uncertainty incomplete|
|13|Runtime/hardware/full training cost|PARTIAL|§3 p3, Tables1–2; missing GPU/offline cost/version|
|14|Meaningful component ablations|PARTIAL|PPO mask-only/no-update panel and separate 600-action E012 DQN ablation; no same-protocol I1 component isolation|
|15|Representative trajectories/replays|PARTIAL|Table3 p7 authentic reward-event summaries, no real frames or action-by-action traces|
|16|Final comparison incl held-out adaptation|PARTIAL|Table2 p6, §7 pp6–7; no true held-out trials|
|17|Null results and uncertainty|PASS|Named §8 p7|
|18|Student vs reused code/model provenance|PARTIAL|§10 p8; peer checkpoint rights/individual roles not fully established|
|19|Adaptation/reset across action/level/game/run|PARTIAL|§3 p3 improved; level-boundary temporary state reset not verified|
|20|Citations/legible figures|PASS|All cited keys present; rendered Figs A/B/C/E126, Tables1–3|
|21|Eight main pages/required template|PARTIAL|Body pp1–8; references begin late p8, continue p9; working 2026.1 `rlj.sty` included, official exact style identity not certified|
|22|Full matching training source+competition/roles/tracks|FAIL|Original course DQN/PPO runner and authenticated Kaggle nomination/receipt, Paper Track, member roles and Moodle receipt absent from supplied deliverable|

## Actual E134 modifications and tested build

- Clarified weights/replay/rollout state across actions and runs without fabricating level-boundary reset semantics.
- Explicitly documented unavailable exact SDK scorer/package version and prior frozen encoder training budget.
- Presented DQN-I2 honestly as a tested *conditional epsilon schedule* that alone **does not establish a second substantive DQN mechanism**.
- Added exact public repository link and distinguished curator's source subset from missing original course runner, nomination, individual roles and receipts.
- Preserved E133 original results, three vector native-attainment figures and the separated E126 development conclusion; no new result or checkpoint invented.
- Actual `latexmk` compile: **9 physical pages**, main body completes p8; references start near bottom p8 and continue p9. No independent paper-cover page. All nine pages rendered and visually inspected.
- Script tests executed: existing **45/45 native curve** checks, **61/61 E133 source/citation/dataset** checks and new **30/30 E134 lecturer acceptance consistency** checks. Rebuilt from a fresh extraction of the ZIP: all checks pass, generated curves regenerated and PDF extracted text matches delivered version. ZIP integrity checked.
- **Saved-data verification remains separate:** E126 75-pair saved arithmetic confirms 44→48 levels and mean SDK 2.081484→2.225399; original DQN/PPO SDK and optimizer was **not** rerun.

**E134 artifact SHA-256:** final PDF `1169548fe821326bc3e12b32b0593e77a676307e1c6736008fc0dc7583af859f`, delivery ZIP `8af69655e40cf8f5efef8d8f8c72b6bf98c41efd25a62f74f976eef68e7212b6`.

**Submission readiness:** PDF source and figures verified at the reporting/reconstruction tier; **NOT** a confirmed complete official Kaggle/Paper Track/Moodle delivery. A high polish report cannot replace mandatory substantive I2 proof, genuine source/replay evidence, official scorer version or authenticated platform/author records. Official eligible class leaderboard marks remain **unknown**.
