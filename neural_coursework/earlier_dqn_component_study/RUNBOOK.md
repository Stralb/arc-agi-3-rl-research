# E012 runbook

## Install

```bash
cd /home-mscluster/astrauss
rm -rf arc_rl_final_e012
unzip ARC_E012_FINAL_DQN.zip
mv ARC_E012_FINAL_DQN arc_rl_final_e012
cd arc_rl_final_e012
```

## Run

```bash
bash submit_e012.sh --fresh
```

Resume without deleting completed task files:

```bash
bash submit_e012.sh --resume
```

## Monitor

```bash
watch -n 10 'cd /home-mscluster/astrauss/arc_rl_final_e012 && bash check_e012.sh'
```

## Completion

```bash
cat results/REPORT.md
cat results/LOCK_IN.json
```

Do not run training, smoke tests, or unit tests directly on the login node. The one-time validation gate executes inside the first Slurm worker.
