# N107 — SMDP Meta-RL Over Object-Centric Options

**Purpose:** implement, falsify or support five source-grounded, object-centric options with duration-aware native-reward Bellman backups and a level-persistent meta-Q table. **Research artifact only; not a replacement Kaggle entry.**

## Quick results

- **Native:** 10 N093 development families × 2 matched arms = 20 real SDK episodes. Both 9 Level-1, 1 Level-2 completion; **1,116 charged actions each**, **0 grounded N107 actions**, **0 native meta-Q updates**. All matching actions/rewards/frames independently replayed once per family.
- **Controlled toy (not ARC):** four-step option learned/credited twice across recoloured levels, with persistent meta-Q and charged synthetic actions. The toy starts from a separately calibrated action model.
- **Tests:** 24 passing unit and regression tests.

Read `FINDINGS.md` for the exact failure mechanism, interpretation and caveats. Read `PROTOCOL.json` for the frozen evaluation.

## Reproduce the pure-code tests and toy

```bash
cd N107_SMDP_META_OPTIONS_20261025
python -m pip install numpy scipy pytest
PYTHONPATH="$PWD/src" python -m pytest -q -p no:cacheprovider tests
OPENBLAS_NUM_THREADS=1 python experiments/synthetic_transfer.py
```

The installed N106 modules are copied byte-for-byte, not rewritten from memory. The original frozen B1 and N093 native selector/checkpoint live in the **unaltered user-supplied N100 archive** included under `inputs/`.

## Reproduce the real SDK experiment (local, no cluster)

Requires the Python dependencies supplied by the N100 SDK (`numpy`, `scipy`, `torch`, `arc_agi`, and the frozen baseline dependencies). This archive contains the original source bundle; use a scratch extraction so the input archive stays byte-identical.

```bash
cd N107_SMDP_META_OPTIONS_20261025
mkdir -p work
unzip -q inputs/N100_ACTIVE_FSM_20261025.zip -d work
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/native_ab.py \
  --source "$PWD/work/N100_ACTIVE_FSM" \
  --out "$PWD/results/reproduced_native_ten.json" \
  --games ar25 cd82 g50t lp85 ls20 m0r0 s5i5 sc25 tu93 vc33 \
  --seed 76 --l1-cap 200 --l2-cap 200
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/replay_saved_native.py \
  --source "$PWD/work/N100_ACTIVE_FSM" \
  --results "$PWD/results/native_ten_families.json" \
  --out "$PWD/results/reproduced_replay_validation.json"
```

The benchmark uses native SDK actions only, **no RESET requests**, no hidden engine state or shadow lookahead, no LLM/VLM, and no sealed-family acting data. `vc33` is historically exposed and is *not* an untouched generalization holdout. There is no claim of a novel non-`vc33` win.

## Files

- `src/n107_smdp.py`: five abstract option proposals, invariant/coarse state descriptors, SMDP Q learning, persistent global option values, conservative B1 bridge.
- `src/n106_odsl.py`, `src/n106_executor.py`: unmodified source parser, action compiler and guarded executor.
- `src/core_priors.py`: retained 15-predicate general static library from the earlier heuristic candidate (N107 uses the five hand-authored option generators directly, not all 15 predicates).
- `experiments/native_ab.py`: 10-family true SDK frozen baseline vs N107 comparison.
- `experiments/replay_saved_native.py`: independent SDK replay of archived actions and frame hashes.
- `experiments/synthetic_transfer.py`: transparent calibrated toy, deliberately separate from real game evidence.
- `tests/test_n107.py`: SMDP correctness, grounding, abstention and transfer checks.
- `results/*.json`: native A/B, independent replay, synthetic control and smaller pilot.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: original research source and local SDK bundle, SHA retained.
- `inputs/frozen_submission.py`, `inputs/frozen_submission.ipynb`: byte-preserved earlier Kaggle baseline. **These are not rewritten with N107.**
- `PROTOCOL.json`, `FINDINGS.md`, `SHA256SUMS.txt`, `verify_package.py`: protocol, caveats and reproducibility.

**Do not submit N107 as though it improved the ARC score.** Kaggle entry and notebook execution require your authenticated Kaggle account; these local tests do not register or submit anything.