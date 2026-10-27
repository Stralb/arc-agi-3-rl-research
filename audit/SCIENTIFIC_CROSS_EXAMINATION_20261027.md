# FORMAL SCIENTIFIC CROSS-EXAMINATION — ARC-AGI-3

**Date:** 27 October 2026 SAST. Impartial simulated moderator. Lecturer: RL_Assignment(1).pdf pp1–5; paper: E128 pp1–10; repo Stralb/arc-agi-3-rl-research (main source baseline 49b966d, archived branch archive/full-research-2026-10-27); prior prosecution/defence audit records. **No original DQN/PPO training execution, SDK replay, or authenticated Kaggle receipt was obtained in this hearing.**

**Ruling semantics:** RESOLVED means a precisely narrowed claim is answered with observed evidence; PARTIALLY RESOLVED means a material part remains open; UNRESOLVED lacks decisive evidence; CONTRADICTED means two same-scope verified sources are incompatible even after considering chronology.

## CX-01 — DQN-I2 substantive improvement

**Step 1 — Prosecution question.** Does the DQN-I2 implementation do more than raise epsilon to at least 0.75 after 96 native-reward-free actions, and can changed exploration be demonstrated against I1?

**Step 2 — Defence answer.** A reward-conditioned stall response can be behaviorally meaningful even without another completion; lecturer explicitly accepts well-motivated negative results.

**Step 3 — Evidence test.** E128 §3.2 reports unchanged Bellman target, I1 architecture, 1,769/3,072 stall activations and same two vc33 wins at first-reward steps 114/21. Source-level DQN-I2 and original run logs remain outside inspected GitHub main/archive indexes. The N-series policy is a different lineage.

**Step 4 — Rebuttal.** The intervention could be primarily a conditional epsilon schedule, which the lecturer may view as tuning. The activation number is paper-reported and not independently verified.

**Step 5 — Moderator ruling.** **UNRESOLVED. Borderline described method; no proof it is a substantive second improvement or that it is defective. Need actual code, triggers, reset, action divergence and ideally epsilon-only matched control.**

## CX-02 — DQN-I1 particular-component attribution

**Step 1 — Prosecution question.** Which separate component—dueling candidate scorer, D14 exploration or frozen effect representation—is shown to cause the recorded gain?

**Step 2 — Defence answer.** Assignment permits an evaluated bundled intervention; E128 explicitly calls I1 a complete candidate-selection redesign, not an isolated component study.

**Step 3 — Evidence test.** E128 §3.2 says multiple mechanisms were changed together, p8 concedes causal isolation missing. N117/E126 ablations concern another controller and do not isolate DQN-I1.

**Step 4 — Rebuttal.** No unique subcomponent effect is identified. A full-bundle V0-to-I1 effect is plausible if original results verify.

**Step 5 — Moderator ruling.** **RESOLVED (narrow). Component-specific causation not established; bundled intervention is not automatically a rubric violation. Preserve treatment-level language; component ablations only if real.**

## CX-03 — PPO-I2 mask-only ablation

**Step 1 — Prosecution question.** Does the mask-only arm demonstrate foreground masking itself caused the PPO-I2 result, with all other training/seed/log-probability machinery matched?

**Step 2 — Defence answer.** Reported mask-only and combined I2 each win s5i5 at seed 302; mask-only has zero novelty and 768 updates, no-updates control has zero wins, supporting novelty not needed in that one case.

**Step 3 — Evidence test.** E128 Table1/Fig2 and p5 describe these results and acknowledge mask-only first-reward time missing. The original PPO/control source and 24 control logs were not located; no mask/log-prob replay performed.

**Step 4 — Rebuttal.** The observed case supports narrow nonnecessity of novelty if records verify, but not a robust mask causal effect or PPO mathematical correctness.

**Step 5 — Moderator ruling.** **PARTIALLY RESOLVED. Scope of inference narrow and correct; implementation/ablations still require original rollout and update logs.**

## CX-04 — Learning/adaptation curves

**Step 1 — Prosecution question.** Does Figure 2 show a change in learned policy effectiveness or online adaptation performance against interaction budget, rather than simply when occasional first rewards occurred?

**Step 2 — Defence answer.** The event-time plots show native progress and failures, and the lecturer allows adaptation curves rather than requiring separately saved checkpoints exclusively.

**Step 3 — Evidence test.** Assignment §5 p3 requires learning or adaptation curves against interaction budget. E128 p5 explicitly calls Figure 2 cumulative within-run events, not independent checkpoint learning curves, and says required evidence remains incomplete.

**Step 4 — Rebuttal.** Reward-event time is useful but not a demonstrated learning/adaptation curve. Archived measurement may exist but was not recovered.

**Step 5 — Moderator ruling.** **RESOLVED. Confirmed assessment-reporting gap. Use real budget-indexed adaptation metrics or preserve limitation; do not relabel event-time curves.**

## CX-05 — Three seeds and heldout generalisation

**Step 1 — Prosecution question.** Do three different policy RNG seeds on fixed, previously exposed games constitute independent evaluation on unseen game families or mechanics?

**Step 2 — Defence answer.** Three seeds measure conditional stochastic sensitivity; assignment requires a holdout split where public data permits and explicit exposure disclosure. E128 disclaims unseen generalisation.

**Step 3 — Evidence test.** Course study: ar25, g50t, s5i5, vc33, seed 47, policy seeds 301–303, 256 actions. E126: 25 repeatedly exposed games x policy seeds 76–78. E126 robustness CSV reports zero changed initial frames for four native seeds 48–51; archive N117 PROTOCOL calls its test games historically exposed.

**Step 4 — Rebuttal.** Multiple policy seeds are meaningful within-game variability but cannot create novel environments; this is not necessarily a rule breach when disclosed.

**Step 5 — Moderator ruling.** **RESOLVED. No unseen-game generalisation established; manuscript is appropriately limited. Genuine prospective unexposed test could change finding.**

## CX-06 — DQN/PPO training and evaluation fairness

**Step 1 — Prosecution question.** Are the DQN/PPO agents matched in all-in learning data, compute, pretrained priors and training/evaluation costs, or only charged online actions?

**Step 2 — Defence answer.** E128 reports identical four game/three policy seed/256 native action conditions, explicitly excludes prior pretraining cost and discloses externally pretrained frozen DQN I1/I2 representations. Lecturer permits justified unequal budgets.

**Step 3 — Evidence test.** E128 §4 Table1 gives per-arm runtime and says it excludes the pretrained model cost. The later E126 peer CNN is a different model and does NOT prove DQN-I1 training cost. Original course source and training logs unavailable.

**Step 4 — Rebuttal.** Online action ceilings are reported matched, but all-in exposure/compute not matched or quantified. Disclosed disparity is not concealment.

**Step 5 — Moderator ruling.** **PARTIALLY RESOLVED. Fair online budget comparison reported; all-in fairness unresolved. Need separate pretrained, online and evaluation cost/source records.**

## CX-07 — Prediction accuracy and native control

**Step 1 — Prosecution question.** Does the improved N118 visual-action-effect prediction establish more reward-grounded control success?

**Step 2 — Defence answer.** The paper says better visual prediction does not guarantee better native progress. Some gated use of a trained effect prior in E126 has narrow local positive results.

**Step 3 — Evidence test.** Archived reports/N118_FINDINGS.md says prequential Brier 0.169102 to 0.151572, false-negative rate 5.29% to 12.22%, and no history/no-history/placebo arm exceeds 15 levels; these are source-reported summaries, raw 1,197 predictions were not rerun. Independently reaggregated E126 per-game CSV: four extra levels/75 and positive score differences in only s5i5 and lf52.

**Step 4 — Rebuttal.** N118 supports a negative causal-inference warning, not a theorem that better predictors cannot help. E126 has limited public game successes but cannot prove general transfer or unique mechanism.

**Step 5 — Moderator ruling.** **RESOLVED (narrow). Prediction calibration alone does not demonstrate learned native control; E126 gains remain a separate limited observation.**

## CX-08 — E126 actual architecture

**Step 1 — Prosecution question.** Does the deployed E126 policy inherit DQN/PPO acting networks, or an empirical N093/N117 Q-controller with a frozen pretrained CNN only in a Level-1 sparse-scene click-ranking gate?

**Step 2 — Defence answer.** E128 explicitly draws separate lineages and says E126 has no acting PPO weights/gradient updates.

**Step 3 — Evidence test.** Directly inspected archived experiments/E126/e126_template.py: E126Core subclasses N117 core; model load verifies peer checkpoint SHA, sets eval() and requires_grad_(False); _rank_ties returns super() for self.level>=1; otherwise if legal ACTION6, no directional actions 1–5 and modal colour >=0.80, uses peer effect ranking; otherwise local rarity/click-contingency bonus. N093 source has empirical Bellman backups and PUCT one-step scoring.

**Step 4 — Rebuttal.** The exact gate does not explicitly require ACTION7 illegal; phrase 'click-only' is imprecise if taken literally. The source architecture does not itself prove a successful official Kaggle deployment.

**Step 5 — Moderator ruling.** **RESOLVED (architecture). E126 is not a DQN/PPO ensemble. Use exact gate wording and keep external submission/trace replay separate.**

## CX-09 — Kaggle vs local score

**Step 1 — Prosecution question.** Does the manuscript conflate local SDK scores with official Kaggle public scores, and is reported E126 Kaggle 0.33 independently confirmed?

**Step 2 — Defence answer.** E128 Table1 labels local SDK 0–100 score; p7 separately lists official Kaggle claim ID 57690887 score 0.33. Earlier not-submitted manifest could predate a later submission.

**Step 3 — Evidence test.** Main release/manifest.json and archived E126 README mark candidate not submitted at their snapshot. E128 p7 asserts later official submission. No official platform receipt retrieved; public web search did not verify the submission ID. Independently reaggregated committed CSVs: N117 mean 2.0814840002, E126 mean 2.2253992392, six positive game-seed score pairs and four added levels; none equals or verifies Kaggle 0.33.

**Step 4 — Rebuttal.** Metric separation is correct. A genuine Kaggle receipt/score/time/source artifact remains unverified; no contemporaneous contradiction or misconduct inference established.

**Step 5 — Moderator ruling.** **PARTIALLY RESOLVED. Score definitions are distinct; official E126 submission success, class team and source hash remain unresolved.**

## CX-10 — End-to-end reproducibility

**Step 1 — Prosecution question.** Can a third party reproduce all six coursework trained variants and all native E126 episodes from the public repository alone?

**Step 2 — Defence answer.** The repo contains N093/N117/E126 source, archived SDK runners, checkpoint, notebook, deterministic builder, hashes, CSV result tables and verifier scripts; it explicitly acknowledges being a curated distribution.

**Step 3 — Evidence test.** Main scripts/verify_repository.py checks source SHA/AST, table sums and SVG presence and explicitly makes no SDK calls. scripts/verify_e126_release.py checks four artifact hashes, notebook/source match, 45x25 rows, mean scores and robustness, and asserts historical official_kaggle_submission false; it explicitly does not run official Kaggle. Archived docs/REPOSITORY_COVERAGE.md documents 1,355-entry offline ZIP with original traces omitted and original authorized SDK needed. Archive experiments/INDEX.md has no six-arm original DQN/PPO index.

**Step 4 — Rebuttal.** Published frozen code and saved arithmetic are reproducible in principle. Native reruns, full historical trace replays, and coursework learning are not established from public subset; dependencies/rights incomplete.

**Step 5 — Moderator ruling.** **PARTIALLY RESOLVED. Source/CSV/hash-level audit is possible, end-to-end native + coursework reproducibility is not yet demonstrated.**

## Final classification

| Issue | Ruling |
|---|---|
| CX-01 — DQN-I2 substantive improvement | **UNRESOLVED** |
| CX-02 — DQN-I1 particular-component attribution | **RESOLVED** |
| CX-03 — PPO-I2 mask-only ablation | **PARTIALLY RESOLVED** |
| CX-04 — Learning/adaptation curves | **RESOLVED** |
| CX-05 — Three seeds and heldout generalisation | **RESOLVED** |
| CX-06 — DQN/PPO training and evaluation fairness | **PARTIALLY RESOLVED** |
| CX-07 — Prediction accuracy and native control | **RESOLVED** |
| CX-08 — E126 actual architecture | **RESOLVED** |
| CX-09 — Kaggle vs local score | **PARTIALLY RESOLVED** |
| CX-10 — End-to-end reproducibility | **PARTIALLY RESOLVED** |

## Confirmed implementation defects and assessment gaps

**Confirmed actual implementation defects in original DQN/PPO: NONE established.** Source not available for decisive verification. **Confirmed reporting/assessment gap:** assignment §5 budget-indexed learning/adaptation curve is incomplete; E128 p5 explicitly concedes. **Confirmed paper submission gap:** E128 p8 individual contributions still to be confirmed. **Unverified rather than proven missing external artifacts:** official Kaggle entry ID57690887 and class nomination, Moodle ZIP/receipt and Paper Track submission. Minor E126 precision: the sparse gate checks directions 1–5 absent, not explicitly ACTION7 absent.

## Agreed facts

- Two genuine trained learning algorithms + two substantive evaluated improvements each are compulsory; negative outcomes are acceptable if motivated, tested and analysed.
- A bundled I1 can count as one intervention but cannot identify which bundled mechanism caused the outcome.
- Three policy seeds do not make exposed game families independent unseen games; disclosure is crucial.
- E126 frozen effect-CNN gating is source-supported, but separate from DQN/PPO and official Kaggle scoring.
- N118 effect prediction improvement did not improve native completion according to archived reports; E126 public development improvements are narrow.

## Fresh arithmetic check in this hearing

Read committed results/e126_per_game.csv and results/e126_all_arms.csv via connected GitHub, reaggregated in tool-executed JavaScript: 45 groups ×25 = **1125** recorded episodes, **125220** charged SDK actions; for E126 seeds 76/77/78, baseline mean SDK 2.093242/2.054775/2.096435 and trained hybrid 2.211518/2.223942/2.240737, with four net extra levels and six positive game–seed score changes confined to lf52 and s5i5. This verifies **saved table arithmetic only**, not native execution.

## Judicial evidence requests (ranked)

1. Complete original DQN/PPO six implementations and all 108 reported original episodes (72 core +12 random +24 PPO controls), including optimizer/target/log-prob/mask tests and source/config hashes. Determines CX-01/CX-03/CX-06/CX-10.
2. Genuine budget-indexed measured learning/adaptation performance series, with original data and scripts. Determines whether CX-04 can be repaired.
3. Authentic Kaggle official submission ID 57690887 receipt, successful score and time, source SHA, nominated class team; actual Moodle and Paper Track receipts. Resolves CX-09/external compliance.
4. Coursework DQN-I1 pretrained encoder provenance/training data/compute separate from E126 peer CNN. Narrows CX-06.
5. Authorized SDK and original owner-held trace/frame archives for N118/E126, replay/frame-hash parity. Improves CX-07/08/10 confidence but does not replace coursework evidence.

**Judicial position:** No fabricated score, broken PPO, or absent RL implementation has been established. Scientifically honest sparse/negative findings remain valid. Award no blanket full-compliance finding before original code and external receipts are verified; do not assume misconduct from missing public files.
