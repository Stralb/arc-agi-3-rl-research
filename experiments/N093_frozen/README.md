# Frozen B1 + N093 pretrained PUCT (Kaggle deployment)

## Exactly what is in the release

- `submission.py`: **single-file ARC-AGI-3 agent**, including the unmodified
  1.3 MB pretrained checkpoint encoded as a self-verifying payload.
- `submission.ipynb`: Kaggle **notebook submission**, built using the supplied
  `ARC-AGI-3-Kaggle-Starter-main` builder in **CPU**, **offline** mode.
- `agent/my_agent.py`: exact copy of `submission.py` for the starter workflow.
- `notebooks/submission.ipynb`: same ready notebook for the starter workflow.
- `original_source/`: exact N093/portable B1 original code and the N093 frozen
  protocol/results report (not generated agent improvements).
- `evidence/`: targeted exact native source-trace replay results.
- `tests/`: portable smoke/trace regression scripts; to rerun with the
  original frozen offline SDK, extract the original `N100_ACTIVE_FSM_20261025.zip`
  alongside this release and set `N100_SOURCE_ROOT` if its folder is elsewhere.

## Controller behavior

- Level 1: original frozen B1 empirical Bellman Q, Q-initialization **1.0**,
  original pretrained neural tie-breaker and candidate generation.
- Level 2 and later: original B1 updates and candidate set, but rank with
  `Q_B1(s,a) + 0.10 * softmax(logits(s,a)/2)/(1 + N(s,a))`.
- No imitation updates, hindsight training, RTA*, GRU or new learned weights.
- Stop the current game when **200 policy actions** have been taken on the
  current level without advancing. Do **not** issue a full-game RESET at the
  limit. A successful 200th action initializes a fresh next-level budget.
- Every chosen action comes from native available actions. ACTION6 is
  coordinate-bounded (0..63), and coordinates are kept agent-local so parallel
  agents cannot overwrite the shared GameAction enum's mutable data. The SDK's `levels_completed` is the only reward.
- `GameAction.RESET` can occur only for initial `NOT_PLAYED` initialization,
  not for search, scouting or scorecard resets.

## What is verified (and what is not)

- Pretrained checkpoint exact SHA-256:
  `42996eed8eea3581971b054a499cf9063d82862147222d8d79c6c0d632e6c5f3`.
- Core action, learned-Q, and level state parity against original N093 code
  on 70 native actions from a public `ar25` episode.
- Exactly **122/122** native action+frame+reward steps match the original N093
  archived `sc25` and `ls20` policy-seed-76 traces.
- Real SDK + Agent framework `g50t` smoke run: 147 native actions, with legal
  control selection and no programmatic full-game resets.
- Startup, 200-decision stopping, 200th-action-level-reward edge cases
  and cross-agent ACTION6 coordinate isolation tested and passed.
- Original N093 held-out-private score: **unknown**. The old *public development*
  10-family x 3-policy-seed study reports **27 Level-1 plus 3 Level-2**
  completions for pretrained PUCT, and does **not** establish this as a
  tournament-performance upper bound. The full 30-episode release replay was
  not completed in this environment.

## Submitting to Kaggle

The supplied Kaggle rules require a **Notebook**, not a raw Python script.
Upload `submission.ipynb` as a Kaggle Notebook attached to the **ARC Prize
2026 – ARC-AGI-3** competition. Keep internet access disabled. During a
competition rerun, the notebook installs the wheel from competition input,
registers this MyAgent in the supplied agent framework, and invokes
`python main.py --agent myagent`. During a save-and-run commit, the notebook
uses the official starter's placeholder parquet pattern; the gateway produces
actual `submission.parquet` during the competition rerun.

To use the starter's command-line workflow, update the placeholder user name
in `notebooks/kernel-metadata.json` and supply your own Kaggle API token in
`.kaggle/access_token` locally, then run `make setup`, `make notebook`,
`make submit`, and `make status` from this extracted directory.
**Never put a Kaggle token in a notebook or submission archive.**

The uploaded competition page specifies October 26, 2026 for entry/merger,
and November 2, 2026 for final submission (11:59 PM UTC), rather than
October 26 as final submission deadline. Verify in Kaggle before submitting.

## Research boundaries

The frozen pretrained checkpoint was trained on historical public-family
material and is not a family-disjoint evaluation checkpoint. The code
contains no family-name rules and only uses public SDK observations/actions.
`N093` calls this a one-step PUCT-style ranking mechanism, **not MCTS**.
The rules allow freely available external pre-trained models, but users remain
responsible for verifying platform execution and competition eligibility.