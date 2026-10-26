# N100 ACTIVE FSM — executable research snapshot

Read `N100_RESULTS_20261025.md` first. This is a reproducible **interim release**, not a finished 10-family evaluation.

- `n100/learner.py`: one-SDK-instance, charged native membership-query learner; tests bounded prerequisite word grammar and extracts observed same-gap distinguishing suffixes
- `n100/run.py`: complete Level-1 B1 source collection, source-only terminal AST extraction, charged Level-2 query and reset orchestration, fallback agent
- `n100/verify.py`: independent action-only native replay, including RESET and Level-1 reentry
- `results/n100/N100_VC33_3SEED.json`: three fresh runs, 68 charged SDK calls per run, independent seven-click verification
- `results/n100/SANITY_OTHER_FAMILIES.json`: fresh single-seed smoke tests on three other training families
- `protocol/N100_FROZEN.json`: partition, seeds, query budget, and claim limits
- `tests/test_n100.py`: N100 checks and independent SDK replay

N100 distinguishes abstract state aliasing but does **not** implement formal L* equivalence queries. Existing N099 reference and all ancestor files are preserved. `RUN_N100_CHECKS.sh` uses the new N100 payload verifier. The N099 standalone verifier has an exact old file inventory and should not be used for the expanded N100 root.