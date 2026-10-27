# RL assignment submission checklist

**Status: not yet a complete Moodle delivery.** This is a transparency and handoff checklist, not an assertion that missing deliverables have been produced.

## Research and assessment evidence

- [ ] Provide the final RLC 2026 formatted report PDF (within the assignment's eight-page main-content limit).
- [ ] Identify and evidence **two distinct qualifying learning algorithms**. The B1/N093/N117/E126 lineage is Bellman/Q-based; the E126 CNN predicts effects and does **not** by itself satisfy a second RL algorithm.
- [ ] Document at least **two substantive improvements for each algorithm**, with controlled ablations and the same evaluation budgets.
- [ ] Include a clear train/validation/held-out protocol, action-count accounting, limitations and reproducibility details. The 25 public games were all exposed during development.
- [ ] Supply final group-member contributions and any required ethics/attribution statements.

## Competition and course submission evidence

- [ ] Verify the nominated notebook with the **official** Kaggle rerun, not just local SDK replay.
- [ ] Record the exact Kaggle code submission/commit ID, date, score and chosen artifact. An earlier 0.33 score is mentioned in the E126 report but its original Kaggle confirmation is not independently stored here.
- [ ] Supply the required Kaggle/Paper Track links or screenshots and class nomination.
- [ ] Package the Moodle submission with the exact final report, evidence and selected executable source; do not mistake GitHub alone for the submission.
- [ ] Review teammate checkpoint distribution permission and ARC Prize competition redistribution restrictions.

## What this repository *does* verify

- Frozen N093/N117 public historical results and source checksums: `python3 scripts/verify_repository.py`.
- E126 checkpoint, generated agent/notebook hashes, public-data arithmetic: `python3 scripts/verify_e126_release.py`.
- Markdown links, SVG integrity and curated regression tests: `python3 -m unittest discover -s tests -v`.
- Offline deterministic E126 packaging: `python3 experiments/E126/build_candidate.py`.

**None of these checks is a new native SDK run, a private leaderboard score, or a complete new-game generalization result.**
