# Reproduction and audit

## Standard-library checks (no SDK needed)

```bash
cd arc-agi-3-rl-research
python3 scripts/verify_artifacts.py
python3 -m unittest discover -s tests -v
```

These independently verify notebook/source immutability, the benchmark count arithmetic and the stored repository hash manifest. They **do not replay native actions**.

## Regenerate figures

```bash
python3 -m pip install -r requirements-analysis.txt
python3 scripts/generate_plots.py
```

## Uncompress the full recorded experiment outputs

```bash
python3 scripts/materialize_outputs.py --experiment N120 --destination /tmp/arc_n120_outputs
```

The decompressed directory contains the original result relative paths. The SHA-256 origin manifest records their source archive and original bytes.

## Reproduce native public-game evaluation

The **offline SDK runtime and public game fixtures are not shipped in this repository** because the competition's redistribution terms require a separate rights review. Obtain them through the authorized ARC-AGI-3 development channel, not via repo auto-download. Archived reference runtime SHA-256: `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888` for `N100_ACTIVE_FSM_20261025.zip`.

The original N114 runner and N093 source checks are under `experiments/N114/`, with the original unmodified N114 report at `reports/findings/N114.md`. To reproduce in the original staging layout, use the archived N114 reproduction directory and restore its `inputs/N100_ACTIVE_FSM_20261025.zip` and `inputs/submission.py`. Then run:

```bash
cd N114_VALID_ARC3_PUBLIC_20261026
export OPENBLAS_NUM_THREADS=1
python3 prepare_runtime.py
python3 verify_release.py
python3 run_all_isolated.py --output-dir reproduction/fresh --timeout-seconds 90
```

Those commands apply to the **original archived layout**, not the curated GitHub source-only snapshot. The reusable scripts in this repository are retained for audit and to simplify rebuilding that layout; they are not claimed to be independently runnable without the original framework and fixtures.

The N117 original archive similarly supplies the fully reconstructible local-effect evaluation, but also requires N100 inputs, original result paths and the official game agent. Use the user-held original evidence archives for complete end-to-end replay.

## Rules

- Offline CPU notebooks, no Internet in competition reruns.
- Charged native actions only, no future observation, hidden engine variables, oracle path or simulator resets.
- Per-level cap of 200 policy actions; native `GAME_OVER` may happen earlier.
- No official Kaggle submission, score, private test set or human-normalized RHAE can be verified from this repository.

The `data/provenance/origins.csv` lists copied files and original SHA-256 hashes.
