# Original archive inventory

The SHA-256 manifest at [`data/provenance/ARCHIVE_SHA256_MANIFEST.json`](../data/provenance/ARCHIVE_SHA256_MANIFEST.json) records **25 separately retained original research ZIPs**, including the frozen N093 notebook, later experiment packages, and the complete offline research repository.

These hashes were calculated against the **original archive bytes** and allow users who already possess the corresponding archives to verify integrity:

```bash
sha256sum FROZEN_B1_PRETRAINED_PUCT_KAGGLE_20261025.zip
sha256sum N120_EPISODIC_VALUE_TD_LAMBDA_20261026.zip
```

**Archive inventory does not equal hosted archive content.** The ZIPs are not present in the public repository; several contain official SDK assets, game snapshots and full native interaction recordings whose rights must be reviewed before wider redistribution.

The GitHub version carries the self-contained agents, published public-result CSVs, supported SVG graphics and experiment reports. The separate archive manifests retain a verifiable path to the larger evidence set without falsely claiming those bytes have been pushed.

No private leaderboard or hidden-test score has been established.
