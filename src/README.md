# Agent implementations

| Agent | Files | Evidence boundary |
|---|---|---|
| Frozen B1/N093 | [source](baselines/frozen_n093.py), [notebook](../notebooks/frozen_n093_submission.ipynb) | Immutable 14-level historical public control |
| N117 local effect-memory | [source](best_public_agent.py), [notebook](../notebooks/local_effect_best_public.ipynb) | 15 levels on historically exposed public games; not independent generalization |
| E126 hybrid | [source](e126_submission_agent.py), [notebook](../notebooks/E126_Kaggle_Candidate.ipynb) | 16 levels for each of three tested policy seeds on exposed games; unsubmitted candidate |

The self-contained submissions deliberately embed frozen components and pretrained weights for offline Kaggle use. Duplication in these generated release files protects exact reproducibility and should **not** be removed by a generic refactor. N117's original modular policy lives at [algorithms/local_effect_policy.py](algorithms/local_effect_policy.py), identical to the archived [experiment copy](../experiments/N117/src/policy.py).

**Editable E126 source of record:** [generator](../experiments/E126/build_candidate.py), [extension template](../experiments/E126/e126_template.py), [manifest](../experiments/E126/manifest.json), and [frozen checkpoint](../assets/e126/effect_prior_s11.pt). Change those only with a new version and native evidence; do not edit the generated agent or notebook without regenerating and verifying hashes.

All native performance figures are previously recorded public SDK outcomes, not official Kaggle/private scores. Source/asset redistribution rights remain subject to review.
