> **Public repository edition:** This folder now contains the original N114 evaluation and verification source, but **not** the `inputs/`, `work/`, raw native traces or official SDK referred to below. To run it, first use [the authorized setup instructions](../../docs/REPRODUCIBILITY.md). `verify_release.py` runs only after a complete 25-game native run; it cannot verify a one-family smoke test.

# N114 — Public 25-game ARC-AGI-3 offline evaluation

Read `FINDINGS.md` for all 25 results, scope correction and limitations.

Contents: `inputs/` archived frozen agent and original SDK source; `results/` 25 native action traces, matrix, verification, logs; `prepare_runtime.py` reproduces local SDK; `run_public_games.py` executes the exact frozen submission core; `run_all_isolated.py` executes all 25 games in fresh Python processes; `verify_release.py` checks source hashes and original N093 parity.

Commands:

```bash
python prepare_runtime.py
python verify_release.py
OPENBLAS_NUM_THREADS=1 python run_all_isolated.py --output-dir reproduction/fresh --timeout-seconds 90
```

No ARC-AGI-1 static 400+400 grid benchmark result is claimed. No Kaggle score or private submission is claimed.