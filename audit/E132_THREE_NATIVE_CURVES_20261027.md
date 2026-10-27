# E132: Three source-faithful budget-indexed native attainment curves

**Date:** 27 October 2026. **Review project:** `ARC_AGI3_E132_Three_Curves_Project.zip` delivered in this conversation. **Source:** E128 contemporaneous Table 1 and Figure 2 reconstructed as 108 documented game–seed cells; not the missing 72-run original SDK action traces. The E131 review source and E129 originals were preserved, not overwritten.

## Executed
- Built **A baseline** Random/DQN-V0/PPO-V0, **B DQN** V0/I1/I2, **C PPO** V0/I1/I2 as **vector PDF/SVG and PNG** with matching 0–256 charged action x-axis, same y 0–0.203 native completed levels per documented run, identical ticks, exact step events and no smoothing.
- All seven arms represent **12 reported runs each**; unsuccessful runs contribute zero through budget 256. Exactly five recorded events: DQN-I1/I2 each `vc33` seeds303 and302 at actions21 and114; PPO-I2 `s5i5` seed302 at action136. Mask-only positive control has no event time and is deliberately excluded.
- Generated original-source-tier CSV `coursework_documented_native_reward_events.csv` (five rows) and `coursework_cumulative_native_progress_0_256.csv` (7×257=1799 rows), plus reproducible plotting `scripts/build_three_native_curves.py` and independent 45-assertion test `scripts/verify_three_native_curves.py`. **45/45 PASS** locally and after clean ZIP extraction.
- Inserted three real `figure` environments in E131 Section4 baseline, Section5 DQN and Section6 PPO, with captions, limitations and interpretation paragraphs. Compiled `latexmk` without final unresolved citations/references or overfull boxes; rendered and inspected nine PDF pages (eight main pages, references on page9), including Figures 1/2/3 on physical pages4/5/6. Clean ZIP extraction regenerated plots, recompiled the manuscript and yielded **identical extracted PDF text**. ZIP integrity passed.
- Completed PDF SHA-256 `4f7393552aafc423545b2c57f2ffd164a7825be451ef375f264db2e15d74d64a`, LaTeX `cbbd0176d72ff8b8590dc708b404aeef1fda64bb5c003034126a3679427fbe25`, ZIP `1488f5c0a2f0231f671c9a28af78e746f2f38eb0fdf207fee6d611da391354ce`.

## Scientific interpretation and boundary
- Baselines: **0/12** native advances each; cannot imply no optimizer updates.
- DQN I1/I2: both **2/12**, identical first native reward event steps and development family; I2 adds no documented native progression at any budget. Bundled I1 component attribution and DQN-I2 substantive qualification remain unresolved.
- PPO I1 no native progress; PPO I2 **1/12** at action136; mask-only also wins this cell but event time unknown.
- **These are valid within-run native attainment-by-budget plots, NOT independently evaluated learning-checkpoint curves or proof of online policy improvement due to gradients.** The lecturer's distinct learning/adaptation-evidence requirement remains **PARTIALLY addressed**, not closed.
- The archived GitHub research branch `archive/full-research-2026-10-27` documents only the curated N-series/E126 experiment index and its known omissions; exact E127 PDF and original six-arm neural logs/checkpoints were not available. No ARC SDK replay, training or Kaggle submission was performed.

## Deliverables
`ARC_AGI3_E132_Three_Curves_Integrated_Paper.pdf`, `ARC_AGI3_E132_Three_Curves_Integrated_LaTeX.tex`, `ARC_AGI3_E132_Figure_A_Baselines.pdf`, `ARC_AGI3_E132_Figure_B_DQN.pdf`, `ARC_AGI3_E132_Figure_C_PPO.pdf`, `ARC_AGI3_E132_Three_Curves_Project.zip`, `ARC_AGI3_E132_QA_Report.md`.
