# N099 — Precondition Modeling and Goal Regression

**Not a winning zero-shot planner. Do not deploy.**

This standalone package preserves the complete N098 code and evidence and adds the `n099` observation-only conditional effect model, strict L1 identifiability screen, native runner, three-seed five-arm 10-family comparison, full action ledger, honest no-edge ablation, and policy-free native verifier.

All used files are under the root, and `ENV.sh` sets the portable offline SDK/PYTHONPATH environment.

## Commands

```bash
sh RUN_N099_CHECKS.sh
sh RUN_N099_NATIVE_REPLAY.sh --games ar25 cd82
sh RUN_N099_NATIVE_REPLAY.sh --games g50t lp85 ls20
sh RUN_N099_NATIVE_REPLAY.sh --games m0r0 s5i5 sc25 tu93 vc33
python -m n099.run --games vc33 --seeds 76 --arms n099_online n099_no_edge --out /tmp/N099_vc33_check.json
```

The fully frozen trial is `results/n099/N099_10X3X5.json`; the independent accounting is `results/n099/N099_ANALYSIS.json`. The original per-batch native runs and replay logs are also retained. `N099_RESULTS_20261025.md` contains the full scientific report.

## Scientific boundaries

No shadow simulator or hidden state is used by N099. Each test/retest is a charged native SDK action; a successful native level advance is the only reward. The separate inherited `n098/oracle_lab.py` is a **nondeployable** local search reference; N099 never imports it. The strict source-only gate abstains, and the online edge-learning policy ties the no-edge ablation exactly. The 15 public evaluation families previously used for N084 are not evaluated again.

The 150-arm ledger includes **49 new native policy episodes** and **101 inherited N098 fallback-equivalent traces**. Provenance is given per row; inheritance is never represented as a fresh execution.

## Code map

- `n099/causal.py` — conditional effect ledger and candidate observed feature differences.
- `n099/controller.py` — charged intervention policy and provisional goal-regression branch.
- `n099/run.py` — real SDK evaluation on frozen 10-family partition.
- `n099/merge.py` and `n099/analyze.py` — evidence-aware merging and per-family accounting.
- `n099/verify.py` — independent native replay from action requests, no policy instance.
- `n099/identifiability.py` — synthetic logical counterexample illustrating why L1-only source evidence cannot determine an L2 key; not a native ARC result.
- `tests/test_n099.py` — new safety, evidence, control and native integration tests.

Use the unchanged existing pretrained PUCT or frozen B1 for any actual deployment decision, not N099.