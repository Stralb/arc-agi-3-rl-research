# N092 — Neural Q-Distillation / Value Cloning

**Result: no deployment.** Distillation of the actually observed final Level-1 B1 Q table succeeds as a regression problem, but it decreases native completions from **30 to 27** across 30 training-family episodes. The teacher contains no distinguishable prerequisite values: **350 source Q labels are 0.985 and 27 terminal labels are 1.0.** The loss of all three `vc33` Level-2 completions makes the current neural-anchored Q initialization unsafe.

N092 does not change native rewards, the Bellman algorithm, action legality, or the frozen B1 checkpoint. No Level-2 solution data is available to the acting or training policy. No 15-family public evaluation games are accessed.

## Reproduce and verify

In a new terminal, after extracting the archive:

```bash
cd N092_NEURAL_Q_DISTILLATION
./RUN_N092_CHECKS.sh
```

To independently re-execute **all 16,635 native SDK calls** from saved 150-episode action traces:

```bash
cd N092_NEURAL_Q_DISTILLATION
./RUN_N092_NATIVE_REPLAY.sh
```

To run the original 10-family policy experiment again, writing a separate result file:

```bash
cd N092_NEURAL_Q_DISTILLATION
. ./ENV.sh
python -m n092.run --out results/N092_FRESH_RUN.json
```

To run only a few training families:

```bash
cd N092_NEURAL_Q_DISTILLATION
. ./ENV.sh
python -m n092.run --games sc25 vc33 --seeds 76 --out results/N092_FRESH_PILOT.json
```

The new run refuses to overwrite an existing output file; `n092.resume` resumes only incomplete frozen-grid ledgers. The 15 formerly reserved public families are hard blocked. All training and evaluation use native SDK observations/actions; there is no privileged engine-state access.

## Key files

- `N092_RESULTS_20261025.md`: full protocol, native results, loss diagnostics, limitations and interpretation.
- `protocol/N092_FROZEN.json`: fixed action budget, seeds, target definitions, five arms, loss settings and dataset boundary.
- `n092/agent.py`: captures final empirical Level-1 Q after terminal Bellman update but before clearing and handles L2 value initializations.
- `n092/distill.py`: literal tabular-Q MSE teacher/student regression, executed-only sample selection; optional separate discounted-return diagnostic.
- `n092/run.py` and `n092/resume.py`: 10-family native policy runs, no extra probes or stored routes.
- `n092/analyze.py` and `n092/verify.py`: per-game metrics, matched reward milestones, freeze and native-evidence audits.
- `results/N092_TRAIN_10X3X5.json`: all 150 native episodes.
- `results/N092_ANALYSIS.json`: native statistics and confidence intervals.
- `results/N092_REPLAY_1..4.json` and `results/N092_NATIVE_REPLAY.json`: independent action-only SDK verification.
- `baseline_source`, `sdk_runtime`, `n090`, `n091`: unchanged original implementation dependencies and frozen lineage; the N091 root report and README remain verbatim as `N091_REFERENCE_RESULTS.md` and `N091_REFERENCE_README.md`.

**Scope:** development-family empirical results, not a new Kaggle score or private holdout generalization claim.