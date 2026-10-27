# PROMPT 5 — EXECUTED RESEARCH RECOVERY AND NATIVE SDK SMOKE

**Date:** 2026-10-27 SAST. **Report not rewritten and no original experimental assets altered.** Complete 30-file, 108 KB reproduction package was created in the conversation as `ARC_AGI3_PROMPT5_RECOVERY_20261027.zip`, SHA-256 `8705a1c5c9ddac4afbca3c9b760eeb4e49123ec26eeb6668cbfcf9b4b450fd96`. Internal `RECOVERY_AND_EXECUTION.md`, `SHA256_MANIFEST.json`, `tests/*.py`, source-separated CSV tables, 12-action true SDK JSONL and screenshot, reproducibility logs are included. The package is a new local artifact, not the historical team's complete source archive.

## Access actually verified

- `Stralb/arc-agi-3-rl-research` repository confirmed via connected GitHub. `main@49b966d06afe8ee2a51da100801bf7d5ae63eebf` has 35 tree nodes and `archive/full-research-2026-10-27@a26e40c1aa5d2e224701c0d0d8d0ed61b991c7ba` has 274. Looked across main, archive, E126 release, lecturer cleanup and audit branch trees. **Original E128 72 core plus 36 control raw learner source and runs not exposed in those trees**; this is NOT evidence of experiment nonexecution.
- Bundled SDK/environment archive `/mnt/data/arc-prize-2026-arc-agi-3.zip` and current E134 LaTeX/PDF/figures available locally. Original SDK wheels inside bundle: `arc-agi==0.9.8` and `arcengine==0.9.3` (new smoke only; original E128 version unknown).
- Wits V6 cluster check/login successful as `astrauss`. Restricted root `/home-mscluster/astrauss/research_artifacts` lists unrelated software-security project. **Historical `arc_rl_final_e012` and `e078_course_recovery` were not accessible**; no Slurm job started.
- Separate relevant historical Library files read: `RLC_DRAFT.pdf` (Oct 21 neural N001/N002 reported study), `Pasted text(20260925-205401).txt` (E012 cluster ablation stdout), `Cross_Game_Native_DQN_PPO_Research.ipynb` (Phase3N stub referring to missing 17 Oct source archive), `PHASE3N_PACKAGE_VERIFICATION_20261017.json` (source/checkpoint hash references). No original bytes of their source archives materialized.

## NEW, actually executed SDK test (does not establish DQN/PPO training)

Ran own `tests/sdk_random_smoke.py` on true bundled ARC public-game SDK offline. All 25 public environments discovered. On `ar25-0c556536`, seed47, a simple RNG-selected **legal random action** policy executed **12 charged actions**, with true SDK JSONL frame/action recordings (`save_recording=True`) and `NOT_FINISHED` final state. Newly executed `tests/summarize_sdk_smoke.py` compared authentic consecutive observed 64×64 frames: **12/12 actions had visible pixel effects (1199 cumulative changed pixels), 0 native level advances**. No terminal GAME_OVER, so explicitly **budget-censored**. A four-frame PNG montage uses the official SDK colour mapping. This is a *real random-policy failure*, **not** one of the original coursework DQN/PPO trajectories or an official Kaggle submission. No new neural agent training conducted.

## Recovered original-research cohorts — keep strictly separate

| Cohort | Source | Native records | Mechanism and inference |
|---|---|---|---|
| E128/134 coursework | contemporaneous E128 Table1/Fig2 | 108 documented game–policy-seed cells, 6 positive episodes incl PPO mask-only; 102 failures. First reward 21/114/136 | **Report-derived only**, original optimizer and 108 raw SDK logs missing |
| N001 Oct21 | contemporaneous `RLC_DRAFT.pdf` p3 Table1 | DQN D0/D1/D2 0/4 each, updates 376/440/440; PPO P0 0/4, P1/P2 2/4 each, updates342/81/81 | Evaluated warm-start and intrinsic novelty are **substantive historical changes** but different 4-eval-run cohort |
| N002 Oct21 | same draft p3 Table2 | DQN anchored Q D3 vs frozen actor 6/9 both; KL PPO P3 vs frozen actor 6/9 both | Genuine training claimed, no added matched wins; original source not in inspected workspace |
| E012 Sep25 | original Wits `results/REPORT.md` pasted cluster stdout | 75 development observations per arm; p600 Dueling+D14 .160, no-D14 .040, no-dueling .120, plain DDQN .053 | Independently ablated DQN components but **600-action** protocol not E128 **256-action** comparison |
| Phase3N Oct17 | separate notebook `Cross_Game_Native_DQN_PPO_Research.ipynb` | references 48 frozen validation outcomes all no L1 | Source imports `arc_phase3n_multigame.verify_end_to_end`, `train_multi` and checkpoints absent, therefore not runnable here |
| E126 | 75 paired committed game-seed CSVs | N117 44 vs E126 48 levels; six local score improvement pairs in two exposed families | **Previously verified saved-table arithmetic**, not original DQN/PPO coursework or new SDK replay |

## DQN-I2 critical finding

The current E128/I2 is documented as raising conditional epsilon to at least 0.75 after 96 native-reward-free actions (triggered during a reported 1769/3072 actions) without additional Level-1 completions versus DQN-I1. Original code not inspected. **It remains likely a conditional hyperparameter schedule; a second substantive change in this particular panel has not been established.** The Oct20 event-terminated repeat was a prospective plan, not a verified E128 implementation. Historical N001/D2 novelty or E012/D14 can **only** be presented as their own separately evaluated protocols with accurate results, not silently substituted as E128-I2.

## Tests executed and outputs

1. Official SDK import was initially blocked by missing Flask dependency; recovered required pure-Python Flask/Werkzeug/Blinker wheels from original user ZIP, no external downloads.
2. First SDK action smoke initially identified an atypical `GameAction` enum constructor; fixed by using members returned by enum iteration and checking public available-action values; repeated test **PASS**.
3. `tests/sdk_random_smoke.py` PASS, 12 genuine SDK actions and raw observation recording.
4. `tests/summarize_sdk_smoke.py` PASS, 1199 changed pixels over 12 visually different frames, 0 Level-1 advances.
5. `tests/build_recovery_tables.py` PASS, historical N001/N002/E012 report-only CSVs, separate current 108-coursework-cell and saved E126 tables.
6. `tests/verify_recovered_evidence.py` PASS, 108 unique reported coursework cells and 6 positive rows (102 zeros), 75 E126 matched pairs, E012/N001/N002 distinct cohorts and new SDK smoke assertions.
7. E134 curve verifier **45/45 PASS**, reproducing the 0–256 reported within-run native attainment events. These are **not** neural checkpoint learning curves.
8. E126 saved-data summary verifier **PASS**; no native replay.

## Exact follow-on inputs for Prompt 6

**Available now in current conversation workspace:** `/mnt/data/ARC_AGI3_PROMPT5_RECOVERY_20261027.zip` (all data/reproduction scripts), `/mnt/data/ARC_AGI3_PROMPT5_RECOVERY_20261027/RECOVERY_AND_EXECUTION.md`, `/mnt/data/ARC_AGI3_PROMPT5_RECOVERY_20261027/SHA256_MANIFEST.json`, `/mnt/data/E134_Final_Acceptance/main.tex`, `/mnt/data/ARC_AGI3_E134_Final_Checked_Paper.pdf`; three figure PDFs and builder scripts under `/mnt/data/E134_Final_Acceptance/{figures,scripts}/`. *Raw new local action recording*: `sources/sdk_random_ar25_seed47_12_actions.jsonl` in ZIP. New public frame montage: `results/sdk_random_failure_frames.png`.

**Required from owner's source archives to verify original DQN/PPO:** exact E128 six arms and 108 SDK runs/checkpoints/configs (not located), original `/home-mscluster/astrauss/e078_course_recovery` and `/home-mscluster/astrauss/arc_rl_final_e012`, `arc_phase3n_multigame/{PROTOCOL.json,train_multi.py,verify_end_to_end.py,results/n1}` if using Phase3N. The similarly named `E127_FULL_RUNNABLE_NATIVE_PROJECT_20261021.zip` appears in a *different* temporal-control E128 history and **must not be presumed the original six-neural-arm study**.

**Not available or not run:** original 108 SDK coursework replays, six original neural optimizer/checkpoint tests, verified PPO masked likelihood math, genuine independent learning/checkpoint adaptation performance curve, exact original SDK scoring version, authenticated Kaggle platform entry and class nomination, Paper Track/Moodle receipts and authorship/permissions. Do not upgrade those statuses merely because this smoke succeeded.

**Submission action:** no team code submitted to Kaggle, no project PDF changed, and no cluster SLURM job submitted.
