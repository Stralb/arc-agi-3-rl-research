# N093 — Hindsight Returns and PUCT-Style Selection

This executable research package runs real native ARC-AGI-3 SDK episodes. It is
an **unsuccessful transfer/improvement experiment** with one small known-family
action-efficiency saving. It leaves B1's checkpoint and native Bellman code
unchanged. It does not solve new held-out games.

## Reproduce the verified artifacts

```bash
./RUN_N093_CHECKS.sh
./RUN_N093_NATIVE_REPLAY.sh    # longer: all 150 episodes and 16,380 native actions
```

Native replay from individual experiments, if time-limited:

```bash
. ./ENV.sh
python -m n093.verify results/N093_vc33.json
python -m n093.verify results/N093_sc25.json
```

To regenerate all native trajectories, use a NEW isolated output path instead
of overwriting frozen evidence. For example:

```bash
. ./ENV.sh
python -m n093.run --games vc33 --out /tmp/N093_new_vc33.json
```

### Experiment files

- `protocol/N093_FROZEN.json`: frozen five-arm protocol and allowed 10 families.
- `n093/hindsight.py`: discounted factual Monte Carlo returns and trained neural policy.
- `n093/agent.py`: one-step neural-PUCT-style action ordering, *not AlphaZero MCTS*.
- `n093/run.py`: 200-decision native SDK runner; no probing or reset actions.
- `n093/analyze.py`, `n093/check.py`, `n093/verify.py`: paired and independent checks.
- `results/N093_10X3X5.json`: complete original 150 episodes and full factual frame-hash traces.
- `results/N093_ANALYSIS.json`: action/reward comparisons and family-cluster interval.
- `results/N093_<game>.json`: 15-arm subsets for manageable native replay.
- `N093_RESULTS_20261025.md`: scientific analysis and negative promotion decision.
- Original N090–N092 source, records, SDK runtime and frozen B1 checkpoint are
  preserved under their original paths. SHA-256 hashes are checked before release.

All 15 previously used public evaluation families are explicitly blocked.
The experiment is known-family development research, not a Kaggle leaderboard score.