# GitHub distribution coverage and known gaps

This repository is intended as a **curated, auditable public research record**, not a claim that every underlying native trace and third-party asset has been published.

## Present

- Original frozen N093 agent and original Kaggle-format notebook.
- Experimental 15-level local-effect agent and notebook.
- Native controller implementations N101–N120 where present.
- N108–N120 findings and key public per-family comparison tables.
- Reproducible SVG plots of public outcomes.
- Original N114 full 25-game native runner and parity verifier, plus N117 local-effect native runner, event-level policy module, replay verifier and test source. Execution requires separately authorized SDK archives and original data.
- Source-defined constraints, caveats and rollback guidance.
- E126 Kaggle-format candidate and its self-contained source, teammate effect-model checkpoint, deterministic generator, per-seed public controls and audit summaries. Original detailed E127 episode traces and cluster cache are not fully hosted.

## Different archival state

The separately prepared offline archival ZIP contained 1,355 entries, including 921 `.gz` files and extensive native trace/frame data. GitHub's present tree does **not** contain all those bytes, nor should they be silently inferred from a report.

The public repository omits or reduces original game-specific native screenshots, official SDK/game assets, unreviewed third-party code, repeated raw action/frame archives, model checkpoints and redundant experiment logs. N114 and N117 runner source is now published, but neither constitutes a fresh rerun without the original owner-held SDK. Their distribution rights and data provenance should be reviewed first.

A file hash is evidence only when the corresponding file is actually present. `scripts/verify_repository.py` checks the **published subset**, not all 1,285 checks from the offline archival ZIP.

## Reproduction status

- Historical public 25-game level counts are compared against committed tables.
- Local snapshot verification is **not** a fresh native run on Kaggle.
- No private leaderboard score, independent hidden-game generalization or Level-3 native win is claimed.
- `vc33` and `tu93` are historically exposed, so repeated policy seeds on the same starting layout are not independent test games.

## Unexecuted directive

N110 relational object resolution was **proposed but not verified as an executed native experiment** in this conversation. It must not be assigned fabricated results.
