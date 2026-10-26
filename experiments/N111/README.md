# N111 — Global Grid DSL Search: Research Package

This is **a measured negative program-synthesis experiment**, not a native ARC-AGI-3 solving submission. See `FINDINGS.md`.

### Verified result

15 original training families (no sealed test): nine successful Level-1 input/target pairs from 912 charged SDK calls. Depth-three exact bounded BFS found **0/9 exact whole-grid programs**. Eight searches exhausted, one hit the 5,000 expanded-state cap. Replaying the nine successful native L1 traces required 203 additional independently verified SDK actions, revealing that ACTION6 is legal in seven Level-2 states but *does not expose pixel colour setting*; no Level-2 actions or wins are claimed for N111.

### Requirements

Python >= 3.11, numpy, scipy, pytest, torch, and dependencies bundled with the archived native SDK. No network, LLM, VLM, game-source inspection, hidden simulator state, uncharged action probes or inference resets.

### Verify packaged evidence

```sh
python verify_results.py
PYTHONPATH=src python -m pytest -q tests
python bootstrap_inputs.py
```

### Rerun the original Level-1 collection in a NEW result directory

```sh
python bootstrap_inputs.py
mkdir -p reproduction/native
OPENBLAS_NUM_THREADS=1 python experiments/collect_training_l1.py --output-dir reproduction/native
```

### Refit all nine actual terminal grids via bounded BFS

```sh
OPENBLAS_NUM_THREADS=1 python experiments/evaluate_programs.py --results-dir reproduction/native --depth 3 --states 5000
```

### Independently replay the original Level-1 actions and inspect Level-2 legal actions

```sh
OPENBLAS_NUM_THREADS=1 python experiments/audit_level2_interface.py --results-dir reproduction/native
```

These scripts strictly separate the original 912 policy-data SDK actions, the 203 replay-verification SDK actions, and **zero N111 Level-2 execution actions**. Re-running the source collection uses new SDK instances and is accounted for as a new experiment, not free cached observations.

The original frozen Kaggle notebook is preserved as `inputs/frozen_submission.ipynb` with SHA-256 `1c235b29c71745d80cb639520528a36d2c9e7f4849bc561c645e736f06f745c4`. **Do not submit N111 in place of it.**