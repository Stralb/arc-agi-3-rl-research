# Archived N117 native tests

These tests are retained from the original 2026-10-26 deep-level RL audit. They are **not** part of the public repository's standard-library CI.

They depend on the owner-held N100 native runtime and original experiment ledger files under `inputs/` and `results/`, including `summary.json` and `local/tu93.json`. Merely staging the runtime is not sufficient to make those archived outputs appear.

Run only after restoring the original authorized data and archived experiment layout:
```bash
python3 -m pytest experiments/N117/tests -q
```

Do not infer from the presence of these test sources that they were run or passed on GitHub Actions.
