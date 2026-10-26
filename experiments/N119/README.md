# N119 — Delayed Native-Reward Credit and State-Return Risk (Offline ARC-AGI-3)

**Status:** completed reproducible research; negative deployment result.

This package tests two proposed improvements to the 15-level public local-effect candidate:

- Cross-level short-horizon eligibility associations drawn only from actual native level-completion rewards.
- Observational risk penalties for action descriptors that return to recent full-frame states.

It includes a falsification control with wrong descriptor attribution and a family-held-out hazard diagnostic. The risk penalty never hard-masks legal actions. No object grammar, oracle, hidden state, sidecar agent, external online calls or synthetic reward enters the actor. Only native levels-completed events update Bellman rewards. Every action is SDK-charged and subject to 200 actions per level.

## Final findings

| Agent | L1 | L2 | L3+ |
| --- | ---: | ---: | ---: |
| Original frozen N093 | 13 | 1 | 0 |
| Previously released local+effect candidate | 13 | 2 | 0 |
| N119 delayed credit | 13 | 2 | 0 |
| N119 state-return risk | 13 | 2 | 0 |
| N119 combined | 13 | 2 | 0 |
| N119 wrong-attribution control | 13 | 2 | 0 |

N119 produces **zero new rewarded levels**. The risk-only branch is action-for-action identical to the previous local+effect controller. The combined branch is action-for-action identical to credit-only. Read `FINDINGS.md` for caveats and exact observations.

## Directory guide

- `inputs/submission.py`, `inputs/submission.ipynb` — immutable original N093 source and Kaggle notebook.
- `inputs/N100_ACTIVE_FSM_20261025.zip` — archived public SDK needed to reproduce native games offline.
- `src/reference_policy.py`, `src/effect_prior.py` — audited existing B1/N117 selector dependencies.
- `src/delayed_credit.py` — new native-reward eligibility and return-risk selector.
- `run_native.py`, `run_matrix.py` — full charged SDK evaluation.
- `verify_replay.py` — independently executes recorded native actions (without loading the policy).
- `generate_candidate.py`, `candidate_submission.py`, `candidate_submission.ipynb` — optional research-only single-file controller; **not promoted**.
- `hazard_audit.py`, `inputs/n118_logged_native25/`, `results/hazard/` — family-held-out terminal-window prediction diagnostic.
- `analyze.py`, `results/analysis/` — exact native benchmark and source-parity validation.
- `results/native25/` — 100 native evaluation episodes, action-by-action frames hashes, rewards, terminal states.
- `results/policy_seed_77`, `results/policy_seed_78` — extra policy seed controls.
- `tests/`, `SHA256SUMS.txt` — regression/integrity checks.

## Reproduction from fresh extraction

Linux, Python 3.11+, NumPy, SciPy, PyTorch, pytest; scikit-learn is needed only for `hazard_audit.py`. No Kaggle login or Internet needed.

```bash
cd N119_DELAYED_CREDIT_RISK_20261026
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python prepare_runtime.py
PYTHONPATH="src:inputs:work/N100_ACTIVE_FSM/sdk_runtime/site:work/N100_ACTIVE_FSM/baseline_source:work/N100_ACTIVE_FSM" python -m pytest -q tests
python analyze.py
python hazard_audit.py
python verify_candidate_parity.py
python verify_replay.py results/native25/*/*.json
python verify_replay.py results/policy_seed_*/*/*.json
sha256sum -c SHA256SUMS.txt
```

Re-run all four live arms on all 25 public games (separate output, avoid overwriting original evidence):

```bash
cd N119_DELAYED_CREDIT_RISK_20261026
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python run_matrix.py --arms delayed_credit state_return_risk credit_plus_risk attribution_placebo --workers 4 --timeout 160 --out results/new_live_25
```

Rebuild the research-only notebook: `python generate_candidate.py`. The original notebook in `inputs/` is never modified.

## Integrity and scientific validity

The source SHA-256 hashes of the original frozen files are preserved in `FINDINGS.md`; the release file-level manifest is in `SHA256SUMS.txt`. A valid observational result must not be confused with a causal intervention: predicting future terminal outcome under an archived policy does not identify the effect of an alternative action. All 25 game layouts were previously exposed. New policy seeds repeat the same layouts. No official RHAE or hidden-test score is claimed.