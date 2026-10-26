# N098: Terminal-goal planning, two strictly different modes

**Status:** research-only, no deployed B1 promotion.

## Interface boundary

- `n098/observed.py` is an observation-only, charged-action intervention that uses the official `frame`, `legal action` and `level completed` fields. It requires no SDK cloning or hidden state.
- `n098/oracle_lab.py` is a **local oracle diagnostic**. It deep-copies the local SDK environment and searches hypothetical actions. Those shadow SDK steps are explicitly counted, not regarded as free Kaggle actions. It is disabled unless `N098_ENABLE_LAB_SHADOW=YES`, and must not be submitted as the competition actor.
- `n098/ablation_blind.py` is an outcome-blind **post-hoc** matched-schedule control. Its rule was chosen after seeing the first `vc33` live improvement. It is not a preregistered generalization test.
- `n098/exhaustive.py` proves there is no shorter completion within the initial four source-shaped control-centroid clicks on the fixed `vc33` puzzle, using 5,460 additional LAB simulation steps to exhaust all depths <=6.

## Readouts

`N098_RESULTS_20261025.md` is the scientific report. `results/n098/N098_10X3X3.json` is the 90-policy-arm ledger. `results/n098/N098_ANALYSIS.json` is its aggregated analysis. Episode `episode_provenance` explicitly differentiates 43 freshly executed N098 episodes from 47 inherited fallback-equivalent N097B controls.

## Commands

```bash
cd N098_MPC_INTRINSIC_GOAL
sh RUN_N098_CHECKS.sh
sh RUN_N098_NATIVE_REPLAY.sh

# Read-only reevaluation of the frozen ledger:
python -m n098.check
python -c "from n098.analyze import analyze; print(analyze())"

# Actually execute a new native observation-only run:
python -m n098.run --games vc33 --seeds 76 --arms live_recovery --out /tmp/n098_observation_only.json

# LAB PRIVILEGED ORACLE ONLY, NOT A COMPETITION AGENT:
N098_ENABLE_LAB_SHADOW=YES python -m n098.run --games vc33 --seeds 76 --arms oracle_lab --out /tmp/n098_lab_only.json
```

The inherited `RUN_N097B_CHECKS.sh` expects an exact old N097B file inventory and therefore intentionally rejects any added N098 files. Use `RUN_N098_CHECKS.sh` for the expanded release: it verifies every N097B ancestor SHA without falsely requiring the new files to be absent.