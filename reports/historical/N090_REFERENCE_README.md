# N090 — Neural Prior Test-Time Training (ARC-AGI-3)

**Validated offline study, not a deployed agent.** Three matched arms on 10 public training game families, three policy seeds each: frozen B1; B1 with Level-1 behavioural-cloning fine-tune; and B1 with BC plus coarse next-observation prediction. No heldout 15-family access, no privileged game state, no internet, no teacher actions, no Q-table transfer.

**Result:** all three policies complete 30 native levels. They reach the exact same 30 native reward milestones at exactly the same charged SDK action indices. BC increases total calls from 3,154 to 3,200; BC+aux increases them to 3,196; those extra calls occur after existing rewards. New weights are trained in 27/30 episodes. See [N090_RESULTS_20261025.md](N090_RESULTS_20261025.md).

## Dependencies

Python, NumPy, SciPy, PyTorch (CPU works), pytest. Bundled `sdk_runtime` contains the native SDK and the 25 public offline-game resources, **used exclusively via the public Arcade interface**. The bundled `baseline_source` includes B1's frozen network and checkpoint.

## Commands

Run all commands in a fresh terminal with the ZIP extracted:

```bash
cd N090_TEST_TIME_PRIOR
./RUN_N090_CHECKS.sh
```

The full historical native replay is available separately because it repeats 9,550 actions:

```bash
cd N090_TEST_TIME_PRIOR
./RUN_N090_NATIVE_REPLAY.sh
```

To produce fresh episodes *without* overwriting the frozen evaluation output:

```bash
cd N090_TEST_TIME_PRIOR
. ./ENV.sh
python -m n090.run --out results/N090_REGENERATED.json
```

All ten training families, three seeds and three arms are selected by default; the runner rejects games outside the frozen training split.

## Layout

- `n090/ttt.py` — Level-1 on-policy dataset assembly, BC and coarse successor auxiliary gradient losses.
- `n090/run.py` — native SDK episode loop using the **unchanged original B1 Bellman agent**.
- `n090/analyze.py` — paired game/seed analysis.
- `n090/verify_native.py` — independent action-only SDK replay without loading the acting neural model.
- `n090/verify_results.py` — fail-closed source/metric/episode integrity check.
- `protocol/N090_FROZEN.json` — fixed evaluation specification.
- `results/N090_TRAIN_10X3.json` — all 90 native trajectories and parameter update diagnostics.
- `results/N090_ANALYSIS.json` — paired reward, action, and decision-divergence audit.
- `results/N090_REPLAY_*.json` — independently reproduced native action evidence.
- `baseline_source`, `sdk_runtime`, `src`, `replay_native.py` — bundled frozen dependencies.
- `B1_FROZEN_REFERENCE.json` — historical B1 ledger reused for independent control comparison.

**Scientific caveat:** The auxiliary model predicts an 80-D coarse observation summary, not a full next frame. A Level-1 winning trace does not establish that every action in it was useful. Existing frozen B1's checkpoint was pretrained using public Level-1 examples from all 25 game families; the 10-family experiment is a development evaluation, not an unseen benchmark.