# Research experiments — index

**Start with [the research summary](../reports/RESEARCH_SUMMARY.md) and [experiment findings catalog](../reports/EXPERIMENT_CATALOG.md).** The agents evaluated for the main snapshot are [the frozen N093 reference](../src/baselines/frozen_n093.py) and [the local-effect candidate](../src/best_public_agent.py).

| Group | Purpose |
|---|---|
| [N092](N092/README.md), [N093 frozen](N093_frozen/README.md), [early notes](early/) | Historical baseline selection and first experiments |
| [N101–N109](N101/README.md) | Bellman, affordance, representation, objects and options; each numbered folder has its own README |
| [N111–N113](N111/README.md) | Program and forward-model planning, ranking and negative controls |
| [N114](N114/README.md) | Historical native 25-game baseline runner and integrity verifier |
| [N115–N116](N115/README.md) | Joint actions and checkpoint studies |
| [N117](N117/README.md), [effect-prior audit](N117_effect_prior/README.md) | Native local-effect experiments, replay checks and controls |
| [N118](N118/README.md), [N119](N119/README.md), [N120](N120/README.md) | Temporal prediction, delayed credit and episodic value studies |

The folders retain experiment-specific source, parameters and historical instructions. **They are not independent, ready-to-run packages:** many older READMEs describe `inputs/`, `results/`, scripts and SDK files retained only in the separate, owner-held offline archive. The documented N114/N117 subset can be staged using [authorized reproduction instructions](../docs/REPRODUCIBILITY.md). Do not interpret historical failures as missing results or an independent hidden-game evaluation.
