# N103 Offline Research Package

Research focus: forced native Level-1 trajectory diversity, source-only contrastive goals, recurrent next-frame prediction, predictive-state clustering and synthetic Bellman search.

Read `FINDINGS.md` for the experimental evidence, limitations, exact denominators, negative results and required next validation gates. The source and evidence package is self-contained for reproducing the offline results on Python 3.11+ with `numpy`, `torch`, `scipy`, `scikit-learn`, `joblib`, `pytest` and the bundled local ARC runtime. It does **not** claim official ARC or Kaggle evaluation.

## Reproduce the frozen results

From the directory containing this README:

```bash
python -m pytest -q tests
python verify_package.py
python experiments/diverse_goals.py
python experiments/synthetic_latent.py
python experiments/predictive_search.py
python experiments/train_native.py --steps 150
python experiments/native_belief_audit.py
```

`experiments/synthetic_latent.py` retrains and overwrites the *local* synthetic checkpoint and cluster file, so run checksum verification **before retraining**. `experiments/train_native.py` likewise overwrites its local model checkpoints. For exact frozen-checksum verification use a clean extracted copy and do not retrain in that directory. The original result files and trained models are already included.

## Replay the actual local SDK native source trajectories

```bash
python bootstrap_inputs.py
mkdir -p scratch_native
python experiments/collect_native.py --out scratch_native
python - <<'PY'
import numpy as np
f=np.load('inputs/native_frames.npz')
g=np.load('scratch_native/native_frames.npz')
for k in ('before','after','action'):
    assert np.array_equal(f[k],g[k]),f'Mismatch: {k}'
print('All native collected arrays identical')
PY
```

The new source trajectories are Level-1 only and stop at the first actual reward or 90 steps. They use fresh environment instances (60 total, tracked separately), but do not call the SDK RESET action. Every chosen action comes from the currently legal B1 candidate set. The `N100` SDK source ZIP is independently SHA-256 checked before extraction; the reproducibility script does not require network access. Runtime availability depends on the bundled native SDK Python dependencies. Python interpreter/library versions may alter optimizer reproducibility.

## Output register

- `PROTOCOL.json`: predeclared families, seeds, exploration levels, safety and metrics.
- `inputs/native_frames.npz`: public before and same-level after frames plus B1 action indices, 1,848 executed actions.
- `inputs/native_manifest.json`: all 60 episode boundaries, seed metadata, native reward and action-trace hashes.
- `inputs/N100_ACTIVE_FSM_20261025.zip`: original user-provided frozen predecessor archive.
- `src/native_gru.py`: full-resolution action-conditioned frame predictor.
- `src/synthetic_belief.py`: synthetic POMDP, trained recurrent predictor, raw and predictive-state clustering adapter.
- `src/n101_rta.py`, `src/n101_bellman_fixed.py`, `src/n102_contrastive.py`: byte-preserved research baselines.
- `results/native_prediction.json`: held-out 449 native transition prediction metrics, controls and per-episode loss.
- `results/native_belief_audit.json`: held-out native transition alias and fragmentation controls.
- `results/diverse_goal_validation.json`: independent-path candidates and nonreward controls.
- `results/synthetic_latent.json`: synthetic GRU accuracy and raw latent search negative result.
- `results/predictive_search.json`: all 252 matched search policy traces and predictive state controls.
- `results/*.pt`, `results/*.joblib`: learned checkpoints and training-only cluster models.
- `tests/test_n103.py`: offline unit/regression/ablation checks; tests do not run any native environment or reset.
- `SHA256SUMS.txt`: immutable artifact hashes; `verify_package.py`: verification.

**Important:** Synthetic environment state (`depth`, `mode`) exists for evaluator label generation; acting models and search adapters never receive it. Predicted hypothetical actions in the synthetic PSR are neural forward passes, not SDK calls. The fixed synthetic geometric goal heuristic and source-derived reducer preference are not verified general-purpose ARC features.