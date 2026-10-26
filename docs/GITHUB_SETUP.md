# Live repository workflow

This repository is already hosted at https://github.com/Stralb/arc-agi-3-rl-research and is connected for direct GitHub edits.

The repository is currently **public**. Before publishing more data, check `DATA_AND_LICENSES.md` and `REPOSITORY_COVERAGE.md`.

Run the offline checks:

```bash
git clone https://github.com/Stralb/arc-agi-3-rl-research.git
cd arc-agi-3-rl-research
python3 scripts/verify_repository.py
python3 -m unittest discover -s tests -v
```

Never commit Kaggle authentication tokens or private ARC-AGI-3 game assets. Native reruns require separately authorized SDK/game installation; source-only checks do not validate the behavior of private leaderboard submissions.
