# N091 — Neural-Anchored Contrastive Exploration

**Complete negative native experiment; not promoted to B1.** A source-only Level-1 immediate-reward discriminator fine-tunes B1's policy head, and a new Level-2 Q initialization replaces B1's optimistic 1.0 with bounded neural action scores. No extra SDK probes, hidden engine state, handcrafted action masks, stored winning routes, new intrinsic rewards, or Level-2 training examples are used.

## Results (native ARC-AGI-3, 10 training families × 3 policy seeds × 5 arms)

| Arm | Native levels | Charged SDK actions |
|---|---:|---:|
| Frozen original B1 | **30** | 3,154 |
| Untrained neural Q anchor | 27 | 3,383 |
| Contrastive TTT, original Q initialization | 27 | 3,028 |
| **Contrastive TTT + neural Q initialization (N091)** | **27** | **3,020** |
| N090 behavioral cloning + neural Q initialization | 27 | 3,254 |

All modified agents lose the 3 `vc33` Level-2 wins and gain no new native rewards. The lower action counts of several weaker variants reflect earlier episode termination rather than greater reward efficiency. All 150 episodes and 15,839 native SDK calls were independently replayed, with full frame-hash and native reward matching. Frozen B1 actions also match the original N090 ledger exactly in 30/30 episodes.

**Important scientific limitation:** a Level-1 successful trajectory supplies only one definitively rewarding action. Other trajectory steps, including steps without reward, may be necessary prerequisites. This experiment trains an *immediate native reward discriminator*, not a valid long-horizon action-value target. The per-candidate neural Q initialization is a bounded **relative rank score**, not a calibrated probability of reward or a measured expected discounted return.

## Instructions

In a fresh terminal after extracting the ZIP:

```bash
cd N091_NEURAL_ANCHORED_CONTRASTIVE
./RUN_N091_CHECKS.sh
```

To independently replay the complete 15,839-action native evidence:

```bash
cd N091_NEURAL_ANCHORED_CONTRASTIVE
./RUN_N091_NATIVE_REPLAY.sh
```

To **re-run** the training-family acting experiment (writes a new output; never overwrites the frozen evidence):

```bash
cd N091_NEURAL_ANCHORED_CONTRASTIVE
. ./ENV.sh
python -m n091.run --out results/N091_NEW_EXECUTION.json
```

To run a faster subtest against the same frozen protocol, restricting to some training families:

```bash
cd N091_NEURAL_ANCHORED_CONTRASTIVE
. ./ENV.sh
python -m n091.run --games ar25 sc25 vc33 --seeds 76 --out results/N091_DEBUG_EXECUTION.json
```

## Files

- `n091/learning.py`: actual native reward discrimination and differentiable, contrastive policy-head update.
- `n091/agent.py`: subclass of frozen B1. New Level-2 nodes and progressively widened actions are initialized with the neural anchor; unchanged B1 Bellman updates and legal candidates.
- `n091/run.py`, `n091/resume.py`: official SDK acting evaluation, with the reserved 15 public families rejected by protocol.
- `n091/analyze.py`, `n091/verify.py`: paired reward/action accounting, game-cluster bootstrap, outcome and provenance checks.
- `results/N091_TRAIN_10X3X5.json`: immutable 150-episode native action ledger and actual update diagnostics.
- `results/N091_NATIVE_REPLAY.json`: action-only independent native SDK replay results.
- `results/N091_ANALYSIS.json`: independently recomputed paired comparisons and uncertainty.
- `results/N091_BATCH_*.json`: source-evaluation progress snapshots, preserved for audit.
- `protocol/N091_FROZEN.json`: tested parameters, training families, controls and evaluation limits.
- `N091_RESULTS_20261025.md`: research report and limitations.
- `baseline_source`, `sdk_runtime`, `src`, `n090`, `results/N090_*`: unchanged N090 reference implementation/SDK and historical evidence, except the former root README which is preserved as `N090_REFERENCE_README.md`.

The N090 original manifest and original `VERIFY_MANIFEST.py` are *historical release artifacts*. They cannot be used as a complete-package inventory after adding N091 files; the N091 verification script instead checks the inherited members against their original hashes and checks the complete N091 release inventory separately.

**B1 deployment and model checkpoint remain untouched.** The previously used 15-family public evaluation partition was not run. No private Kaggle benchmark claims or submissions.