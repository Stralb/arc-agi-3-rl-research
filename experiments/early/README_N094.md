# N094 — Symbolic Policy Synthesis from Native Level-1 Trajectories

**Final result: negative.** The only accepted Level-1 decision tree is from `vc33`. It takes **zero actions** in Level 2 or later. N094 exactly matches its fallback controller and does not improve native level completions or action efficiency. See `N094_RESULTS_20261025.md` for the full evidence, limitations and experimental provenance.

## Reproduce the release

In a **new terminal** after extracting `N094_SYMBOLIC_POLICY_20261025.zip`:

```bash
cd N094_SYMBOLIC_POLICY
./RUN_N094_CHECKS.sh
./RUN_N094_NATIVE_REPLAY.sh
```

The first script checks SHA-256 package contents, frozen N093 source, 47 automated tests, source freeze, the N093 reference result ledger and the 90-arm N094 merged evidence. The second script independently replays all 10,208 recorded SDK actions on fresh native game instances; no policy model is used in replay.

To perform new, **native acting-policy** runs for any subset of the 10 permitted development games (use a unique output filename):

```bash
cd N094_SYMBOLIC_POLICY
. ./ENV.sh
python -m n094.run --games vc33 sc25 --seeds 76 --arms symbolic_strict symbolic_guarded symbolic_b1_fallback --out results/N094_FRESH_CHECK.json
```

To reproduce the complete **native Level-1 source screening** (requires a fresh native SDK instance for each winning source):

```bash
cd N094_SYMBOLIC_POLICY
. ./ENV.sh
python -m n094.screen
```

This last command rewrites only the screen diagnostics and will invalidate the signed file inventory; for research regeneration, **make a copy of the extracted package first** and use that copy. Prefer read-only `./RUN_N094_CHECKS.sh` for verification of an official release.

To rerun every acting policy from scratch, use `n094.run` separately per game with a fresh output path, three policy seeds and three arms. The frozen release conserves time by inheriting historical N093 control traces only when native source screening proves the symbolic program cannot activate. Every inherited trace is marked `NOT_new_native_execution`. All active-rule `vc33` episodes were rerun natively in full.

## Methods and source data

- `n094/objects.py`: 26 discrete current-object and relational features, no raw color IDs or absolute coordinate features.
- `n094/synthesis.py`: bounded-depth, Occam-penalized decision tree with readable AST; unchosen alternative actions are *not* labelled native failures.
- `n094/agent.py`: B1 with strictly legal Level-2 symbolic pre-emption and optional fallback guard, unchanged native Bellman learning.
- `n094/run.py`: prospective native SDK episode runner; no replayed Level-2 solutions and no SDK probes.
- `n094/screen.py`: native Level-1 replay source screening, with exact pre/post frame hashes.
- `n094/merge.py`, `n094/analyze.py`, `n094/check.py`, `n094/verify.py`: transparent exact-match accounting, analysis and verification.
- `protocol/N094_FROZEN.json`, `protocol/N094_CODE_FREEZE_SHA256.txt`: original action budgets, source/holdout constraints and frozen acting code.
- `results/N094_SCREENING.json`: complete object-property candidate matrices and source-level rule diagnostics for the 27 native-winning episodes.
- `results/N094_vc33.json`, `results/N094_ar25.json`, `results/N094_cd82.json`, `results/N094_g50t.json`: 31 fresh prospective N094 native episode traces.
- `results/N094_10X3X3.json`: 90-arm complete comparison ledger, tagging 31 fresh episodes and 59 inherited exact-equivalence controls.
- `results/N094_ANALYSIS.json`: per-arm native action/reward totals and matched milestones.
- Original `n093`, checkpoint, SDK, results and previous experimental lineage: **unchanged**, with 408 SHA-256 hashes checked.

The 15 previously used public evaluation families are blocked in native acting code. The output is a public development experiment, not a Kaggle score.