# N096 — Epistemic Boundary Probing

Verified native ARC-AGI-3 programmatic action-hypothesis experiment with unchanged original B1 and PUCT fallback. See **N096_RESULTS_20261025.md** for the complete research account.

**Outcome:** 30 completed levels per arm; `vc33` exact count hypothesis conditionally falsified, but no supported geometric/submitter stopping rule. The 12-probe exploratory arm reaches the Level-2 reward at action 22 instead of PUCT's 30, and an outcome-blind matched schedule yields the identical action/frame trajectory; therefore no information-gain benefit has been demonstrated.

**Scientific boundary:** N096 cannot prove a specific unseen game's mechanics from one Level-1 demonstration. All ten tested families are already used development families. Fifteen previously evaluated public families remain excluded.

## Reproduction commands

```bash
cd N096_EPISTEMIC_BOUNDARY
./RUN_N096_CHECKS.sh
./RUN_N096_NATIVE_REPLAY.sh
./RUN_N096.sh
```

- `n096/hypotheses.py`: explicit count/effect/geometry/submit hypotheses and observation-conditioned stage transitions.
- `n096/agent.py`: charged, legal epistemic actions with matched Q and PUCT visit counters.
- `n096/run.py`: fresh native ARC-AGI-3 evaluation driver, frozen split guard.
- `n096/source_screen.py`: Level-1-only source extraction using native action replay; original frozen traces verified by hash.
- `n096/merge.py`: 46 fresh N096 episodes plus 74 explicit frozen-PUCT fallback-equivalent records; no invented fresh runs.
- `n096/analyze.py`, `n096/check.py`, `n096/verify.py`, `n096/verify_lineage.py`: analysis, forensic integrity and independent SDK replay.
- `results/n096/N096_10X3X3.json`: 120 fully described policy-arm traces.
- `results/n096/N096_SOURCE_SCREEN.json`: source-only pre-Level-2 induction on all 10 families × 3 seeds.
- `protocol/N096_FROZEN.json`: complete policy/action boundaries and sealed experiment configuration.
- `tests/test_n096.py`: 13 new mechanism/integrity checks, plus predecessor suites.

All exposed native rewards come from SDK `levels_completed`. There is no Kaggle submission or private benchmark access.