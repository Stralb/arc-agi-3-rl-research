# Results and limitations

## Study context

This is an interactive environment. The agent observes 64×64 native game frames and legal action menus. Its actions are sent to the native SDK and the only external reward is verified advancement of `levels_completed`. It cannot directly write an arbitrary target grid.

## Best observed outcomes on the 25 previously exposed public games

| Policy | L1 | L2 | L3+ | Native charged actions | Caveat |
|---|---:|---:|---:|---:|---|
| Frozen B1 + N093 | 13 | 1 | 0 | 2,982 | N093 no official hidden score |
| Local effect-memory | 13 | 2 | 0 | 2,790 | Extra `tu93` L2 win only; earlier failures elsewhere |

Both preserve 200-policy-actions-per-level stopping logic; game-native terminals may occur sooner. Level-3 native terminal after 75 actions occurred in `vc33` but is not a global 75-action rule. Public level counts are not RHAE.

The native Level-2 winners are `vc33` (both policies) and `tu93` (local-effect only). Native Level-3 completions are zero. In the 25-game comparison, the local candidate's extra `tu93` reward occurs at native action 44. The Q change discourages repeating a small-effect control; it does not establish universal puzzle-object semantics.

## Major architecture findings

1. N093 PUCT is a **one-step action score**; no deep search tree is expanded. Q=1 optimistic initialization can prefer untried actions to unrewarded repeats. The cross-level hypothesis memory exists but is not directly consulted by Level-2 PUCT selection.
2. Local effect-memory can alter the native trajectory and add one rewarded Level-2 completion on an exposed layout. Counting *any* pixel change or shuffling the evidence removes that extra win. A simpler pixel-effect preference also adds it, limiting a unique-mechanism claim.
3. Arbitrary action pairs (N115), symbol/object compilers (N106–N109), grid-program synthesis (N111), learned frame-forward MCTS (N112), top-5 pruning and inherited priors (N113), and checkpoint proxies (N116) yielded **no new Level-3 wins**.
4. Soft/hard visual-effect models, temporal classifiers, delayed credit and episodic return models (N117-effect, N118–N120) do **not** improve the best observed 25-game completion count. Better visual-effect prediction does not imply better native rewards.
5. With `vc33` and `tu93` withheld, the historical episodic-value training corpus has **no rewarded Level-2 or Level-3 trajectories**. A learned deep-level winning value function is consequently unsupported by available positive examples.

## Evaluation threats

- **Every public game has been exposed** during the research; family-disjoint historical splits are no longer untouched holdouts.
- Repeated starting seeds sometimes yield identical initial frames, so multiple policy seeds are not independent environment samples.
- Some smaller experiments used different subsets, budgets or metrics. Do **not** aggregate them into one leaderboard.
- Source/frame-hash replay establishes recorded native results, not future platform compatibility, private score or generalization.
- No current official human-action counts per game are supplied; do not convert raw native completions to RHAE.

**Deployment conclusion:** freeze N093 as the conservative reference; retain the 15-level local-effect variant as the highest observed *public research candidate*, not as an established stronger hidden-game entrant.