# E012 — Final DQN Consolidation

E012 is the final manual DQN consolidation experiment. It does **not** introduce a new mechanism.

## Frozen evidence entering E012

- E004 representation: `E-onehotcnn__T-stack2__A-vector__U-effect`.
- E008: Dueling DQN selected as the development backbone.
- E009: full D14 structured epsilon exploration produced the clear behavioral gain and is retained.
- E010: mechanics adaptation improved mechanics prediction but produced no behavioral uplift; excluded.
- E011: mechanics persistence tied the E009 behavioral control; excluded.

## Four matched systems

1. `E12_F_full_dueling_d14` — final full stack.
2. `E12_A_no_d14` — Dueling DQN + uniform epsilon exploration.
3. `E12_A_no_dueling` — non-dueling DDQN + D14.
4. `E12_A_plain_ddqn` — non-dueling DDQN + uniform epsilon exploration.

All other settings are matched. Evaluation uses all 25 public ARC-AGI-3 games, three new seeds, and a 600-command budget: 60 tasks = 300 game-runs.

## Parallel execution

E012 replaces fixed serial shards with a shared dynamic task queue. Every allocated CPU core can execute an independent ARC task, while a biggpu worker uses one CUDA lane plus its remaining allocated CPU lanes. Slow games therefore do not strand a shard. No Slurm arrays and no controller job are used.

Hard user job caps remain respected: batch <= 4, stampede <= 2, bigbatch <= 1, biggpu <= 1.

## Launch

```bash
bash submit_e012.sh --fresh
```

Monitor:

```bash
watch -n 10 'cd /home-mscluster/astrauss/arc_rl_final_e012 && bash check_e012.sh'
```

Expected final outputs:

- `results/LOCK_IN.json`
- `results/ABLATION_RESULTS.json`
- `results/REPORT.md`
- `artifacts/e012_scheduler/COMPLETE`
