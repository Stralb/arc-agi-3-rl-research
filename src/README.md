# Agent sources

- [`best_public_agent.py`](best_public_agent.py): the **best measured public-development result**, with 13 L1, 2 L2 and 0 L3+ completions across 25 historically exposed native SDK games. This single-file entry point embeds the experimental local effect-memory action selector and pretrained prior. It is **not established to generalize to hidden games**.
- [`baselines/frozen_n093.py`](baselines/frozen_n093.py): immutable B1 tabular RL + pretrained N093 PUCT conservative control, with 13 L1, 1 L2 and 0 L3+ public completions.

The original experimental package also contained a modular `algorithms/local_effect_policy.py`, which has **not been published separately here**; use the complete single-file experimental agent above. No module absent from this directory is required for the self-contained source to parse.

The original and experimental [Kaggle-format notebooks](../notebooks/README.md) remain separate. The 14/15 level counts are not official Kaggle scores or human-normalized RHAE. No native Level-3 success was demonstrated.
