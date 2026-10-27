# Experiments and results

We tested whether an agent can explore unfamiliar ARC-AGI-3 games more effectively by remembering the effects of its actions. This page presents the comparisons relevant to the current agents. The [research archive](https://github.com/Stralb/arc-agi-3-rl-research/tree/archive/full-research-2026-10-27) contains the rest of the experiments, including approaches that did not work.

## Environment and baselines

The native game interface supplies a 64×64 observation, a legal action menu and level progression. We use actual increases in the SDK's completed-level count as reward; visual changes alone do not count as success. The agents have a 200-action policy cap per level, although games can end earlier. The historical tests cover 25 public game families: 15 originally used for training, five for validation and five originally held out but subsequently exposed during development.

N093 uses optimistic Bellman/Q-value updates with a PUCT-style **one-step action ranking**, not full Monte Carlo tree search. N117 retains that controller but adjusts choices using observed local action effects. E126 adds click-frequency feedback and an offline-trained model that predicts effects on sparse click-only screens. That predictor is not a separate reinforcement-learning algorithm.

| Version | L1 | L2 | L3+ | Total | Native actions, original comparison |
|---|---:|---:|---:|---:|---:|
| N093 frozen | 13 | 1 | 0 | 14 | 2,982 |
| N117 local-effect | 13 | 2 | 0 | 15 | 2,790 |

The extra N117 Level-2 completion occurs on `tu93`. Both complete Level 2 on `vc33`. Lower action totals do **not** necessarily mean greater efficiency: an agent can finish earlier because the game terminates. See [N093 per-game outcomes](results/n093_public25.csv) and [paired N093/N117 outcomes](results/n117_public25.csv).

![Completed native levels for N093 and N117](results/plots/level_completions.svg)

## Which changes helped?

The [N117 ablation table](results/n117_ablations.csv) compares local-effect memory with cross-level transfer, curiosity, novelty, random novelty and skill variants on a 13-game subset. Local effect memory and pixel novelty reach two Level-2 completions. Counting every pixel change or shuffling the local evidence removes the additional `tu93` completion. This supports an action-effect preference being useful in one exposed environment, but does not prove a unique mechanism.

For E126 we compared observation-conditioned click feedback, random model weights, salience-based controls and a trained effect model. Each arm has [per-game records](results/e126_per_game.csv), with [arm totals](results/e126_all_arms.csv) and [paired changes](results/e126_paired_changes.csv).

| Policy seed | N117 levels | E126 levels | N117 local SDK mean | E126 local SDK mean |
|---|---:|---:|---:|---:|
| 76 | 15 | 16 | 2.093242 | 2.211518 |
| 77 | 14 | 16 | 2.054775 | 2.223942 |
| 78 | 15 | 16 | 2.096435 | 2.240737 |

The E126 agent newly completes `s5i5` Level 1 on each tested seed. For seed 77, click feedback also recovers `lf52`. The mean local SDK score over these seeds rises from **2.081484 to 2.225399**; this is a local development metric, **not an official Kaggle score**. Four additional policy/native seed pairings showed level differences of +1, 0, 0 and +1 ([records](results/e126_robustness.csv)). Their native starting frames were identical to the original seed's frames.

## What did not work

Earlier object parsers, planned action sequences, learned frame predictors, temporal models, joint actions and episodic value models did not establish a new Level-3 completion. Some improved intermediate predictions without improving game reward. The full implementation history, negative controls and original diagnostic results remain in the archive rather than being repeated in this submission-facing tree.

![N093 versus N117 level completion by game](results/plots/family_completion_matrix.svg)

## What these numbers do and do not establish

All 25 public games were repeatedly exposed during development. The E126 sparse-scene threshold was selected using those games, and a game-cluster uncertainty interval for its improvement includes zero. Repeating a policy seed with the same starting frames does not provide independent environment variation. We also have no independently verified hidden Kaggle result for E126 and no completed Level 3.

The training and acting code uses only permitted observations and legal actions as documented by the saved studies. The source archive contains the original seed protocol, raw hashes and native replay checks. Those archives and official SDK files are **not available in this curated main branch**. The scripts here validate the saved data and release files; they do not replay the original games.

Finally, the current experimental record mainly concerns a Q/Bellman-based family of agents. Although the original assignment requires a second distinct learning algorithm and two substantive tested changes for each, the experiments shown here should **not** be presented as if they fulfil that whole requirement.
