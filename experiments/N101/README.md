# N101 Bellman Fix + N097B Nine-Family Offline Audit

See **`FINDINGS.md`** for evidence, limitations, and exact source references.

The package contains the original, unchanged N100 archive alongside N101/N101B code, a repaired **observed-graph** Bellman learner, 44 tests, 96 synthetic matched conditions, 518 SHA-verified native Level-1 source replay actions, 24 real outgoing terminal frames, and a nine-family goal signature audit. It does **not** contain a successful new Level-2 controller or any new `vc33` run.

## Dependencies

Python 3.11+ recommended, with `numpy`, `scipy`, `Pillow`, `pytest`, and `torch` installed. The captured ARC SDK and environment files are shipped in `inputs/N100_ACTIVE_FSM_20261025.zip` and become available under `work/N100_ACTIVE_FSM` after bootstrapping.

## Quick verification

```sh
cd N101_N097B_AUDIT_20261025
python bootstrap_inputs.py
PYTHONPATH=src pytest -q tests
PYTHONPATH=src python experiments/trap_witness.py
PYTHONPATH=src python experiments/verify_rta_grid.py
PYTHONPATH=src python experiments/fixed_vs_ablation_procedural.py
```

To reproduce the native **source-only** evidence (replays frozen N093 actions and checks every frame hash; this is not policy evaluation):

```sh
cd N101_N097B_AUDIT_20261025
python bootstrap_inputs.py
OPENBLAS_NUM_THREADS=1 python experiments/recover_native_l1.py
OPENBLAS_NUM_THREADS=1 python experiments/strict_masked_source_replay.py
OPENBLAS_NUM_THREADS=1 python experiments/strict_unmasked_recheck.py
OPENBLAS_NUM_THREADS=1 python experiments/generic_goal_audit.py
python experiments/make_contact.py
PYTHONPATH=src pytest -q tests
```

**Do not** run `n100.run`, full native evaluation or cluster jobs as part of this reproduction. No software or network download is performed by these scripts.

## What counts as evidence

- `src/n101_bellman_fixed.py`: a corrected mathematical/graph implementation, not a guaranteed POMDP solver.
- `results/bellman_trap_witness.json`: proves backups change decisions on a controlled synthetic graph.
- `results/procedural_repair_ablation.json`: 96 synthetic paired cases; backups not uniformly advantageous.
- `results/native_replay_manifest.json` + `results/l1_native_frame_replay.npz`: raw public ARC Level-1 observations, produced by hash-verified replay of historic N093 actions.
- `results/goal_signature_audit.json`: exploratory geometry/topology features **with exhaustive nonreward control**; never count these as validated reward-goal ASTs.

All frame/goal extraction analyses are confined to the nine training families **other than `vc33`**. The original archived N097B strict extractor has no accepted goal on those eight completed families, and `s5i5` has no archived Level-1 success.