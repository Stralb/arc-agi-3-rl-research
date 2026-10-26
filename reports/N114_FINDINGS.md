# N114 — Complete public ARC-AGI-3 baseline benchmark

**Correct benchmark:** ARC-AGI-3 is interactive, and its local public-game snapshot contains 25 environments. The 400 training and 400 evaluation task split belongs to ARC-AGI-1 static grid prediction. The frozen N093 action agent cannot be assigned a score over 800 static ARC-AGI-1 tasks.

## Headline result

**25/25 evaluated, 13 Level-1 completions, 1 Level-2 completion, 0 Level-3+ completions; 2,982 local env.step actions.** The sole Level-2 finisher is **vc33**. It received its native L1 reward at call 3, L2 reward at call 30, and ended GAME_OVER after 105 total calls.

Raw completed-level count is **14**, not an official Kaggle score and not the historical N093 30-completion result on 10 families x 3 seeds.

The experiment uses native SDK seed 47 and policy seed 76, the frozen checkpoint and controller, 200 actions per level. No explicit reset queries, hindsight adaptation, top-k pruning, GRUs, object compilers, coordinate dispatch or model-based look-ahead. `vc33` terminates naturally after 75 Level-3 actions; no global Level-3 cap was forced.

The local SDK creates a playable environment through `make(...)`. The 2,982 counted actions are charged `env.step` actions, excluding any separate framework initialization RESET call a Kaggle implementation might require.

## Per-family matrix

| Game | Archived split | L1 | L2 | L3+ | SDK actions | Stop reason |
|---|---|---:|---:|---:|---:|---|
| ar25 | train | 1 | 0 | 0 | 215 | per_level_200_cap |
| bp35 | train | 0 | 0 | 0 | 34 | native_terminal |
| cd82 | validation | 1 | 0 | 0 | 108 | native_terminal |
| cn04 | train | 0 | 0 | 0 | 75 | native_terminal |
| dc22 | train | 1 | 0 | 0 | 222 | native_terminal |
| ft09 | originally sealed* | 0 | 0 | 0 | 65 | native_terminal |
| g50t | train | 1 | 0 | 0 | 147 | native_terminal |
| ka59 | train | 0 | 0 | 0 | 100 | native_terminal |
| lf52 | train | 1 | 0 | 0 | 244 | per_level_200_cap |
| lp85 | train | 1 | 0 | 0 | 196 | native_terminal |
| ls20 | validation | 1 | 0 | 0 | 79 | native_terminal |
| m0r0 | train | 1 | 0 | 0 | 176 | native_terminal |
| r11l | originally sealed* | 0 | 0 | 0 | 60 | native_terminal |
| re86 | train | 0 | 0 | 0 | 100 | native_terminal |
| s5i5 | originally sealed* | 0 | 0 | 0 | 50 | native_terminal |
| sb26 | train | 0 | 0 | 0 | 200 | per_level_200_cap |
| sc25 | validation | 1 | 0 | 0 | 43 | native_terminal |
| sk48 | validation | 0 | 0 | 0 | 200 | native_terminal |
| sp80 | train | 1 | 0 | 0 | 49 | native_terminal |
| su15 | validation | 0 | 0 | 0 | 39 | native_terminal |
| tn36 | train | 1 | 0 | 0 | 75 | native_terminal |
| tr87 | originally sealed* | 0 | 0 | 0 | 128 | native_terminal |
| tu93 | train | 1 | 0 | 0 | 72 | native_terminal |
| vc33 | originally sealed* | 1 | 1 | 0 | 105 | native_terminal |
| wa30 | train | 0 | 0 | 0 | 200 | native_terminal |

*Originally sealed is the historical protocol label; `vc33` and other public cases have already been exposed in prior development research. None are claimed as untouched test cases.*

## Original split breakdown

| Historical group | Games | L1 | L2 | L3+ | SDK actions |
|---|---:|---:|---:|---:|---:|
| 15 precommitted train | 15 | 9 | 0 | 0 | 2105 |
| 5 validation | 5 | 3 | 0 | 0 | 469 |
| 5 originally sealed | 5 | 1 | 1 | 0 | 408 |

## Verification

- Frozen `submission.py` SHA-256: `e6c6a49c82e93294ae42eb1ee9d87d94a1dde329964e1d7358f63c7d63ba184d`. Matches the archived frozen submission release.
- Frozen `submission.ipynb` SHA-256: `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`. Matches the archived frozen release.
- All ten original N093 pretrained-PUCT / policy-seed-76 games reproduce the first **1,176 actions** action-for-action, with identical before/after frame hashes and reward-level progression. `ar25` continues beyond 200 total calls only because the submission is capped per level.
- The first long all-family process stalled at `wa30` after 24 finished games. Re-running `wa30` in a fresh process completed 200 valid actions with no level reward. The recommended reproduction uses isolated per-game processes.
- No private Kaggle submission, official relative-efficiency score or hidden-test result was obtained.

## Reproduce offline (full commands)

Run these commands from the extracted `N114_VALID_ARC3_PUBLIC_20261026` directory:

```bash
python prepare_runtime.py
python verify_release.py
OPENBLAS_NUM_THREADS=1 python run_all_isolated.py --output-dir reproduction/fresh --timeout-seconds 90
```

The packaged `results/public25_native_traces.json` is the complete native trace ledger; `results/public25_matrix.csv` is the concise matrix. All actions originate from the embedded frozen submission core and SDK legal-action interface. This reproduction does not inspect game source to guide the agent.

## Deployment

**Retain the unmodified frozen Kaggle notebook.** Public-game completion counts do not establish a leaderboard score, hidden-test reliability or generalization to the private game distribution. Entry eligibility requires accepting Kaggle rules before the October 26, 2026 entry deadline; final code deadline is November 2, 2026.
