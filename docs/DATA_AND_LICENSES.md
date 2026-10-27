# Data provenance, confidentiality and license review

**This repository is already public.** Before publishing any further material, check the ARC-AGI-3 competition terms and the ownership/redistribution rights of each artifact. The repository excludes the official SDK/game binaries, but includes derived native research output. Do not add native trajectories, game visuals, SDK fixtures or model parameters without checking their permissions; if existing published material cannot be cleared, restrict access while reviewing it.

- The official ARC-AGI-3 Agents framework includes upstream MIT-licensed code. Verify the applicable license and preserve upstream notices if redistributing substantial parts. **No upstream framework license file or SDK source is included in this repository.**
- The archived pretrained N093 checkpoint and local agents are from the user's research files. Rights/provenance of constituent model weights and original modules must be confirmed before choosing a final repository-wide open-source license.
- **No new repository-wide license is granted here.** The repo owner can select a license when the underlying rights have been checked.
- No Kaggle API token, `.kaggle` directory, private test responses, private leaderboard results or user credentials should be committed. `.gitignore` excludes common credential paths.
- `data/outputs/` contains native action, frame-hash and research results from historically exposed public games, not independent holdouts.
- Additional original research archives and the offline runtime should be retained privately outside GitHub if their distribution is not authorized.

Source provenance and checksums live in `data/provenance/`. Avoid describing any private Kaggle score until a genuine Kaggle server submission is complete.

- E126 includes a pretrained action-effect checkpoint derived from teammate research. Retaining its published bytes does not itself establish permission for further redistribution or a new repository-wide license. Confirm the rights holder's permission before a new public release or submission.
