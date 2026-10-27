# Data provenance, confidentiality and license review

**This repository is already public. Review existing content and all future additions for redistribution rights before publishing more.** The supplied ARC-AGI-3 competition rules state that competition data may not be duplicated or redistributed to people who have not agreed to those rules, including supplied executable code. The owner must check whether raw native trajectories, game visuals, SDK fixtures and model parameters are permitted for public posting. The repo package omits all distributed SDK/game binaries, but includes derived native research outputs. Until cleared, prefer a private repository with strictly limited collaborators who have accepted the relevant rules.

- Official ARC-AGI-3 Agents framework, where used, contains code released by ARC Prize under the MIT License (upstream license notice; the SDK and license file are not copied into this repository).. Keep notices if distributing substantial reused material.
- The archived pretrained N093 checkpoint and local agents are from the user's research files. Rights/provenance of constituent model weights and original modules must be confirmed before choosing a final repository-wide open-source license.
- **No new repository-wide license is granted here.** The repo owner can select a license when the underlying rights have been checked.
- No Kaggle API token, `.kaggle` directory, private test responses, private leaderboard results or user credentials should be committed. `.gitignore` excludes common credential paths.
- `data/outputs/` contains native action, frame-hash and research results from historically exposed public games, not independent holdouts.
- Additional original research archives and the offline runtime should be retained privately outside GitHub if their distribution is not authorized.

Source provenance and checksums live in `data/provenance/`. Avoid describing any private Kaggle score until a genuine Kaggle server submission is complete.