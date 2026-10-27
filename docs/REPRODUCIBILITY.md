# Reproducing the published ARC-AGI-3 evidence

**Environment:** Python 3.11+ for the published source checks; NumPy, SciPy and PyTorch for native-agent Python imports (see [`requirements-agent.txt`](../requirements-agent.txt)). The official ARC SDK additionally supplies `arcengine` and `agents`, which are not bundled. The full historical native runtime and original trace data require separately authorized archives.

## Standard-library repository checks

```bash
git clone https://github.com/Stralb/arc-agi-3-rl-research.git
cd arc-agi-3-rl-research
python3 scripts/verify_repository.py
python3 -m unittest discover -s tests -v
python3 scripts/summarize_results.py
```

These checks confirm the **committed** frozen source hashes, notebook validity, public 25-family benchmark arithmetic and SVG plot integrity. They do **not** run the native game SDK, reproduce every original archived trace, check Kaggle submissions or validate private scores.

## Regenerate aggregated public-result figures

```bash
python3 -m pip install -r requirements-analysis.txt
python3 scripts/generate_plots.py
```

This produces two additional SVG and PNG charts from the CSVs in `data/outputs/benchmarks/`. All prior published charts remain available as SVG in `data/outputs/plots/`.

## Rebuild and verify the E126 Kaggle candidate offline

The E126 release in `src/e126_submission_agent.py` is a generated, self-contained research candidate, **not a Kaggle submission**. The binary checkpoint is in `assets/e126/`; its original teammate model provenance and permission require review.

```bash
python3 experiments/E126/build_candidate.py
python3 scripts/verify_e126_release.py
python3 -m unittest discover -s tests -v
```

These commands use only Python's standard library. The builder verifies frozen N117 and checkpoint SHA-256 hashes, reconstructs the generated notebook and agent, and the verifier checks that the rebuilt and committed bytes match their manifests. No SDK action, model inference, game rendering or Kaggle server run occurs. E126's stored E127 native results and E128 parity are **historical public-game evidence**, not results recomputed by these commands. The official Kaggle rerun remains unverified.

## Native replay and source archives

The original offline research archive included the official SDK/game fixtures, experiment-specific native runners and extensive per-step action/frame records. It is **not fully mirrored to this public repository**.

- Original SDK reference archive: `N100_ACTIVE_FSM_20261025.zip`, SHA-256 `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`.
- Archived N114 native harness: `N114_VALID_ARC3_PUBLIC_20261026`, original 25-family replay.
- Archived N117 native comparison: `ARC_DEEP_RL_AUDIT_20261026`, original local effect-memory evidence.

Those archived tools require separately authorized SDK assets and the original directory layout. Do not attempt to execute them with missing files or claim the GitHub subset is a complete replay environment.

The public `experiments/` directory contains selected implementational variants, experiment notes and changelogs. The original archive holds additional scripts, tests, raw frames and engine-specific fixtures. See [repository coverage](REPOSITORY_COVERAGE.md).

## Verified historical public findings

- Frozen N093: 13 Level-1, 1 Level-2 (`vc33`), 0 Level-3+; 2,982 charged SDK actions across 25 games.
- Experimental local effect-memory: 13 Level-1, 2 Level-2 (`vc33`, `tu93`), 0 Level-3+; 2,790 charged SDK actions.
- Both scores are **public offline native level counts**, not private Kaggle scores or human-normalized RHAE.
- All games are historically exposed. Repeated seeds with identical start frames do not establish independent generalization.

## Method constraints

Only legal native SDK actions are charged; no game-specific solutions, privileged source physics, shadow oracle, future frame or uncharged resets belong in a deployable acting controller. Level action budgets are bounded at 200, while native `GAME_OVER` can happen earlier.

The repository is public. Do not redistribute private competition assets, credentials or unlicensed game-engine code.


## Restore the original N114/N117 native harness from owner-held SDK archives

The public repository now contains the original N114 runner, the N117 local-effect runner, and independent replay verifiers. The SDK and frame data are NOT part of this repository. Use only the archives you are authorized to access.

Run these commands from the cloned repository root; replace the two example archive paths with your own local copies:

```bash
python3 scripts/prepare_native_workspace.py --experiment N114 --n100-runtime /path/to/N100_ACTIVE_FSM_20261025.zip --frozen-release /path/to/FROZEN_B1_PRETRAINED_PUCT_KAGGLE_20261025.zip --destination /tmp/arc-n114
cd /tmp/arc-n114
python3 prepare_runtime.py
python3 run_public_games.py --families vc33 --output-dir reproduction/smoke
python3 run_all_isolated.py --output-dir results --timeout-seconds 90
python3 verify_release.py
```

For the N117 action-effect ablation, use `--experiment N117 --destination /tmp/arc-n117`, then in that new workspace run `python3 prepare_runtime.py`, `python3 run_native.py --arm baseline --families vc33`, `python3 run_native.py --arm local --families vc33`, and `python3 verify_replay.py results/local/vc33.json`.

The staging script checks the original archive SHA-256 hashes and does not execute or silently redistribute game data. The N114 verifier needs a complete 25-game run; it is not expected to pass after a one-game smoke test.
