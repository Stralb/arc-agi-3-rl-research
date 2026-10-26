# Core-Knowledge Prior Ensemble — Evidence and Deployment Decision

## Research question

Can 15 generic object-centric predicates, independent of Level-1 final-state inference and with no LLM/VLM, improve B1/N093's native interactive Level-2 execution?

## Key factual corrections

- Frozen B1 + pretrained N093 PUCT is **not** RTA*. Its source contains tabular Bellman backup and one-step PUCT-like action ranking, without search-tree rollouts.
- The previous N106 audit showed **0/53** rewarding transitions explainable as *one unique exact symbolic primitive* in its tested grammar. That is not a measured "100% false-positive rate" and does not mathematically rule out other valid priors.
- A pre-written geometric objective is neither a reward oracle nor a native-action compiler. A hidden puzzle may have a different goal, and its native controls may not realize the desired transform.
- The "15 most common" phrase lacks a supporting ARC-AGI-3 frequency survey. These are 15 explicit, testable *candidate* predicates.
- Public-development level counts do not guarantee a score on unseen Kaggle games.

## Methods

- Parse observed native 64x64 frame using original N106 object parser (4-connected monochrome regions, modal background, holes, centroids, bounding boxes, containment).
- Evaluate fifteen hardcoded palette/geometry/topology predicates, with nonvacuous applicability checks and explicit unknown status.
- Rotate objectives after 20 action opportunities or early stalling, never claiming an objective is the engine's true goal.
- Observe and record action effects only from paid legal SDK interactions. Zero hypothetical game steps. Never RESET for exploration.
- Strict controller can override PUCT only after two concordant native positive transitions with no contradictory signs; only within near-tied Q actions. ACTION6 mappings are exact-frame-bound; no transferring old absolute click positions to new scenes.
- Probe controller may take at most 24 legal, charged, unverified native actions focused on object centroids/enclosure interiors or available simple controls. Observe the effect and return to B1/PUCT if unsupported.
- Only `levels_completed` advancing supplies Bellman reward. No pseudo-reward from an attractive geometry.

## Verification

| Arm | Native matched development episodes | L1 parity | Level-2 wins at 60-action cap | Heuristic interventions |
|---|---:|---:|---:|---:|
| Frozen B1 + N093 (strict comparison) | 5 | 5/5 | 0 | — |
| Strict priors | 5 | 5/5 | 0 | 0 |
| Frozen B1 + N093 (probe comparison) | 5 | 5/5 | 0 | — |
| Budgeted prior probes | 5 | 5/5 | 0 | 25 |

In the strict comparison, there were 750 SDK actions across 10 episodes; in the probe comparison 712 across 10. The separate agent-framework check passed 75 actions per candidate type. There are no hidden test scores or additional level wins. Please see `results/` for complete action/frame hashes and exact measurements.

## Scientific decision

**Do not replace the already frozen B1 + N093 PUCT submission.** The strict ensemble is safe but inert in the measured native traces. Active probing changes decisions but has no measured completion benefit. The next valid decision requires an actual native Level-2 completion on a genuinely held-out development family within the same budget, not merely improved heuristic geometry scores.