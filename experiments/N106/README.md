# N106 — Object-Centric Inverse Graphics (experimental, not a Kaggle submission)

The frozen B1 + N093 pretrained PUCT submission remains unchanged. This package includes a public-observation 64×64 object parser, three-operation image DSL, strictly grounded native action compiler, guarded native-step executor, B1 bridge, source-only audits, a small native SDK smoke experiment, negative controls and regression tests.

**Start with `FINDINGS.md` before interpreting results.** The compiler cannot infer unknown physics or the correct object-level winning program from image geometry alone. Recorded same-level source effects are not causal reward goals.

## Exact reproduction — offline audits

On a Python environment with `numpy`, `scipy`, `pytest`:

```bash
cd N106_OBJECT_DSL_20261025
python -m pytest -q tests
python verify_package.py
OPENBLAS_NUM_THREADS=1 python experiments/audit_native_level1.py
OPENBLAS_NUM_THREADS=1 python experiments/audit_local_effects.py
OPENBLAS_NUM_THREADS=1 python experiments/terminal_control.py
OPENBLAS_NUM_THREADS=1 python experiments/audit_contextual_grounding.py
```

The audit scripts overwrite generated `results/*.json` when rerun, so use a **copy** if you need to preserve the checksum-verified frozen outputs. The source data are the original N103 legally collected Level-1 `before`, same-level `after`, native B1 action and manifest arrays, copied byte-identically into `inputs/`. No hidden ARC state or test examples are present in the diagnostic labels.

## Optional fresh legal native SDK smoke reproduction

```bash
cd N106_OBJECT_DSL_20261025
python bootstrap_sdk.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiments/native_smoke.py \
  --source work/N100_ACTIVE_FSM \
  --out scratch_native_smoke.json \
  --games ar25 g50t lp85 m0r0 tu93 \
  --seeds 76 --l2-budget 100
```

All calls are legal `ACTION1`–`ACTION7` SDK actions. Level-1 max 200, Level-2 smoke max 100. There are **no explicit RESET actions**. The SDK is initialized once per episode; no game cloning, shadow oracle, environment-source inspection, or test-family trial is used for acting. Original frozen source SHA-256 `b012aa0eaf3d4e5c5fa1bd3c99711cc24810a9df043545586db3be0de922c888`. Local source needs the original SDK Python wheels/dependencies installed; package otherwise supports source-and-data offline audit only.

## Files

- `src/n106_odsl.py`: scene graph, exact visual transforms, strict and context-conditioned inverse action compiler, partial-effect diagnostic
- `src/n106_executor.py`: charged-step executor that checks observed native frame after each compiled click; guarded source-program learner
- `src/n106_bridge.py`: source-only compiler in front of untouched N093 B1 Bellman / PUCT with fail-closed fallback and 200-action cap
- `experiments/*.py`: archived native frame audit, local-effect negative control, contrastive terminal control, action-grounding diagnostic and legal native smoke
- `results/*.json`: frozen counts, paired SDK traces and calibration detail (not competition score)
- `inputs/N100_ACTIVE_FSM_20261025.zip`: original user-uploaded N100 predecessor archive, byte-identical
- `inputs/native_frames.npz` and `inputs/native_manifest.json`: frozen N103 Level-1 data with source provenance and episode boundaries
- `tests/`: synthetic unit and regression tests for ambiguous targets, native mismatch, isolation and safety
- `PROTOCOL.json`: no `vc33`/sealed-family sampling; split and metrics
- `SHA256SUMS.txt`, `verify_package.py`: content integrity

**Do not submit this experimental adapter instead of the frozen notebook.** It has not established an ARC improvement.