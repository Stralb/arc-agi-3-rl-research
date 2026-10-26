# N118 Native Research Findings — Action History Versus Action Effect

26 October 2026 — Completed offline research. **No deployment promotion.**

## Tested hypothesis

The previous action-effect model captured static frame/action features but ignored the immediately previous native action and its visual result. Because ARC-AGI-3 games may encode sequential control dependencies, the first two observed action/effect pairs could improve online effect predictions and hence action selection. This hypothesis does **not** assume that visual changes are always meaningful or that hidden dynamics can be reconstructed from screenshots.

## Architecture and source provenance

The original frozen N093 B1 + pretrained prior is preserved byte-for-byte (`inputs/submission.py` SHA-256 `e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d`; `inputs/submission.ipynb` SHA-256 `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`). The *research-only* comparison inherits the previously verified local-effect selector from N117; therefore, the no-history arm has **complete 25/25 physical-trajectory parity** with archived N117 `soft_plus_local`. All 75 N118 Level-1 action sequences are exact matches, so Level 2+ variation is attributable to selection, not different Level 1 experience.

A regularized online 45-feature logistic predictor is trained only after observing native charged action outcomes. Base 27 features encode current frame and proposed action. The extra 18 features encode the previous control type, previous and two-back visible effect buckets (0, 1–3, >=4 pixels), repeat status/length and action switching. Every level transition clears this short history, while model weights retain Level-1 experience. No game-ID policies, source-derived mechanics, hidden or future SDK frames, shadow SDK transitions, fake terminal rewards, LLM, VLM, or hard action masks are used by the actor.

Three matched policy arms use the same initial frozen checkpoint, optimizer, features dimension, Q-updates, legal actions, selection coefficient and sampling seed:

1. `temporal_nohistory`: History feature coordinates are all zero; validated byte-identical to previous `soft_plus_local` action paths.
2. `temporal_history`: Actual previous one/two native action outcomes supplied before selection.
3. `temporal_corrupt`: Extra features are functions of the *current candidate only* and omit real history, a placebo feature-ablation control (not merely a reversible permutation).

The predictor learns the >=4-pixel label; its output adds a modest finite **selection bonus** only. Native level progression is the only Bellman reward. Every native SDK action costs one action; cap 200 **per level**, with actual `GAME_OVER` earlier where applicable.

## Results: complete 25-game native matched evaluation

| Controller | L1 | L2 | L3+ | Total completed levels | Charged SDK actions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Immutable N093 reference (N114) | 13 | 1 | 0 | 14 | 2,982 |
| Previous N117 local+effect | 13 | 2 | 0 | 15 | 2,706 |
| N118 no-history ablation | 13 | 2 | 0 | 15 | 2,706 |
| N118 actual history | 13 | 2 | 0 | 15 | 2,703 |
| N118 corrupted-history placebo | 13 | 2 | 0 | 15 | 2,759 |

Only `vc33` and `tu93` complete Level 2 in the N118 runs. There are **zero new Level-2 completions** and **zero native Level-3 completions**. A smaller overall SDK-action total cannot establish better efficiency because episodes often terminate earlier. In particular, `tu93` reaches native `GAME_OVER` after **15 Level-3 actions** in the temporal-history branch, compared with **27** for the no-history branch. `vc33` still terminates at 75 Level-3 actions in both.

History changes physical trajectories in **11 of 25 games**. It produces **191 visually silent Level-2+ actions**, compared with **146** for no-history, and **406** <=3-pixel actions compared with 350. These are retrospective correlates of exploration behavior, not direct failure labels.

## Prediction-only audit with identical native actions

To avoid the selection-confounding problem, all three predictors were independently trained/evaluated **prequentially** on the same 25 previously frozen N117 action trajectories. Each action was replayed through the real SDK. For each action, models predicted *before* receiving its observed frame and updated only afterward. Reward and terminal transitions were not used to train the visual-effect target.

| Level-2+ measure (1,197 nonterminal nonreward decisions) | No history | Actual history | Corrupted history |
| --- | ---: | ---: | ---: |
| Brier error | 0.169102 | **0.151572** | 0.162504 |
| Log loss | 0.503864 | **0.457355** | 0.484127 |
| False-negative rate for >=4 pixels at p<0.5 | **5.29%** | 12.22% | 10.46% |

History can improve probability calibration and aggregate predictive error while worsening sensitivity under a particular threshold. In Level 3, only 100 charged nonterminal action examples occur in this frozen archive. Actual-history Brier 0.242059 versus no-history 0.252793, but Level-3 false-negative rate rises from 42.55% to 51.06%. The fixed-trajectory audit is observational with no counterfactual candidate-action labels.

Prequential error is calculated *per transition*, so apparently large sample counts should not be mistaken for independent games. In the 13 exposed families reaching Level 2, history reduces within-family Brier versus no-history in 12/13. This is evidence of a useful predictive signal, **not** evidence of an RL control improvement or hidden-game generalization.

## Reproducibility and robustness

- Native actor: 25 families x 3 fixed arms = **75 episodes**, **8,168 charged SDK actions**.
- Independent replay: **75/75 episodes, 8,168/8,168 actions**, exact action legality, pre/post frame SHA-256, changed-pixel count, native reward events, and final state.
- Policy-seed sensitivity: 3 arms x 2 Level-3-reaching games x two additional policy seeds = **12 more native episodes**, **1,019 more actions**, all independently replayed. Repeated seeds kept the same underlying layouts.
- Initial native frame SHA-256 across native seeds 47, 48, 49, 50 is identical for both `vc33` and `tu93`.
- Code-level history/nohistory/corrupted-history tests, including no-future information, no hard mask, strict reward labeling, and frozen source hashing.
- Generated standalone experimental notebook/source: **4/4** acting-time parity games (`vc33`, `tu93`, `ar25`, `lp85`) with native action, observation hash, and reward equality to modular N118.
- The published full frozen N093 N114 25-game matrix is retained for reference, and the earlier N117 complete trajectory archive is copied to the release for independent playback and parity without another connected service.

## Limitations and decision

**Do not promote N118 to Kaggle.** It has not improved the level-completion objective. The classifier's predictor improvement is a real measured result on historically exposed public SDK trajectories; it is not a task-progress predictor. No official RHAE can be computed because human-reference action efficiency values are unavailable here. Native seeds do not produce new configurations. More policy-seed replicas on identical layouts would not address that evidence gap.

Retain both research-only experimental approaches (previous 15-level local-effect candidate and current temporal actor) for external independent-layout validation, but the immutable N093 notebook remains the recommended competition fallback under the defined promotion standard.

The next high-value question is not another binary screen-change classifier: evaluate **delayed outcomes that predict native survival and eventual level advancement**, using prospective family-disjoint validation. Do not treat `GAME_OVER` timing or raw visual novelty as a solved subgoal; develop controls that separate irreversible failures, animations and consequential state transitions. Without independent variation in game layouts, refrain from asserting generalization.
