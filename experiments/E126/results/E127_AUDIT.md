# E124-E126: Observation-Conditioned Click Exploration

**Status:** native-SDK evaluation completed; no Kaggle submission.

The native checkpoint and original N117 agent were not modified. SHA256 0663845070e47a053076db54243c3445921a06b4bf0908b7b233c263da423bfa.

## Main design

**E124:** prune large likely background candidates, replace centroid with an edge point (pilot only), estimate color rarity and empirically local click effects, or follow a click with a primitive action.

**E125:** transfer the teammate pretrained CNN effect prior only when ACTION6 is legal, directional keys 1-5 are not legal, and >=80% of the observed 64x64 image has one color. Compare random weights and deterministic visual salience through the identical gate.

**E126:** fuse E124 click-contingency outside the gated states with E125 pretrained effect prior in those gated states; compare random-weight and salience-only hybrids.

All interventions use only the official observation and legal action interface. N117 Bellman targets and frozen model unchanged.

## Three-seed local SDK outcomes

| Study | Seed | Arm | L1 | L2 | Total levels | Mean native SDK score (0-100) |
|---|---:|---|---:|---:|---:|---:|
| E124 | 76 | baseline | 13 | 2 | 15 | 2.093242 |
| E124 | 76 | prune_bg | 13 | 2 | 15 | 2.088488 |
| E124 | 76 | prune_broad | 13 | 2 | 15 | 2.088488 |
| E124 | 76 | contingency | 13 | 2 | 15 | 2.127502 |
| E124 | 76 | selection_chain | 13 | 2 | 15 | 2.089970 |
| E124 | 77 | baseline | 12 | 2 | 14 | 2.054775 |
| E124 | 77 | contingency | 13 | 2 | 15 | 2.123161 |
| E124 | 78 | baseline | 13 | 2 | 15 | 2.096435 |
| E124 | 78 | contingency | 13 | 2 | 15 | 2.129626 |
| E124_ablation | 76 | contingency | 13 | 2 | 15 | 2.127502 |
| E124_ablation | 76 | rarity_only | 13 | 2 | 15 | 2.127502 |
| E124_ablation | 76 | effect_only | 13 | 2 | 15 | 2.127502 |
| E124_ablation | 76 | random_bonus | 12 | 2 | 14 | 1.952195 |
| E124_ablation | 77 | rarity_only | 12 | 2 | 14 | 2.054775 |
| E124_ablation | 77 | effect_only | 13 | 2 | 15 | 2.096993 |
| E124_ablation | 78 | rarity_only | 14 | 2 | 16 | 2.162342 |
| E124_ablation | 78 | effect_only | 13 | 2 | 15 | 2.129626 |
| E125 | 76 | baseline | 13 | 2 | 15 | 2.093242 |
| E125 | 76 | sparse80_trained | 14 | 2 | 16 | 2.177258 |
| E125 | 76 | sparse80_random | 13 | 2 | 15 | 2.093242 |
| E125 | 76 | sparse80_salience | 13 | 2 | 15 | 2.093242 |
| E125 | 76 | sparse70_trained | 13 | 2 | 15 | 2.034401 |
| E125 | 77 | baseline | 12 | 2 | 14 | 2.054775 |
| E125 | 77 | sparse80_trained | 13 | 2 | 15 | 2.155556 |
| E125 | 77 | sparse80_random | 12 | 2 | 14 | 2.054775 |
| E125 | 77 | sparse80_salience | 12 | 2 | 14 | 2.054775 |
| E125 | 78 | baseline | 13 | 2 | 15 | 2.096435 |
| E125 | 78 | sparse80_trained | 14 | 2 | 16 | 2.207546 |
| E125 | 78 | sparse80_random | 13 | 2 | 15 | 2.096435 |
| E125 | 78 | sparse80_salience | 13 | 2 | 15 | 2.096435 |
| E126 | 76 | baseline | 13 | 2 | 15 | 2.093242 |
| E126 | 76 | contingency_only | 13 | 2 | 15 | 2.127502 |
| E126 | 76 | hybrid_trained | 14 | 2 | 16 | 2.211518 |
| E126 | 76 | hybrid_random | 13 | 2 | 15 | 2.127502 |
| E126 | 76 | hybrid_salience | 13 | 2 | 15 | 2.127502 |
| E126 | 77 | baseline | 12 | 2 | 14 | 2.054775 |
| E126 | 77 | contingency_only | 13 | 2 | 15 | 2.123161 |
| E126 | 77 | hybrid_trained | 14 | 2 | 16 | 2.223942 |
| E126 | 77 | hybrid_random | 13 | 2 | 15 | 2.123161 |
| E126 | 77 | hybrid_salience | 13 | 2 | 15 | 2.123161 |
| E126 | 78 | baseline | 13 | 2 | 15 | 2.096435 |
| E126 | 78 | contingency_only | 13 | 2 | 15 | 2.129626 |
| E126 | 78 | hybrid_trained | 14 | 2 | 16 | 2.240737 |
| E126 | 78 | hybrid_random | 13 | 2 | 15 | 2.129626 |
| E126 | 78 | hybrid_salience | 13 | 2 | 15 | 2.129626 |

## Mechanism ablation and validity

The E124 rarity-only and effect-only arms both reproduce the single-seed lf52 action-efficiency result. Therefore the result is not uniquely attributable to causal learning; a matched random bonus is an additional control.

The E125 pretrained sparse-click transfer produces the missing s5i5 win on 3/3 policy seeds without breaking existing public-game completions. The identically gated random and salience controls do not.

The E126 combined policy produces the s5i5 result and can improve other exposed games through E124 ranking. This is a post hoc development result only.

Three-seed game-cluster mean score differences are descriptive:

- E125 {'mean': 0.09863604, 'low': 0.0, 'high': 0.29590813}
- E126 {'mean': 0.14391524, 'low': 0.0, 'high': 0.38646652}

## Methodological limitations

The public games have repeatedly informed model development. The 80% sparse-scene threshold is susceptible to visually identifying the s5i5 family, even without explicit game names. Evidence does not establish generalization to hidden competition games.

No Kaggle notebook, agent checkpoint, or official 0.33 submission was modified.

See per_game.csv, paired_changes.csv, and RESULTS.json for all scores, regressions, frame-change validation, and provenance.
