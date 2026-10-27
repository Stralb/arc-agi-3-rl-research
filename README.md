# ARC-AGI-3 — Interactive Reinforcement Learning Research

This repository preserves a **public, curated research snapshot** of agents for ARC-AGI-3 interactive games. It contains the frozen B1/N093 optimistic Bellman + PUCT control, the local action-effect extension, the E126 click-exploration candidate, verified historical development summaries and negative results. Results concern **25 previously exposed public games**, not unseen-game generalization or an official Kaggle score.

## Verify the published snapshot

**Python 3.11+**; these verification commands need only the Python standard library.

```bash
git clone https://github.com/Stralb/arc-agi-3-rl-research.git
cd arc-agi-3-rl-research
python3 scripts/verify_repository.py
python3 scripts/verify_e126_release.py
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
| Kaggle-format source notebooks (no new E126 submission) | [`notebooks/`](notebooks/README.md) |
| E126 model, generator, controls and public audit | [E126 protocol](experiments/E126/README.md), [findings](reports/E126_SUBMISSION_CANDIDATE.md) |
| Experimental implementations, ablations and protocols | [`experiments/`](experiments/INDEX.md) |
| Main findings and negative results | [`reports/RESEARCH_SUMMARY.md`](reports/RESEARCH_SUMMARY.md), [research index](reports/INDEX.md) |
| Public native benchmark tables and SVG figures | [`data/outputs/`](data/outputs/INDEX.md) |
| Source archive hashes and unpublished-asset inventory | [provenance](data/provenance/README.md), [coverage](docs/REPOSITORY_COVERAGE.md) |
| Exact offline/native reproduction boundary | [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) |
| Assignment deliverables and known gaps | [Submission checklist](docs/SUBMISSION_CHECKLIST.md) |

## Observed public-development results

| Frozen / candidate | Level 1 | Level 2 | Level 3+ | Total completed levels |
|---|---:|---:|---:|---:|
| Frozen B1 + N093 | 13 | 1 | 0 | **14** |
| Local effect-memory (N117, seed 76) | 13 | 2 | 0 | **15** |
| E126 hybrid (seeds 76/77/78) | 14 | 2 | 0 | **16 each seed** |

The N117 gain over N093 is one Level-2 completion on `tu93`. E126 additionally completes `s5i5` Level 1 on seeds 76/77/78; its 16 levels per seed are **public-development results selected after exposure to all 25 games**. Across those seeds, local SDK mean score increases from 2.081484 (matched N117 control) to 2.225399 (+0.143915), but a descriptive game-cluster interval includes zero. These are **not official Kaggle leaderboard scores**. Fewer charged actions can mean earlier `GAME_OVER`, not greater efficiency. All 25 game families influenced research; no independent unseen-game gain is demonstrated.

## Reproducing a native run

The public GitHub tree **does not contain the original game SDK, native frame/trace archives or private competition inputs**. To replay N114/N117, obtain the authorized original SDK archives, install the runtime dependencies in [`requirements-agent.txt`](requirements-agent.txt), and follow the checksum-verified [native staging commands](docs/REPRODUCIBILITY.md). The standard-library checks above validate committed files and arithmetic, **not** a fresh ARC game execution.

The **E126 candidate is now preserved in `main`** as research, alongside the unchanged N117 and N093 controls. The self-contained source and notebook are generated from a frozen pretrained effect checkpoint; the build is checked by committed SHA-256 manifests. It is **not submitted to Kaggle**, has not been verified in the official rerun, and is not an independently generalized agent. Teammate checkpoint redistribution rights must be confirmed before further release.

Build and check E126 offline (Python standard library; the SDK is not needed for packaging):

```bash
python3 experiments/E126/build_candidate.py
python3 scripts/verify_e126_release.py
```

**Submission status:** This repository is a curated research archive, **not the complete Moodle submission**. The final RLC-format report PDF, group contribution statement and externally verified Kaggle/Paper Track identifiers or evidence are not in this tree. The assignment's requirement for two qualifying learning algorithms and two separately evaluated improvements *per algorithm* is not established by these committed studies alone. See the [submission checklist](docs/SUBMISSION_CHECKLIST.md). See [data and licensing boundaries](docs/DATA_AND_LICENSES.md) before sharing additional assets.
