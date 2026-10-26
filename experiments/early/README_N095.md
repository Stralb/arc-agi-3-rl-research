# N095 — Contrastive Procedural Synthesis

A reproducible, native SDK experiment building small symbolic `WHILE/UNTIL` programs from *observed Level-1 B1 transitions*. Native reward means only actual level advancement. **Result: no confirmed procedural transfer, no new native win.**

## Frozen design

- `n095/synthesis.py`: transition ledger, exact frame-revisit/no-effect evidence, non-differentiable role/predicate AST enumeration, guarded executor. The AST uses no stored click coordinates or raw color labels.
- `n095/agent.py`: integrates the AST via N094's existing pre-emption interface; fallback is frozen N093 pretrained PUCT and underlying unchanged tabular B1.
- `n095/run.py`: paired native episodes; blocked 15-family evaluation split; 200-step game cap; native SDK reward only.
- `n095/screen.py`: independently replays all 27 winning Level-1 sources, and attempts synthesis **without Level-2 data**. Three unsuccessful `s5i5` source episodes are correctly marked unavailable.
- `n095/merge.py`: reconstructs the complete 60-arm ledger from **40 fresh native policy episodes** plus **20 explicitly labelled inherited fallback-equivalent N093 controls**. Inherited controls are never counted as new policy executions.
- `n095/verify.py`: independent SDK replay using recorded actions only, not the acting neural/symbolic policy.
- `n095/analyze.py`: reproduces all numerical totals from the frozen action ledgers.
- `results/N095_SYMBOLIC_SOURCE_MATRIX.json`: post-evaluation native-replayed object-property transition matrices (30 attempts, 527 transitions); not used to fit the policy.
- `results/N095_SCREEN.json`: human-inspectable per-family ledger, including all actual source event counts and induced `vc33` exploratory AST.
- `results/N095_10X3X2.json`: comprehensive native action/reward/frame-hash ledger; `results/N095_ANALYSIS.json`: analysis.
- `protocol/N095_FROZEN.json`: complete preregistered evaluation constraints and thresholds.
- `N095_RESULTS_20261025.md`: full scientific results and caveats.

## Reproduce from a fresh extraction

```bash
cd N095_CONTRASTIVE_PROCEDURES
sh RUN_N095_CHECKS.sh
sh RUN_N095_NATIVE_REPLAY.sh
```

For an optional **new** matched experiment (does not overwrite archived runs):

```bash
cd N095_CONTRASTIVE_PROCEDURES
sh RUN_N095.sh
```

Use `sh` on a freshly extracted ZIP because standard ZIP extraction may not restore executable file permissions. The native replay may need additional wall-clock time. Its three commands execute sequentially, verifying all 7,054 actions and 60 episodes.

**Important:** The exact action trace must not be used as privileged supervision for the agent; replay reads it only for independent verification. The 15 previously evaluated public game families are excluded, not fresh holdouts.