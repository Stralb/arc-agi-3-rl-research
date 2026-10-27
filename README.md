# ARC-AGI-3 — Interactive Reinforcement Learning Research

This repository preserves a **public, curated research snapshot** of agents for ARC-AGI-3 interactive games. It contains the frozen B1/N093 optimistic Bellman + PUCT control, an experimental local action-effect variant, native evaluation summaries and documented negative results. Results concern **25 previously exposed public games**, not unseen-game generalization or an official Kaggle score.

## Verify the published snapshot

**Python 3.11+**; these verification commands need only the Python standard library.

```bash
git clone https://github.com/Stralb/arc-agi-3-rl-research.git
cd arc-agi-3-rl-research
python3 scripts/verify_repository.py
python3 -m unittest discover -s tests -v
python3 scripts/summarize_results.py
```

To regenerate the public-result charts (requires a separate analysis environment):

```bash
python3 -m pip install -r requirements-analysis.txt
python3 scripts/generate_plots.py
```

## Where to look

| What | Location |
|---|---|
| Frozen reference agent and experimental local-effect agent | [`src/`](src/README.md) |
| Kaggle-format source notebooks (no verified submission from this repo) | [`notebooks/`](notebooks/README.md) |
| Experimental implementations, ablations and protocols | [`experiments/`](experiments/INDEX.md) |
| Main findings and negative results | [`reports/RESEARCH_SUMMARY.md`](reports/RESEARCH_SUMMARY.md), [research index](reports/INDEX.md) |
| Public native benchmark tables and SVG figures | [`data/outputs/`](data/outputs/INDEX.md) |
| Source archive hashes and unpublished-asset inventory | [provenance](data/provenance/README.md), [coverage](docs/REPOSITORY_COVERAGE.md) |
| Exact offline/native reproduction boundary | [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) |

## Observed public-development results

| Frozen / candidate | Level 1 | Level 2 | Level 3+ | Total completed levels |
|---|---:|---:|---:|---:|
| Frozen B1 + N093 | 13 | 1 | 0 | **14** |
| Local effect-memory | 13 | 2 | 0 | **15** |

The additional Level-2 completion was on `tu93`. These are archived native SDK results, **not official Kaggle leaderboard scores**. Fewer charged actions can mean earlier `GAME_OVER`, not greater efficiency. All 25 game families influenced research; no independent unseen-game gain is demonstrated.

## Reproducing a native run

The public GitHub tree **does not contain the original game SDK, native frame/trace archives or private competition inputs**. To replay N114/N117, obtain the authorized original SDK archives, install the runtime dependencies in [`requirements-agent.txt`](requirements-agent.txt), and follow the checksum-verified [native staging commands](docs/REPRODUCIBILITY.md). The standard-library checks above validate committed files and arithmetic, **not** a fresh ARC game execution.

The later **E126 research candidate** is retained on a [separate development branch](https://github.com/Stralb/arc-agi-3-rl-research/tree/feat/e126-kaggle-release-20261027); it is not part of this frozen `main` snapshot and has not been verified on Kaggle's official rerun.

**Submission status:** This GitHub repository is a research archive, **not the complete Moodle submission**. The assignment's final report PDF, team contribution statement, and Kaggle/Paper Track submission identifiers or evidence are not present here. See [data and licensing boundaries](docs/DATA_AND_LICENSES.md) before sharing additional assets.
