# SIX-PERSPECTIVE ADVERSARIAL TRIBUNAL — 2026-10-27

**Status:** Completed simulation by **one model** applying six distinct standards; not six independent human or model reviews. **No scientific files edited.** Primary manuscript: user-uploaded `ARC_AGI3_E128_Revised_Research_Paper (1).pdf` (8 main pages, 2 references). Required named E127 paper not separately available. Lecturer: uploaded `RL_Assignment(1).pdf` pp1–5. Repository: `Stralb/arc-agi-3-rl-research`, audit source `main@49b966d06afe8ee2a51da100801bf7d5ae63eebf`, archived research branch `archive/full-research-2026-10-27`.

The reviews were formulated **separately before synthesis** and deliberately disagree about severity and what can currently be inferred. All evidence labels follow EVIDENCE_LEDGER.md.

## 1. Strict coursework lecturer
**Five issues (ordered):** (L1) **Critical/UNVERIFIED:** actual trained DQN/PPO source/checkpoints and 72 native episodes absent from indexed GitHub snapshot although E128 §3–4 reports them; threatens 20 baseline marks and 25 improvement marks. (L2) **High/VERIFIED omission:** true learning or adaptation curve requested by lecturer §5, explicitly not supplied by Figure 2/E128 p5; threatens 25 rigour marks. (L3) **High/UNVERIFIED:** DQN-I2 may be epsilon schedule rather than substantive method, E128 p3 (threshold 96, epsilon 0.75); threatens improvement 25. (L4) **High/UNVERIFIED:** random 12 and PPO controls 24 original logs unavailable; affects baselines/rigour. (L5) **Critical/MISSING or UNRESOLVED:** contributions, Paper Track/Moodle receipts and Kaggle submission confirmation, E128 pp7–8, repo manifest.
**Strengths:** six named stages and a random reference appear in E128; unsuccessful results explicitly reported and discussed; correct distinction of coursework vs E126.
**Further verification:** actual optimizer call sites, seed budgets, raw logs, server receipts, actual roster.
**Exact corrections:** recover 6-arm complete source/trace manifest; check I2 implementation; recover true curves or accurately disclose gap; complete real contribution and submission evidence.
**Verdict:** overall provisionally adequate but incomplete implementation proof; not yet supportable as full-credit coursework.

## 2. Senior RL researcher
**Five issues:** (RL1) **Critical/UNVERIFIED:** DQN Eq(1) target mask/done/target-network implementation, though written equation is correct. (RL2) **Critical/UNVERIFIED:** PPO factorised conditional click log-probs and rollout/update mask equivalence for clipped ratio (E128 Eq2, §3.2). (RL3) **High/SUPPORTED BUT LIMITED:** DQN-I1 changes candidate scorer+D14+frozen effect encoder together, confounding attribution; E128 acknowledges bundle. (RL4) **High/BORDERLINE:** DQN-I2 raising epsilon to .75 after 96 zero-reward actions could be conditional tuning; code needed. (RL5) **Medium/SUPPORTED:** PPO-I1 Eq3 encourages observable novelty; 20.49 reported intrinsic bonus without win is not proof curiosity intrinsically fails.
**Strengths:** native reward vs shaped reward vs visual-effect target correctly separate; `src/frozen_n093.py` source confirms empirical Q backups, frozen prior and one-step PUCT, not PPO/DQN ensemble.
**Further verification:** actual target terminal semantics, GAE, gradients, mask support, optimizer freeze/old log-prob, I2 trigger.
**Exact corrections:** run source-level mathematical invariants; isolate bundles only when ablations exist; classify I2 conditionally; maintain E126 lineage separation.
**Verdict:** math described plausibly; no claim of actual code correctness until original source audited.

## 3. Statistician / causal-inference specialist
**Five issues:** (ST1) **High/SUPPORTED:** 72 nominal coursework episodes are four development-exposed families x 3 seeds, with only 3 distinct positive game-seed cells (E128 Table 1, Fig2). (ST2) **High/VERIFIED design:** E126 75 runs are 25 historically exposed public families x 3 policy seeds, not 75 independent hidden games. (ST3) **High/VERIFIED arithmetic:** only s5i5 and lf52 improve SDK score; s5i5 is 68.54% of E126 gain (`results/e126_per_game.csv`). (ST4) **High/SUPPORTED:** PPO mask-only also wins one reported case; E124 rarity/effect controls reproduce lf52 effect, so no unique mechanistic attribution. (ST5) **High/SUPPORTED:** E126 28/75 changed choices vs just 6/75 score-positive; first visible-frame hash does not certify full POMDP identity.
**Strengths:** manuscript admits prior exposure, interval including zero and action changes not equal native progress; E126 arithmetic supports narrow descriptive gains.
**Further verification:** bootstrap unit/replicates, censoring, prespecification/selection, frame traces and actual comparison results.
**Exact corrections:** family-level units; descriptive confidence language; leave-one-positive-family diagnostics; do not infer hidden-game effect.
**Verdict:** descriptive results are useful but broad generalisation/causal claims not identified.

## 4. Software / reproducibility engineer
**Five issues:** (EN1) **Critical/UNVERIFIED:** original six-arm course scripts/configs/checkpoints/logs not identified in connected repository indexes. (EN2) **High/UNVERIFIED:** reported 360/361 DQN and 768 PPO updates need actual optimizer calls and parameter-difference checks. (EN3) **High/SUPPORTED:** `scripts/verify_repository.py` and `scripts/verify_e126_release.py` check hashes/CSV arithmetic, not native SDK execution. (EN4) **Critical/CONTRADICTED pending chronology:** earlier manifest `official_kaggle_submission=false`, E128 p7 says E126 Kaggle 57690887=0.33; a later real submission is possible and must be checked. (EN5) **Medium-high/SUPPORTED:** loose `requirements.txt`, owner-held SDK/trace archives and pretrained compute not included in Table1.
**Strengths:** N114/N117 runner source checks legal actions and native progression; deterministic E126 source/notebook/checkpoint hashes and 1125-row CSV evidence are committed.
**Further verification:** original archive and Kaggle receipt, test execution, environment hashes, reset/terminal branches.
**Exact corrections:** per-run provenance manifest, optimizer invariant tests, version-pinned replay environment, source-hash-to-submission check.
**Verdict:** E126 auditable offline to a bounded extent; coursework raw implementation not yet independently auditable.

## 5. Integrity / competition auditor
**Five issues:** (IN1) **Critical/UNRESOLVED:** official Kaggle E126 record conflicts with older repo status; no misconduct conclusion without chronological platform check. (IN2) **High/VERIFIED omission:** E128 p8 says author contributions to be confirmed. (IN3) **High/UNVERIFIED:** peer effect checkpoint reuse/share permission; `docs/DATA_AND_LICENSES.md`. (IN4) **Critical/MISSING:** Paper Track, nominated class team, matching Moodle ZIP and platform receipts. (IN5) **High/SUPPORTED limitation:** 25 public families have been used for development, so no new-test claim.
**Strengths:** external model attribution, self-disclosed exposure and checksum provenance, local vs Kaggle metric separation.
**Further verification:** platform IDs/timestamps, ownership, exact collaboration and AI-use declaration subject to Wits policy.
**Exact corrections:** independent receipts/source checks, signed-off contributions, license/permission review, truthful platform-specific status.
**Verdict:** serious documentation gaps but **no evidence here establishes misconduct**.

## 6. Top-tier scientific editor
**Five issues:** (ED1) **High:** four required coursework improvements get less exposition than N118–E126 (E128 pp3–5 vs pp5–8). (ED2) **High:** 4-family/256-action DQN/PPO protocol cannot be numerically pooled with 25-family/N117→E126; E128 acknowledges difference. (ED3) **High:** bundled DQN I1 limits mechanism isolation. (ED4) **High:** Figure2 depicts event timing, not proper learning curve, consuming tight page budget. (ED5) **Medium:** Figures2/4 dense at eight-page limit; figure/LaTeX sources not yet matched.
**Strengths:** strong title/thesis separating visual effect, selected action and native reward; includes negative cases, source boundaries and no generalisation claim.
**Further verification:** original coursework diagnostics sufficient for a stronger core; exact figure regeneration and RLC source.
**Exact corrections:** keep course comparison central, E126 as separately qualified case study, preserve negative evidence and precise metric labels; edit only after proof.
**Verdict:** coherent research narrative but unbalanced toward independently better evidenced E126 study.

## Synthesis and preserved disagreements

| Issue | Reviewers | Evidence | Severity | Disagreement | Verification needed |
|---|---|---|---|---|---|
| Coursework DQN/PPO source and 72-run provenance | Lecturer, RL, engineer, editor | E128 §§3–4 Table1 vs no matching indexed main/archive code | Critical | Lecturer discounts assessment; engineer does not infer experiments absent; editor focuses balance | Original cluster ZIP/source/logs/checkpoints |
| Genuine substantive DQN-I2 | Lecturer, RL, editor | epsilon>=.75 after 96 non-reward actions E128 p3 | High | RL: borderline/tuning; lecturer: at-risk rubric; editor: narrative evidence thin | code plus trigger/control ablations |
| PPO masked ratio correctness | RL, engineer | factorised probability Eq2, mask §3.2; no original PPO source | Critical verification gap | No evidence of error; cannot declare correct | rollout/update old/new log prob and mask tests |
| Learning/adaptation curves | Lecturer, editor, statistician | assignment p3; E128 p5 admits absent checkpoint series | High | Lecturer: mandatory missing; editor: fix space allocation; statistician warns against false proxies | checkpoint metrics or honest omission |
| Dataset independence/uncertainty | Statistician, RL, editor | 4x3 core + 25x3 E126, 3 unique core positives | High | Not a method violation by itself; invalid if called new-game success | pretraining exposure, seed/layout metadata |
| E126 local effect vs causal mechanism | Statistician, RL, editor | 28 changes, 6 score gains, 4 levels, 2 games, E124 controls | High | RL supports narrower decision-level mechanism; statistician disallows broader causal attribution | original traces, alternate gates on new families |
| E126 official Kaggle score | Lecturer, engineer, integrity | E128 ID 57690887=0.33; archived release says unsubmitted | Critical provenance | Integrity: no misconduct inference; engineer: possible chronological update | server receipt timestamp and exact artifact SHA |
| E126 verification depth | Engineer, statistician | 1125-row CSV, offline verifier, owner-held trace archive | High | Arithmetic verified; native engine replay still limited | original SDK and trace replay |
| Peer model rights and training cost | Integrity, RL, engineer | frozen peer CNN, `docs/DATA_AND_LICENSES.md`, excluded Table1 pretraining | High | Licensing and compute comparability are distinct issues | training/permissions/source assets |
| Missing contributions/Paper Track/Moodle | Lecturer, integrity | E128 p8 and repo checklist | Critical compliance | Documentation gap not misconduct | signed roles, track receipts, Moodle ZIP |
| Figure density and thesis focus | Editor, lecturer | E128 Figs 1–4, eight-page body | Medium-high | Editor sees important framing; lecturer prioritizes rubric evidence | final source/figures and grading adequacy |

### Board decisions
- **VERIFIED directly from committed source:** N093 empirical Bellman backups (not neural DQN gradient), one-step PUCT; N117 effect-memory extensions; E126 pretrained CNN frozen and gated on sparse L1 click scenes. E126 CSV arithmetic includes 1125 episodes and 125220 actions, 28 changed game-seed trajectories for the trained hybrid, six positive score pairs, four extra levels, and no new Level 3 completions. Arithmetic verification is not native replay.
- **SUPPORTED BUT LIMITED:** E126 control mechanisms and reported historical full replay; N118 Brier/FNR discrepancy; real public development gains.
- **UNVERIFIED:** actual DQN/PPO six-arm source, gradient correctness, PPO mask ratio, DQN-I2 exact mechanism, random/PPO control raw runs and resource provenance; official Kaggle server receipt.
- **MISSING:** proper checkpoint learning/adaptation curve in E128; confirmed author contributions; confirmed Paper Track and Moodle artifacts.
- **CONTRADICTED/UNRESOLVED:** E126 earlier repository 'unsubmitted' status vs later manuscript's official submission ID. Verify chronology before correction.

### Prioritized verification, *not a rewrite*
P0: find original coursework source+72/36 episodes and implementer logs; check PPO ratio; inspect DQN-I2 actual branch; confirm Kaggle receipt and course deliverables.
P1: recover true adaptation/checkpoint metrics, trace-level E126 replay, checkpoint license/cost, figure source.
P2: only then rebalance wording and figure emphasis while protecting negative results.
