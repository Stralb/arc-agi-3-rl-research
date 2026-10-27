# ARC-AGI-3 research notebooks

| Notebook | Purpose | Status |
|---|---|---|
| [frozen_n093_submission.ipynb](frozen_n093_submission.ipynb) | Original immutable B1/N093 baseline | Preserved control; no independently verified Kaggle record stored here |
| [local_effect_best_public.ipynb](local_effect_best_public.ipynb) | N117 local-effect 15-level research candidate | Public-development result, not a hidden-game score |
| [E126_Kaggle_Candidate.ipynb](E126_Kaggle_Candidate.ipynb) | E126 hybrid click ranking plus pretrained action-effect prior | Deterministically packaged, **not submitted** |

The notebook sources should not be hand-edited independently of their release source. For E126, run `python3 experiments/E126/build_candidate.py` and `python3 scripts/verify_e126_release.py` from the repository root to verify identical generated artifacts.

Use the official ARC-AGI-3 competition framework for any later Kaggle execution. Published public fixtures and previous local SDK metrics do not demonstrate hidden-game generalization or official score. No credentials or private game assets belong in this repository.
