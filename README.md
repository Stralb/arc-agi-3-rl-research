# Learning to explore ARC-AGI-3 games

This is our reinforcement learning research project for ARC-AGI-3. The benchmark has interactive games rather than puzzles with a known target grid. The agent sees a 64×64 frame, chooses a legal action, and has to work out which actions are useful. We experimented with ways to improve exploration when rewards are sparse and the rules are unknown.

The code below is the part of the project we would actually want someone marking our work to read. Older trials, failed ideas, detailed traces, and the original research notes are preserved in the [full research archive](https://github.com/Stralb/arc-agi-3-rl-research/tree/archive/full-research-2026-10-27).

## Agents we compared

| Version | What changed | Completed levels on 25 public games |
|---|---|---:|
| N093 | Optimistic Bellman/Q updates and a PUCT-style action selector | 14 |
| N117 | Adds local action-effect memory to the same controller | 15 |
| E126 | Adds click feedback and a pretrained action-effect model in selected scenes | 16 |

These are **historical local SDK results**, not Kaggle leaderboard scores. E126 reached 16 levels with each of three tested policy seeds; N117's matched results were 15, 14 and 15. All 25 games were used during development, so we cannot treat these as independent evidence of generalisation. No agent completed Level 3. The E126 notebook is a **research candidate, not a verified Kaggle submission**.

The action-effect network is an auxiliary predictor, **not a second independent RL algorithm**. The assignment also asks for another learning algorithm and two tested improvements per algorithm; this repository does not yet establish that requirement.

## Finding your way around

| Location | Contents |
|---|---|
| [src/](src/) | Frozen N093 and N117 sources, readable local-effect policy, and the generated E126 agent |
| [notebooks/](notebooks/) | One E126 Kaggle-format candidate notebook |
| [release/e126/](release/e126/) | Notebook builder, action-effect extension and release checksums |
| [assets/e126/](assets/e126/) | Pretrained effect-model checkpoint |
| [RESULTS.md](RESULTS.md) | Comparison, ablations, failures, evaluation limitations |
| [results/](results/) | Per-game CSVs and a few figures used in the comparison |

The generated agents are large because they embed model parameters for offline use. We have left their exact bytes alone to avoid breaking release hashes. The earlier Kaggle-format notebooks, additional training code and historical evaluations are available on the archive branch, not deleted.

## What you can run

From the repository root with Python 3.11+:

```bash
python3 scripts/verify_repository.py
python3 release/e126/build_candidate.py
python3 scripts/verify_e126_release.py
python3 -m unittest discover -s tests -v
python3 scripts/summarize_results.py
```

These commands check the committed evidence and rebuild the E126 notebook **without running any games or requiring the SDK**. For optional charts:

```bash
python3 -m pip install -r requirements-analysis.txt
python3 scripts/generate_plots.py
```

The actual ARC-AGI-3 SDK and original native replay files are not redistributed here. The original N114/N117 runner instructions and source are in the [archived repository](https://github.com/Stralb/arc-agi-3-rl-research/blob/archive/full-research-2026-10-27/docs/REPRODUCIBILITY.md). They require separately authorised game assets. A passing offline test is **not** a fresh gameplay result or a Kaggle rerun.

## Work still to be submitted

The final RLC-format assignment report, the second qualifying RL algorithm's evaluation, group contributions, and verifiable Kaggle/Paper Track submission evidence are not included in this branch. We have not labelled those as complete. We also need to check redistribution permission for the teammate-trained effect-model checkpoint before any wider release.
