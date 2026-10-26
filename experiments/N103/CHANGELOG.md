# N103 change log

1. Precommitted training-family-only native Level-1 collection; epsilon perturbations inside the legal B1 candidate set, strict 90-action cap and no explicit RESET.
2. Collected 60 new fresh-instance attempts (53 native Level-1 rewards), complete public before/after observation arrays, paid action indices and episode hashes.
3. Measured action-path diversity and native-seed failure to generate distinct observed initial layouts.
4. Reused byte-preserved N102 contrastive grammar; introduced independent action-path candidate intersection and held-out seed 279 negative controls.
5. Implemented 64x64 next-frame action-conditioned GRU, matched frame-only model, trained-hidden reset and action ablations; preserved weak native changed-pixel performance as a negative result.
6. Trained a separate synthetic GRU from Level-1 observations/actions; evaluated synthetic in-distribution and out-of-distribution hidden unlock depths.
7. Tested original Bellman controller with three synthetic keys: visual SHA, raw GRU hidden clustering and learned multi-step predictive-response clustering, all with backup toggles and matched action-order/gap/depth variants.
8. Independently audited held-out native GRU cluster collisions against shuffled-cluster fragmentation, documenting the failed native predictive-sufficiency gate.
9. Added 12 deterministic tests, source checksum pinning, complete code, model weights, clusterers, native ledger, raw paired synthetic traces and full scientific caveats.