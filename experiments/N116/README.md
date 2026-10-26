# N116 native checkpoint validity gate

A self-contained research audit of the suggested "object-factorized checkpointing" concept, deliberately **not a new competition agent**. Relies only on public SDK observations. Original frozen source included for verification; no modifications to `submission.py`.

## Reproduce from an extracted archive

```bash
cd N116_CHECKPOINT_EXPERIMENT_20261026
python prepare_runtime.py
OPENBLAS_NUM_THREADS=1 python -m pytest -q tests
OPENBLAS_NUM_THREADS=1 python run_native_ablation.py
OPENBLAS_NUM_THREADS=1 python analyze_reward_events.py
OPENBLAS_NUM_THREADS=1 python verify_native.py
python verify_release.py
```

Python dependencies: numpy, scipy, torch, pytest, bundled native SDK. Runs on CPU. The only fresh SDK calls are the actual native policy evaluations and separate forensic verification replays, never free planning probes for the actor.

## Files

- `n116_checkpoint.py` — observation-only local effect extractor and guarded cross-level evidence gate.
- `run_native_ablation.py` — matched Level-3-reaching experimental local-effect reference versus checkpoint wrapper, every native action charged.
- `analyze_reward_events.py` — retrospective in-level reward-frame/false-positive audit. NOT available to acting controller.
- `verify_native.py` — policy-free native SDK replay of archived actions. NOT available to acting controller.
- `results/` — native outcome/action traces and per-level reward-template comparisons.
- `inputs/submission.py` — unmodified N093 frozen baseline; `inputs/policy.py` — original local-effect experimental policy; `inputs/n106_odsl.py` — original N106 parser; `inputs/N100_ACTIVE_FSM_20261025.zip` — archived public SDK runtime.
- `tests/` — eight synthetic regression checks, including no invented native reward.
- `FINDINGS.md` — limitations, exact result matrix, deployment decision.

**No hidden SDK states or engine source strategies are used.** Reproducibility SDK verification uses a separate episode replay, not an oracle queried during native action selection.