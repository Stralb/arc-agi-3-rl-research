# Learning to explore ARC-AGI-3 games

This is our reinforcement learning research project for ARC-AGI-3. The benchmark has interactive games rather than puzzles with a known target grid. The agent sees a 64×64 frame, chooses a legal action, and has to work out which actions are useful. We experimented with ways to improve exploration when rewards are sparse and the rules are unknown.

The code below is the part of the project we would actually want someone marking our work to read. Older trials, failed ideas, detailed traces, and the original research notes are preserved in the [full research archive](https://github.com/Stralb/arc-agi-3-rl-research/tree/archive/full-research-2026-10-27).

## How our agents work

We developed three versions of a Bellman/Q-based agent. The **N093** baseline uses optimistic Q updates and a PUCT-style one-step action score (not a full search tree). **N117** keeps that controller but learns which actions have local visual effects and uses that information when choosing again. **E126** adds click feedback and a pretrained action-effect model on sparse click-only screens. The pretrained network predicts effects; it is not a second RL algorithm.

## Results on public games

The native SDK supplies the observation and legal actions. We reward actual increases in completed levels, not arbitrary pixel changes. We evaluated 25 publicly exposed game families with a policy limit of 200 actions per level, although the game can end sooner.



## What the experiments showed

The [N117 ablation table](results/n117_ablations.csv) compares local-effect memory with cross-level transfer, curiosity, novelty, random novelty and skill variants on a 13-game subset. Local effect memory and pixel novelty reach two Level-2 completions. Counting every pixel change or shuffling the local evidence removes the additional `tu93` completion. This supports an action-effect preference being useful in one exposed environment, but does not prove a unique mechanism.

For E126, we compared click feedback with a trained effect predictor, random weights and visual-salience controls. The complete [arm totals](results/e126_all_arms.csv), [per-game observations](results/e126_per_game.csv) and [paired changes](results/e126_paired_changes.csv) are available as CSVs.

| Policy seed | N117 levels | E126 levels | N117 local SDK mean | E126 local SDK mean |
|---|---:|---:|---:|---:|
| 76 | 15 | 16 | 2.093242 | 2.211518 |
| 77 | 14 | 16 | 2.054775 | 2.223942 |
| 78 | 15 | 16 | 2.096435 | 2.240737 |

The E126 agent newly completes `s5i5` Level 1 on each tested seed. For seed 77, click feedback also recovers `lf52`. The mean local SDK score over these seeds rises from **2.081484 to 2.225399**; this is a local development metric, **not an official Kaggle score**. Four additional policy/native seed pairings showed level differences of +1, 0, 0 and +1 ([records](results/e126_robustness.csv)). Their native starting frames were identical to the original seed's frames.

Earlier trials using object parsers, planned action sequences, joint actions, frame predictors, temporal models and episodic value estimates did **not** establish any new Level-3 completion. We kept the detailed failed experiments, original protocols, older notebooks and diagnostic evidence on the [archive branch](https://github.com/Stralb/arc-agi-3-rl-research/tree/archive/full-research-2026-10-27), rather than spreading them across `main`.

## Finding your way around

| Location | Contents |
|---|---|
| [src/](src/) | N093, N117 and E126 agent sources, including the readable local-effect policy |
| [E126_Kaggle_Candidate.ipynb](E126_Kaggle_Candidate.ipynb) | E126 Kaggle-format candidate notebook |
| [release/](release/) | Notebook builder, extension, checkpoint and checksums |
| [results/](results/) | Saved per-game results, ablations and figures |

The generated agents are large because they embed model parameters for offline use. We have left their exact bytes alone to avoid breaking release hashes. The earlier Kaggle-format notebooks, additional training code and historical evaluations are available on the archive branch, not deleted.

## What you can run

From the repository root with Python 3.11+:

```bash
python3 scripts/verify_repository.py
python3 release/build_candidate.py
python3 scripts/verify_e126_release.py
python3 -m unittest test_repository -v
python3 scripts/summarize_results.py
```

These commands check the committed evidence and rebuild the E126 notebook **without running any games or requiring the SDK**. For optional charts:

```bash
python3 -m pip install -r requirements-analysis.txt
python3 scripts/generate_plots.py
```

The actual ARC-AGI-3 SDK and original native replay files are not redistributed here. The original N114/N117 runner instructions and source are in the [archived repository](https://github.com/Stralb/arc-agi-3-rl-research/blob/archive/full-research-2026-10-27/docs/REPRODUCIBILITY.md). They require separately authorised game assets. A passing offline test is **not** a fresh gameplay result or a Kaggle rerun.

## Limitations

All 25 public games were seen during development, so these numbers do not show independent generalisation. The E126 screen threshold was also chosen using those games; a descriptive game-cluster uncertainty interval includes zero. Some different policy seeds produce identical starting frames. We have no independently verified E126 Kaggle rerun and no Level-3 completion.

The original SDK/game traces are not published in this curated repository. The scripts above check committed source hashes and saved results; they do not replay the games. The actual native runners and instructions are preserved in the archive. The large generated agent files contain embedded model weights, so their bytes remain unchanged.

## Work still to be submitted

The final RLC-format assignment report, the second qualifying RL algorithm's evaluation, group contributions, and verifiable Kaggle/Paper Track submission evidence are not included in this branch. We have not labelled those as complete. We also need to check redistribution permission for the teammate-trained effect-model checkpoint before any wider release.
