# EXECUTED EXPERIMENTAL REANALYSIS — 27 October 2026

**Scope:** Offline, non-destructive saved-evidence verification and figure generation, not a fresh ARC SDK replay. **User-facing downloadable package:** `arc3_experimental_audit_20261027.zip` delivered in this conversation. Original repo code and checkpoint files were **not modified**.

**Reproduction package SHA-256:** `0610fcb1a5243d6ed67b388dca49b8b74234f9c0cfb83e11d3c43c72d8c31c7e`.  
**Figure/source script SHA-256:** `bac36d35697d5fca20eed747192319337fde082c01f4415b46dc2b396ee416f9`.  
Source commit: `main@49b966d06afe8ee2a51da100801bf7d5ae63eebf`.  
Actual original source blob: `results/e126_per_game.csv` Git blob `427b129ba3300200be40fd4df70b2c6f28fb9b81`; `results/e126_all_arms.csv` Git blob `6439a2261ca6a94d9df85ed8c1b31bc21c6b8357`. The 75-pair and 45-arm CSVs were copied/extracted directly from those connected repository file contents.

## Exactly executed

1. Connected GitHub fetch and inspection of original E126 1125 per-game rows, 45 E124–E126 arm aggregate rows, and archived N-series action/failure tables. GitHub snapshot contains no verified six-arm E128 DQN/PPO original code/checkpoints/108 episode logs.
2. Offline Python 3, pandas, NumPy and Matplotlib `reproduce_analysis.py`, with original 75 paired E126 and 45 arm rows as included fixtures. Reaggregated CSV tables and five publication-oriented candidate figures in vector PDF, SVG and PNG.
3. **14 passed** offline pytest tests, including unique arm/game/seed cells, E126 source arithmetic, retained zero outcomes, unreported mask-only first reward as missing, family bootstrap, and original repository-schema parser fixture. No known test failures; see original `logs/pytest_stdout.txt` in ZIP.
4. Generated two **distinct evidence tiers**: coursework `tables/coursework_108_reported_only.csv` reconstructed from E128 manuscript statements, and matched E126 `tables/e126_matched_75_recomputed.csv` independently recalculated from GitHub source.
5. Inspected rendered PNGs and corrected caption overlap; figure captions, interpretation, evidence tier and limitations included in `FIGURE_CAPTIONS.md`.
6. Repacked ZIP and verified `unzip -t` success; source-file SHA manifest included.

## Verified E126 stored-data arithmetic

- Historical E124–E126 rows **45 arms ×25 public games = 1125** episodes, **125220** charged SDK actions, exact saved arm summary totals.
- E126 vs N117 baseline: **75 matched family-seed pairs**. Baseline completed levels **44**, trained hybrid **48** (gain **4**). Baseline mean local SDK score **2.08148400018**, hybrid **2.22539923920**, mean paired delta **+0.14391523902** (local SDK 0–100 scale). Baseline actions **8293**, hybrid **8632**.
- **Six** positive game-seed score changes, all in `lf52` and `s5i5` (68.5376% of aggregate positive score difference is `s5i5`). No score regressions in the 75 matched E126 comparisons. This is descriptive on historically exposed public games.
- Native first-completion timestamp present in **38/75** baseline and **42/75** hybrid episodes; this produces a valid descriptive *within-run attainment-by-budget* chart, **NOT** checkpoint RL learning/adaptation.
- E126 control arms over 75 runs each: baseline **44** levels, contingency-only **45**, hybrid-random **45**, hybrid-salience **45**, hybrid-trained **48**. These are E126 controls and cannot be attributed to DQN/PPO coursework.
- Seeded family-block bootstrap (**20,000** draws; sample 25 families and retain each family’s 3 policy-seed outcomes; RNG seed **20261027**) yields descriptive 95% percentile interval **[0, 0.38646652048]** local SDK points. No unexposed-game or post-selection corrected inference.
- The full original per-action frame hashes or ARC SDK replay were **not** executed, so status is **VERIFIED saved arithmetic**, not verified fresh native progression.

## Coursework evidence available and missing

- E128 manuscript (pp4–5) explicitly reports six core arms (72 runs) plus random (12) and PPO controls (24). The 108-row reconstructed matrix retains **all 102 non-completion cells** and flags `provenance=E128_PDF_TABLE1_FIG2_REPORT_ONLY`, SDK per-episode reward/score `NaN`, terminal status `UNVERIFIED_FROM_ORIGINAL_LOG`.
- Core DQN results **0/2/2**, PPO **0/0/1** completions, five total; positive game-seed cells `vc33` 302/303 and `s5i5` 302. Mask-only control's win has **unknown first-reward time**, not imputed. Final DQN-I2 minus PPO-I2: **two positive**, **one negative**, **nine tied** cells. Zero significance/generalisation claims.
- Reported native score & runtimes listed **separately** (not independently verified): DQN-I2 local mean SDK **0.0342**, in-run wall **85.7s**; PPO-I2 **0.0050**, **121.9s**. DQN-I1/2 inherit external pretrained features, so **not equal total compute**.
- Reported DQN-I2 epsilon floor 0.75 after 96 zero-reward steps, 1769 active decisions; **no source-level substantive qualification** determined. Reported PPO-I1 intrinsic bonus 20.49 and PPO-I2 masked 1518 decisions; **PPO log-prob correctness not source-tested**.
- E128 has no true budget-indexed checkpoint/adaptation metric and its cumulative native win event curves cannot meet that requirement alone. No claim that the gap was closed.

## Generated tables and figures

**Tables:** `coursework_108_reported_only.csv`, `coursework_arm_summary_REPORTED_ONLY.csv`, `coursework_DQN_I2_vs_PPO_I2_REPORTED_ONLY.csv`, `e126_matched_75_recomputed.csv`, `e126_by_seed_verified_saved_data.csv`, `e126_by_game_verified_saved_data.csv`, `e126_all_45_arms_verified_saved_data.csv`, `e124_e125_e126_control_summary.csv` (eight CSVs).  
**Figures:** `fig1_coursework_reported_outcomes`, `fig2_reported_event_timing_NOT_learning`, `fig3_e126_family_paired_sdk_delta`, `fig4_e126_first_reward_attainment_NOT_learning`, `fig5_e126_control_ablation_levels` (PDF/SVG/PNG each).  
Each figure's exact caption, source, scientific interpretation, limitation and script included in the ZIP.

## Failures/successes worth reporting without invention

- E126 `s5i5` seeds76–78: N117 zero completed levels, E126 one each; first reward action **23/21/20**, with different charged run lengths. Strongest new-completion local evidence.
- E126 `lf52` seed77: N117 **0 levels/174 actions**, E126 **1 level/233 actions**, first reward at action **33**. Seeds76 and78 show unchanged completed-level count but positive local SDK difference.
- E126 `bp35`: no completed levels across matched seeds; action totals differ, but native `GAME_OVER` vs action-cap censoring is not reconstructible from this per-game CSV.
- N118 archived `tu93` Level-3 branch ends in `GAME_OVER` at 15 actions vs 27 for no-history with no added levels. Earlier termination is NOT efficiency.
- DQN-I1/I2 paper-reported two `vc33` wins at actions114 and21; PPO-I2 one `s5i5` win at136; raw frame histories **not** independently replayed.

## Honest blockers and updated repair interpretation

| Planned task | Disposition | Reason |
|---|---|---|
| RP-01 six-arm source recovery | BLOCKED | Public GitHub experiment index and mounted files lack matching original E128 sources/108 raw runs. Historical `e078_course_recovery` uses different seeds/action cap. |
| RP-02/03 DQN/PPO algorithm verification | BLOCKED | Actual optimizer and PPO rollout source not inspected; no defective implementation presumed. |
| RP-04 DQN-I2 substantive adjudication | OPEN/UNVERIFIED | Manuscript says conditional epsilon rule; source/paired action evidence absent. |
| RP-05 recalculation | PARTIAL | E128 aggregates independently reconstructed **from paper only**; E126 native saved-data aggregates independently verified from source. |
| RP-06 learning/adaptation curves | OPEN/MISSING | Valid within-run event timing plots produced but no actual evolving-policy performance curve. |
| RP-09 informative successes/failures | PARTIAL | E126 per-game and N118 historical source cases extracted; original DQN/PPO actual trajectories absent. |
| RP-10 final coursework comparison | PARTIAL | 12 reported matched cell comparisons made, **not** independently SDK-verified. |
| RP-11 ablations | PARTIAL | Exact E126 controls recomputed; original PPO mask/novelty ablations unverified. |
| RP-12 provenance/resources | OPEN | DQN pretrained encoder cost and peer CNN redistribution permissions not established. |
| RP-07/08 official external submission | OPEN | No authenticated Kaggle/Paper Track/Moodle receipt; no leaderboard mark inferred. |

**Local execution limitation:** direct `git ls-remote https://github.com/Stralb/arc-agi-3-rl-research.git HEAD` failed because the sandbox cannot resolve github.com. Connected GitHub file tools supplied the original table contents. All other calculations were run through the local Python container. The ZIP links in the chat are the exact downloadable generated artifacts; this repository Markdown is a persistent reproducibility/provenance record.
