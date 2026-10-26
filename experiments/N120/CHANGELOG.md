# Changelog

- Preserved original frozen B1 + N093 notebook/source hashes.
- Reconstructed N093 and N118 archived logged native transition histories without alternative SDK queries.
- Deduplicated 125 replayed episodes to 75 distinct level trajectories, retaining rewards only on native level advancement.
- Implemented state/history `V(s,h)` head and action-conditional `Q(s,h,a)` head, level-bounded discounted MC and fitted TD(lambda) with no game-ID input.
- Implemented family-disjoint model fit excluding `vc33` and `tu93`; validation on three distinct families.
- Tested Level-3-only value priors, state-only null, shuffled-label placebo, unsafe Q-replacement control and winning-level-only online updates.
- Ran native targeted ablations, complete 25-game Monte Carlo public regression, and matched-seed checks, then independently replayed their SDK actions.
- Did not modify or promote the frozen Kaggle notebook. No Level-3 completion was observed.