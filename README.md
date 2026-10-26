# ARC-AGI-3 — Reinforcement Learning Agents and Experimental Evidence

**Repository:** `Stralb/arc-agi-3-rl-research` · **Status:** Public, own code and derived results only; official SDK and original game assets excluded.

**PUBLISHING STATUS (2026-10-26): PARTIAL.** The research documentation, selected source modules, measured CSVs, and source-derived SVG figure are committed. The 1.6 MB standalone primary agent, notebooks, and several archives have **not** yet been uploaded because the connected GitHub content-write tool blocked large-file transfers. Do not assume the default `src/best_public_agent.py` path is available in this remote repository. The local release bundle remains authoritative until this gap is resolved.

This repository organizes a multi-experiment, Kaggle-legal ARC-AGI-3 interactive-agent research project. It contains reproducible Python agent sources, the frozen and experimental Kaggle notebooks, reports, per-family and per-action result files, failure studies and generated plots. The evaluations use **25 historically exposed public interactive game fixtures** and the **native SDK action interface**, not ARC-AGI-1's 400+400 static grid tasks.

## Most important result

| Agent | Level 1 | Level 2 | Level 3+ | Total public levels | Status |
|---|---:|---:|---:|---:|---|
| **Best measured public: local effect-memory** (`src/best_public_agent.py`) | 13 | **2** | 0 | **15** | Research candidate; not independently generalized |
| **Frozen B1 + N093 pretrained PUCT** (`src/baselines/frozen_n093.py`) | 13 | 1 | 0 | 14 | Immutable, conservative fallback |

The new local-effect Level-2 winner is `tu93`; both agents clear `vc33` Level 2. No tested method completed Level 3. **Neither score is an official Kaggle leaderboard score or human-normalized RHAE.** Lower total action counts can reflect earlier native `GAME_OVER`, not efficiency improvements.

## Structure

```text
src/                  Best public measured agent, frozen baseline, algorithm module
notebooks/            Original frozen and local-effect Kaggle-format submissions
experiments/          N093 and N101–N120 experimental Python, protocols and tests
reports/              Research synthesis, archived original reports and full findings
data/outputs/         Native result matrices, per-action traces, model diagnostics
data/outputs/plots/   Regenerable figures (PNG and SVG)
data/provenance/      File-level source/hashes and original asset manifest
scripts/              Plot regeneration, integrity verification, data expansion
tests/                Repository integrity and benchmark-consistency checks
.github/workflows/    Offline CI that never submits or downloads competition games
```

## Quick start

```bash
# After extracting the repo ZIP or cloning your future GitHub repo:
cd arc-agi-3-rl-research
python3 scripts/verify_artifacts.py
python3 -m unittest discover -s tests -v
python3 -m pip install -r requirements-analysis.txt
python3 scripts/generate_plots.py
```

The first two checks use only the Python standard library. Plot regeneration requires pandas, NumPy and Matplotlib. Native gameplay requires the separately obtained official game SDK and Agents framework; see [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Read the results

- [`reports/RESEARCH_SUMMARY.md`](reports/RESEARCH_SUMMARY.md): scientific conclusions, exact baseline comparison and risks.
- [`reports/EXPERIMENT_CATALOG.md`](reports/EXPERIMENT_CATALOG.md): prior experiments and verified negative controls.
- [`data/outputs/benchmarks/n117_local_vs_frozen_25.csv`](data/outputs/benchmarks/n117_local_vs_frozen_25.csv): complete per-family comparison.
- [`data/outputs/plots/`](data/outputs/plots/): plots of native completions, progression, budget, and predictive tradeoffs.
- [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md): code, inputs, provenance and actions counted.
- [`docs/DATA_AND_LICENSES.md`](docs/DATA_AND_LICENSES.md): competition data and third-party license restrictions.

## Reproducibility and scientific claims

All published counts in this snapshot refer to **archived native local runs**, not fresh runs during GitHub packaging. Original source and data hashes are logged under `data/provenance/`. Results are from exposed development/public fixtures; model-selection on those fixtures prevents claims of independent generalization.

The Kaggle deployment and leaderboard status is unknown. Neither notebook has been submitted from this repository. The frozen N093 checkpoint is embedded in both source files.

**Research snapshot:** 2026-10-26.