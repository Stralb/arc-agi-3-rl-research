# E012 validation

Local package validation completed before packaging:

- 4/4 isolated unit tests passed.
- Python source/scripts compile successfully.
- `configs/e012.json` parses as valid JSON.
- `submit_e012.sh`, `check_e012.sh`, `scripts/env.sh`, `scripts/worker_loop.sh`, and the Slurm worker pass `bash -n`.
- ACTION7/full ACTION6 coordinate-space handling remains inherited and unit-tested.

Cluster-only validation runs inside Slurm before any full task is claimed:

1. unit tests,
2. dependency/lock-in preflight,
3. real ARC smoke using the full and ablated systems.

The scheduler is resumable, uses atomic task locks, retries a failed task up to three times, and only writes the final lock-in after exactly 60 result files exist.
