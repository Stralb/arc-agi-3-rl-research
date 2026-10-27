# N102 Offline Research Package

See [the archived N102 findings](../../reports/findings/N102_AFFORDANCE_AND_CONTRASTIVE.md) for methods, negative controls, matched metrics, limitations and go/no-go decisions. The commands below refer to the separately retained original N102 offline package, not a complete runnable copy in this GitHub subset.

## Required Python dependencies

Python 3.11+; `numpy`, `scipy`, `pytest`. The optional native frame-stack replay also requires the dependencies bundled by the N100/ARC SDK (available in the environment used to generate this package). There is no network access in these procedures.

## Reproduce all purely offline analyses and tests

```sh
cd N102_AFFORDANCE_CONTRASTIVE_OFFLINE_20261025
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python -m pytest -q tests
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python experiments/affordance_benchmark.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python experiments/contrastive_benchmark.py
```

## Optional: independently replay original saved Level-1 sources through the native SDK

**This replays 123 original recorded Level-1 actions on eight non-`vc33` training families.** It incurs native SDK actions locally; it does not choose any new actions, run membership queries, or test a new policy.

```sh
cd N102_AFFORDANCE_CONTRASTIVE_OFFLINE_20261025
python bootstrap_inputs.py
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 python experiments/check_frame_stack.py
```

The source ZIP checksum is checked by `bootstrap_inputs.py` and the source traces check every recorded public pre/post frame hash. No test accesses sealed ARC families or oracle game internals. Test modules include an explicit synthetic hidden-lock fixture to prove insufficient-mask aliasing; that fixture is **not** used by the agent as privileged information.

## Input and output boundaries

- N100's original ZIP is immutable source evidence and is included in `inputs/`.
- The replay NPZ and manifest come from the previous N101 audit's byte-level replay of the N093 frozen source traces.
- All N102 agent search outcomes in `results/affordance_benchmark.json` come from **synthetic procedural environments**, not ARC Level 2.
- All `results/contrastive_goals.json` reward frames are **real archived SDK-observed Level-1 rewards**; any candidate is **correlation only**, not a verified goal.
- `vc33` was not tested in N102. No cluster, submission, or online policy search was used.