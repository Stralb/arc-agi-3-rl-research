# Forensic code, outcomes and scientific validity audit
**Date:** 27 October 2026, SAST. **Status:** source/record audit, not a native rerun and not a paper rewrite. **Repo:** `Stralb/arc-agi-3-rl-research`, pinned `main@49b966d06afe8ee2a51da100801bf7d5ae63eebf`, archived `archive/full-research-2026-10-27`. **Paper:** uploaded `ARC_AGI3_E128_Revised_Research_Paper (1).pdf`, 10 physical pages. The specifically named E127 PDF was not available for independent side-by-side versioning.

## Scope, reproducibility and test method
The report is treated as hypotheses/claims, not ground truth. Direct source inspected: frozen N093 Git blob `e9e605c0b4cab51ae3ba4c48d163ae494a8a0a21`, frozen N117 blob `eb6f071c3162a28c902b43c56fce3d89cc8415f3`, E126 blob `84a4d30cc654f141e98ff1a1769d181bbe96c07d`, `src/local_effect_policy.py`, `release/e126_template.py`, `release/build_candidate.py`, `release/manifest.json`, native N114/N117 runner source, published N118/N119/N120 JSON summaries, main E126 CSVs and research archive documentation. GitHub blob contents were retrieved through connected GitHub actions; source text was inspected without modifying the repo.

**Executed safe verification:**
1. Independently parsed `results/e126_per_game.csv` (1,125 rows), `results/e126_all_arms.csv` (45 rows), `results/e126_paired_changes.csv` (36 rows), `results/n093_public25.csv`, `results/n117_public25.csv`, `results/e126_robustness.csv` using a CSV parser supporting quoted commas, and independently computed contrasts and totals.
2. Static inspection of N093/N117/E126 *actual Git blob contents*, verifying exact source-prefix inheritance and key flags. This is not dynamic test execution.
3. Read E128 PDF text and ran local non-native Python arithmetic checks in `/mnt/data/arc3_audit/report_internal_consistency.py`; checked PDF metadata (10 pages, creation 2026-10-27 12:00:37 UTC). The arithmetic checks are **consistency of manuscript numbers only**, not independent validation of original RL actions.
4. Read archived N118 prequential JSON (`data/outputs/experiments/N118/prequential/summary.json`) and N119/N120 native summary JSON.
5. Attempted `git ls-remote` from the analysis container, blocked by unavailable DNS/network; native repo clone and complete offline test suite could not be run locally. Connected GitHub retrieval remained functional.
6. Searched connected GitHub repository and branch indexes plus prior-project file references. Earlier Wits cluster directory listing indicates `/home-mscluster/astrauss/e078_course_recovery` with DQN-V0/I1/I2 and PPO-V0/I1/I2 subdirectories from an **older E078 single-game experiment**. This is promising provenance but not the later four-game/three-seed 72-run source. It is not accessible as a live filesystem in this runtime.
7. No native SDK replay, no new neural training, no model checkpoint load/test, no Kaggle server run and no independent GPU/CPU benchmark were performed. Hash strings in manifests were compared as text; checksums of binary checkpoints were **not freshly recomputed**.

## 1. Coursework six-arm implementation inspection
The actual source of the 72-run DQN/PPO matched study and raw experiment records was **not located** within inspected main/archive indexes. The paper's methodology cannot be upgraded to VERIFIED implementation merely because it is technically plausible. A separate earlier E078 cluster experiment exists by path listing but is not proof of the reported final comparison.

| Arm | Manuscript method (reported, not code verified) | Required primary technical checks | Verdict |
|---|---|---|---|
| DQN-V0 | Two recent frames, previous action, legal index mask; legal-type-uniform epsilon exploration; replay Huber Double-DQN TD; 16 warmup, batch 8, train every 8, sync80, capacity2048 | Network definition/shapes, target sync, detached bootstrap, correct terminal/truncation, optimizer steps, replay samples and log entries | UNVERIFIED |
| DQN-I1 | Legal-candidate dueling Double DQN; D14 structured exploration; externally frozen effect representation | Compare actual code to V0; verify weighted candidate enumeration, click coverage, pretrained weights, actual gradients and separate training budget; identify which package component caused difference | UNVERIFIED |
| DQN-I2 | DQN-I1 plus raise structured epsilon to >=0.75 after 96 consecutive un-rewarded actions | Locate actual threshold and counter reset logic, choose-action branch, epsilon scheduling, number of **different actions** vs I1, confirm other changes fixed | UNVERIFIED / potential borderline substantive intervention |
| PPO-V0 | Factorised type/click policy, clipped PPO, GAE, 64-action rollouts, epsilon clip .2, lambda .95, 4 epochs/4 minibatches, learning rate 2.5e-4 | Actor and critic parameter updates, old versus new log-probs, type mask and click mask, entropy, advantage/terminal semantics, sample reuse, total losses | UNVERIFIED |
| PPO-I1 | Novelty bonus 0.02*1[visual change]/sqrt(count(phi(next observation))) included in training return | Verify count initialisation, no divide-by-zero at first visit, observed-before-updated counts, no bonus passed into native SDK score or termination; compare same budgets and seeds | UNVERIFIED |
| PPO-I2 | PPO-I1 + modal-colour >=65% and >=4 legal non-modal click positions, masked selected click logprob stored for PPO updates | Verify mask **recomputed from stored observation or stored with rollout** for new-policy logprob; old/new conditional distributions normalise over **same support**; type and click factor and entropy handled consistently | UNVERIFIED |

### DQN-I2 determination
A thresholded, reward-stall-dependent epsilon adjustment is a *conditional exploration scheduler*, not intrinsically a new learning objective or architectural mechanism. On the **paper description alone**, it is **borderline / likely a hyperparameter-centred intervention** because its only stated effect is `epsilon=max(epsilon,0.75)` after 96 unrewarded actions. The paper reports 1,769 activated decisions and **zero additional native completions** relative to I1, with identical first-reward seeds/times; this supports execution of a trigger only if original logs confirm, but **does not demonstrate altered action choices or better learning**. Do not make a definitive lecturer qualification decision until its actual source/config and paired action differences are examined. A static threshold is not made substantive just by running it under a condition. If code shows a distinct recovery policy with state-dependent candidate selection or another mechanism, revise classification accordingly; do not invent it.

### PPO-I2 mathematical audit boundary
For click action `a=(k=6,x,y)`, a correctly masked factorised policy has `logpi(a|h,M)=logpi_type(6|h)+logpi_xy((x,y)|k=6,h,M)`. PPO's `rho=exp(new_logpi(a|h,M)-stored_old_logpi(a|h,M))` is valid only if **old sampling and new evaluation use the identical mask support for that stored transition**. Invalid click logits must be excluded before normalisation and the current observation must reconstruct the correct mask (or mask must be retained). For primitive actions, no pixel-coordinate term should be added. The paper's statement that masked old logprobs were stored is necessary but insufficient. No code or rollout tensor was available to establish mathematical correctness. A separate masked-policy correctness test would be needed.

## 2. Coursework numerical sanity checks
| Claim | Check | Result/interpretation |
|---|---|---|
| Six arms, 4 games, 3 seeds | 6*4*3 | 72 (internal arithmetic VERIFIED) |
| Each arm at most 256 native calls per run | 4*3*256 | 3,072 ceiling per arm; **not a verified actual action total** without logs |
| 12 random + 24 PPO controls | (6+1+2)*4*3 | 108 total experiments in Figure 2 if all ran (internal consistency) |
| Six-arm recorded completions | 0+2+2+0+0+1 | Five rewarded episodes over 72; only three distinct successful game-policy-seed cells as described |
| DQN warmup 16, every 8, 256 calls | (256-16)/8*12 | 360 scheduled optimizer steps under the simple post-warmup convention; DQN-V0/I2 report 360, DQN-I1 reports **361**. Not proof of error—requires exact update condition/replay implementation |
| PPO 64-step rollouts, 4 epochs × 4 minibatches | 256/64 *4*4*12 | 768 (consistent with all PPO arms and ablations) |
| First native rewards | DQN-I1/I2 vc33: seeds302@114 and303@21; PPO-I2 s5i5: seed302@136 | Present in PDF but primary run logs UNVERIFIED |
| Native mean scores 0.0342 / 0.0050 | Need per-run SDK scores and human-normalization source | UNVERIFIED; cannot recompute from sparse rewarded-cell labels |
| Intrinsic 20.49, DQN I2 1,769 triggers, PPO I2 1,518 masks | Need per-step event logs | UNVERIFIED |
| Runtime 10.3/64.2/85.8/85.7/125.1/121.8/121.9 sec | Need source timestamp/resource logs | UNVERIFIED |
| Every arm reports exactly 3,072 actions | 12*256 exact cap, even though native games can terminate before cap | **FLAG**: could be valid full budgets, in-run resets or mislabeled action ceilings. Original native action records and handling of `GAME_OVER` must decide. Do not assert contradiction without logs |
| Learning curves | Figure 2 is cumulative within-run reward timing | **VERIFIED report admission:** no independently evaluated intermediate policy checkpoints; mandatory learning/adaptation curve incomplete |
| Natural episode failures vs 256 budget | Need terminal/censor labels | UNVERIFIED; early GAME_OVER should not be called 256 real charged actions without corresponding permitted reset protocol |

All "internal arithmetic" passes establish only that a narrative is self-consistent. None independently verifies a DQN optimizer, PPO gradient, native frame, runtime, seed independence, official score, or genuine learning.

## 3. Exact E126 implementation lineage
**Source-blob static test PASS:** `N117_source.startsWith(N093_source)`, and `E126_source.startsWith(N117_source)`. This checks the retrieved *actual Git blobs*, not just claims in README. N093 1,671,889 characters, N117 1,683,773, E126 2,620,230 (characters as returned by GitHub connector, not byte sizes).

- N093 `PortableAgentCore`: pretrained `ValueNet` weights loaded from frozen checkpoint and set to `.eval()`; trained neural policy probabilities evaluated under `torch.inference_mode()`. No optimizer is called in the acting core. The online learner uses empirical `Counter` transition frequencies, optimistic `Q=1`, `gamma=.985`, Bellman backups and bounded predecessor propagation. `num_updates` is **backup count**, not gradient step.
- N093 `PretrainedPUCTCore`: Level 1 inherits B1 choice, Level 2+ uses `Q + c*prior_probability/(1+visits)` with `c=.1`, temperature 2.0. **No planning simulations / MCTS search tree**.
- N093 input: 64x64 frame, legal type mask; six simple types index 0–5 (native actions 1–5,7) plus 4,096 ACTION6 click positions index 6–4,101. Candidate proposals initially select connected components / grid points and may expand; not a flat 4,102-way PPO actor.
- N093 `observe`: `r=float(levels_completed>before)`; non-native pixel differences go to effect hypotheses only; reward/terminal edges suppress bootstrap. On level advance Q nodes/visits reset; hypotheses from earlier levels persist with separate discount; full game reset clears them. No proof this state is a complete POMDP belief.
- N117 `AuditedCrossLevelCore`: conservative level-2+ action-score modification based on within-level descriptor-conditioned effects; does not change Bellman reward. It clears short effect history at level change and inherits prior hypothesis lifecycle.
- E124: rarity term and per-click-colour observed local-versus-global change contingency; `_local_bonus` selects click coordinates with no new game source oracle. Positive colour-response observations are updated only after charged native actions.
- E125: peer `_Effect126` CNN with 3 convolutional layers (16→32→64→96), 128-d projection and action-conditioned head. It operates on current and previous frames; **hist_grid/hist_mask arguments are unused in the retrieved temporal forward**. `load_state_dict(...,strict=True)`, `.eval()`, `requires_grad_(False)`, `torch.inference_mode()`. It is **frozen auxiliary effect prediction**, not RL control training.
- E126: for Level 1 only, when click is legal, no actions 1–5 legal and frame modal colour >=0.80, trained CNN scores candidate clicks; otherwise E124 local click ranking. **Level 2+ delegates to N117**. Static search of E126 extension found no PPO/policy gradient code, no `.backward()` or `optimizer.step()`, no known game-ID branch. Core constructed `learning=True` enables empirical online Q backups, not CNN fine-tuning. Teammate checkpoint redistribution permissions unresolved.
- Limitations: selected 0.80 gate is post-hoc on exposed public families and can be distributionally identifying; source absence of explicit game IDs alone does not prove novel-game generalisation.

## 4. Recalculated E126 numerical evidence
Primary observed source: 1,125 per-game CSV rows = 45 arms×25 games, plus 36 paired-difference records. 45 arm rows sum to **125,220 reported charged actions**, which cross-checks the archived `integrated_audit.json` aggregation (but not original native traces). Main seed results:

| Seed | N117 levels | E126 levels | N117 mean SDK | E126 mean SDK | E126 actions | Changed trajectories | Score-positive games | Added levels |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 76 | 15 | 16 | 2.0932423408 | 2.2115182587 | 2,872 | 10 | lf52,s5i5 | 1 |
| 77 | 14 | 16 | 2.0547750230 | 2.2239424189 | 2,873 | 9 | lf52,s5i5 | 2 |
| 78 | 15 | 16 | 2.0964346368 | 2.2407370400 | 2,887 | 9 | lf52,s5i5 | 1 |
| Total / mean | | | **2.0814840002** | **2.2253992392** | **8,632** | **28/75** | **6/75 pairs** | **4** |

- Difference in mean local SDK score = **+0.1439152390** (6.913% relative, rounded paper 6.9%). All 23 other game families tied at zero difference for each of the three seeded E126 matched comparisons.
- `s5i5` total paired score contribution across seeds = 7.3977031827 points (68.5376% of all positive paired points), with native first-win steps **23, 21, 20** (seeds 76,77,78) versus none for baseline.
- `lf52` positive paired score contributions 0.8564988730, 1.7096585692, 0.8297823018. First-win steps E126 **31, 33, 33**, baseline **44, no win, 46**. Only seed77 adds a level, others improve action efficiency on the already-completed L1.
- The 28/75 figure is **VERIFIED against stored paired changed_trajectories counts** 10+9+9. The stronger assertion "first different action had identical preceding observation/frame hash" remains **SUPPORTED BUT LIMITED** because original frame trace bytes were not replayed here.
- Random-weight and salience E126 controls change 10+9+9=28 trajectories each and yield a positive score on `lf52` only in each seed (three score-positive pairs; one extra level for seed77). These results support selectivity but **do not uniquely attribute the lf52 gain to learned contingency**.
- On E124 seed76, rarity-only and effect-only both reproduce the same local score gain on `lf52`; thus sole-mechanism causal attribution is invalid.
- Additional policy/native seed pairs 79–82 have local SDK score deltas 0.134875381, 0.037532222, 0.0331912921 and 0.128988431 (all positive). `different_initial_frames_vs_seed47` is zero for all four records; not four new novel layouts.
- **Native replay not independently performed**; official RHAE / private score not derivable from these CSVs.

## 5. Independent checks of historical N118/N119/N120 summaries
- N118 archived prequential JSON has L2+ `n=1197`, `positive=851`. Brier: nohistory 0.169102, real history 0.151572, corrupted 0.162504. False negative rates 0.052879→0.122209 (10.37% relative Brier decrease and 6.933 percentage-point FNR increase). **VERIFIED as original saved summary numbers**, not independent replay.
- N119 archived native summary records 100 episodes, delay-credit 2 L2/0 L3, risk-only 2 L2/0 L3 and no extra completions. State-return-risk-only has 25 exact trajectory matches to local baseline, so it cannot be credited with changing native decisions.
- N120 archived native summary shows N093 13 L1/1 L2, N117 13 L1/2 L2, and MC prior 13 L1/2 L2, all zero L3. Source report's absent rewarded L3 trajectories explains data-support limit, not inability of general RL algorithms in principle.

## 6. Official Kaggle provenance contradiction
E128 p7 **reports** four official submissions: random 0.00 ID 57499040, separate DQN V2np 0.21 ID 57664781, N117 0.33 ID 57675023, E126 0.33 ID 57690887. The manuscript reports E126 source SHA-256 prefix/suffix matching the `release/manifest.json` hash `84f27a2589575558ddb85dff2539f68d1937c6dc1a048cb3b133f6ae7005178c`. The actual manifest says `official_kaggle_submission: false` and `candidate_not_submitted`; archived E126 results state zero official submissions. **Both observations are authentic source observations, their chronology unresolved.** Main source latest inspected commit 2026-10-27 09:32:41 UTC and paper creation 12:00:37 UTC, so a real later submission is possible. No independent Kaggle receipt, server timestamp, notebook ID, leaderboard URL or checksum retrieval was performed. Therefore Kaggle score is **UNVERIFIED with contradictory earlier status metadata**, **not independently confirmed and not disproved**. Reported tie at 0.33 cannot be used to establish private/generalization benefit.

## 7. Claim-by-claim evidence ledger
| CLAIM_ID | Exact claim (or bounded paraphrase) | Primary source | Verification method | Status | Contradictory evidence / limitations | Required correction |
|---|---|---|---|---|---|---|
| F-001 | DQN-V0 used a trained network, Double DQN objective and actual gradients | E128 p3 | PDF inspection; raw trainer not found | UNVERIFIED | N093 empirical Bellman is **different** code | Recover actual DQN source, logs and checkpoint |
| F-002 | DQN-I1 contains dueling candidate scorer + D14 + frozen effect features | E128 p3 | PDF; repository archive search | UNVERIFIED | Intervention bundles multiple mechanisms | Recover exact diff/config and provenance |
| F-003 | DQN-I2 uses stall-triggered epsilon≥.75 after 96 unrewarded actions | E128 p3 | PDF only | UNVERIFIED | Could be primarily hyperparameter scheduling | Examine source and paired action selections |
| F-004 | DQN-I2 changed 1,769 action decisions | E128 p4 says trigger active 1,769 | Textual distinction | UNVERIFIED | Trigger activation ≠ chosen action changed; I1/I2 reward outcomes identical | Report trigger vs actual different actions separately |
| F-005 | DQN-I1 completed 2 native levels and I2 2, baseline 0 | E128 Table1/Fig2 | Internal counts consistent | UNVERIFIED | 72 raw records absent from accessible repo | Recover and recalculate each run's levels |
| F-006 | DQN-I1 had 361 optimizer updates; V0/I2 360 | E128 Table1, methods | Mathematical schedule cross-check | UNVERIFIED / FLAG | 361 exceeds simple 16-warmup/every8 360 expectation by 1 | Explain source update condition or correct log summary |
| F-007 | PPO uses a correctly implemented clipped ratio and GAE | E128 Eq2/p3 | Equation conceptual review only | UNVERIFIED | No old/new logprob code or rollout tensors | Verify actor/critic source and tensor-level tests |
| F-008 | PPO novelty bonus never affects native SDK score | E128 Eq3/p3 | PDF and unrelated N-series source only | UNVERIFIED | Must audit target computation and metric logging | Recover actual PPO rewards and scorer |
| F-009 | PPO-I2 masked foreground clicks and stored proper masked logprob | E128 p3–5 | Mathematical requirement derived | UNVERIFIED | Logprob storage alone insufficient, needs same support | Inspect sampling, stored mask, evaluation and ratio |
| F-010 | PPO-I2 single native win, mask-only also wins, no-updates 0 | E128 p4–5 | PDF internal consistency | UNVERIFIED | No 24 ablation raw records/paired trajectories | Recover ablation source and run records |
| F-011 | 72 core runs, 108 including controls | E128 p4–5 | 6×4×3, 9×4×3 | VERIFIED arithmetic only | No raw episode file | Recover filenames/trace manifests |
| F-012 | Every arm spent 3,072 real charged SDK actions | E128 Table1 | Equals exact per-arm max | UNVERIFIED / FLAG | Native GAME_OVER may end earlier; possible resets or ceiling mislabeled | Audit actual calls, terminal handling and reset charges |
| F-013 | DQN/PPO first win step, score and wall time exactly as Table1 | E128 p4/Fig2 | No primary rows | UNVERIFIED | No timestamps, scorer version or native logs | Recover raw records and recompute |
| F-014 | Genuine training/adaptation curves are available | E128 p5 | Read admission | CONTRADICTED if claimed; E128 itself says incomplete | Fig2 within-run progress is NOT saved-checkpoint learning curve | Disclose incompleteness, recover checkpoint series only if recorded |
| F-015 | N093 Bellman value learner updates on native level advance | `src/frozen_n093.py` Git blob | Static source: `observe`, `_backup`, `_observe_q` | VERIFIED code | Neural prior is frozen, Bellman backups not gradients | Keep terminology precise |
| F-016 | N093 late-level PUCT is one-step ranker, not deep MCTS | `src/frozen_n093.py` | Code implements `Q+cP/(1+N)` without simulation | VERIFIED code | No search-tree planning | Retain caveat |
| F-017 | N117 extends N093 without changing native reward semantics | N117 and N093 blob text | Exact prefix and policy inspection | VERIFIED code | Actual native replay still owner-held | Describe effect bonus as selection-only |
| F-018 | E126 extends N117 exactly; no PPO or acting-time policy gradients | E126/N117 Git blob text | Exact prefix plus extension static search | VERIFIED code | No dynamic model-load validation | Do not call ensemble |
| F-019 | E126 frozen peer CNN and sparse Level-1 gate | `release/e126_template.py` | Source inspection | VERIFIED code | Gate post hoc and may identify exposed layouts | Call auxiliary effect prior, not reward learner |
| F-020 | E126 long temporal history tensor is used | `_Temporal126.forward` | Static forward-variable-use inspection | CONTRADICTED for tensor history use | Only current/previous frames processed, `hist_grid/hist_mask` ignored | Do not assert long-history inference from unused args |
| F-021 | E126 16 levels each of three seeds, N117 15/14/15 | 1,125 per-game CSV | Independently summed per game | VERIFIED recorded data | No SDK replay | Cite as source-verified public results |
| F-022 | E126 28 changed trajectories, 6 SDK-positive pairs, 4 extra levels | Paired and per-game CSV | Independently recomputed | VERIFIED recorded data | Exact pre-frame-hash match not independently replayed | Separate trajectory-change count from matched hidden-state proof |
| F-023 | E126 gain concentrated in s5i5 (68.5%) and lf52 | Per-game CSV | Independent score differences | VERIFIED recorded data | All families previously exposed | No new-game generalisation claim |
| F-024 | Original 1,125 E124–E126 episodes covered 125,220 real SDK actions | `integrated_audit.json`, per-arm CSV | Sum arms agrees with archived audit | VERIFIED aggregate arithmetic | Original raw native archives not executed | Do not call it fresh independent replay |
| F-025 | N118 Brier .169102→.151572, FNR 5.29%→12.22% | Archived N118 prequential JSON | Read exact stage `L2+` | VERIFIED recorded summary | Not proof of better control; different policy distributions | Keep objective separation |
| F-026 | E126 official Kaggle 0.33, ID57690887, matching source SHA | E128 p7 vs repo manifest | Source/version chronology crosscheck | UNVERIFIED, source status CONFLICT | Manifest says not submitted; later paper possible | Obtain official receipt, source hash and time |
| F-027 | Mean E126 SDK 2.081484→2.225399 | 75 per-game records by stage | Independent averaging | VERIFIED recorded data | Public SDK ≠ official Kaggle score | Keep separate metrics |
| F-028 | E126 improved unseen-game generalisation | E128 explicitly disclaims | Source archives inspect development exposure | CONTRADICTED if claimed | 25 public games used during model selection | Keep strictly exploratory claim |
| F-029 | E126 CNN trained online from Kaggle rewards | Frozen model source | No extension gradients, eval()/inference_mode | CONTRADICTED if claimed | Only online empirical Q + click counts | Never call CNN online RL |
| F-030 | E128's action-frame first divergence at s5i5 step3 | E128 p7 | Need source per-step pre/post SHA traces | SUPPORTED BUT LIMITED | Paired CSV counts do not prove first divergence index | Recover E127 owner-held trace ZIP |

## 8. Scientific correctness and mechanism findings
1. **CONFIRMED:** The research correctly separates visual-effect prediction and native level progression in the E126 source and historical N118 dataset. Prediction accuracy is not reward.
2. **CONFIRMED:** "Action choices changed" is weaker than "reward improved"; E126's 28/75 → 6/75 → 4 pattern supports this hierarchy.
3. **CONFIRMED:** E126 is not DQN+PPO; it is an empirical Bellman online value learner with frozen trained priors and observation-driven click bonuses.
4. **LIMITATION:** E126 post hoc sparse-scene gating and repeated known layouts prevent claims of clean unseen-game generalisation. Its family-bootstrap interval includes zero and is descriptive, not a new-game confidence interval.
5. **LIMITATION:** E126 uses frozen teammate pretrained weights; total compute and permissions matter, especially if comparing against models trained from scratch.
6. **OPEN:** DQN I1 aggregates several mechanisms; it cannot identify one causal driver without a component ablation.
7. **OPEN:** DQN I2's epsilon trigger may be too close to tuning; no verified code/paired changed-action evidence.
8. **OPEN:** PPO I2 probability-ratio correctness is essential and presently unsupported by executable source. This is a technical correctness blocker, not a style concern.
9. **OPEN:** Native calls versus fixed upper bounds, episode ending and resets in the 72-run panel are unverified. A short failure may end in GAME_OVER before the cap.
10. **OPEN:** Official E126 score and submission source-hash provenance remain not independently established.

## 9. Repairs prioritised for audit (not paper rewrite)
**P0:** find the exact dated DQN/PPO trainer and logs for all 72 + 12 + 24 runs; unit-test PPO masked old/new logprobs and DQN target branch; verify DQN I2 code and per-action difference; reconcile official Kaggle receipt and code checksum.

**P1:** recompute all DQN/PPO per-run outcomes/updates/runtime from original files; classify `GAME_OVER` versus budget stop; reveal all resource/pretrain costs; locate E126 raw E127 trace ZIP and run hash/native replay; verify effect checkpoint bytes/permissions.

**P2:** record true checkpoint/adaptation curves if available, provenance of figures, and report exact residual uncertainties. Do **not** produce fabricated controls, invent learning curves or rewrite manuscript now.

## Paths and original evidence locations
- GitHub research repository: https://github.com/Stralb/arc-agi-3-rl-research
- Archived research source: https://github.com/Stralb/arc-agi-3-rl-research/tree/archive/full-research-2026-10-27
- Original E126 8.75 MB trace ZIP referred in archive: `~/research_artifacts/mcp_uploads/jobs/click_integrated_audit_e127_20261026/analysis/E124_E125_E126_FULL_NATIVE_EVIDENCE.zip` on Wits cluster (not accessed).
- Earlier E078 single-game coursework runs in prior directory listing: `/home-mscluster/astrauss/e078_course_recovery/E078_native_vc33_160_seed28901_71805/` etc (not accessed).
- E128 local internal arithmetic audit output in this conversation's container: `/mnt/data/arc3_audit/report_internal_consistency.json`; this file contains only manuscript arithmetic, not native results.
- See `audit/EVIDENCE_LEDGER.md`, `audit/REPAIR_REGISTER.md`, `audit/SUBMISSION_CHECKLIST.md` and `audit/REQUIREMENT_TO_EVIDENCE_MATRIX.md` for cumulative requirement tracking.
