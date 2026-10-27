# E012 decisions

- E012 is a final ablation/consolidation, not another broad search.
- The full candidate is E004 representation + Dueling DQN + full D14 epsilon exploration.
- E010 mechanics and E011 mechanics persistence are excluded because neither improved matched behavior over the E009 control.
- Exact behavioral ties retain the full stack because the retained components entered with prior evidence.
- If an ablation is behaviorally better on the matched E012 evaluation, the run reports `E012_COMPONENT_REVIEW_REQUIRED` rather than silently rewriting the prior evidence.
- No hyperparameter search is performed.
- E012 freezes the DQN baseline before official-style scoring, cross-game holdouts, failure analysis, and advanced specialist architectures.
