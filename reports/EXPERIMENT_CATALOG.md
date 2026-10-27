# Research index and reading order

The archive preserves every major experiment and failure analysis without presenting distinct test protocols as directly comparable. Read each corresponding full report in `reports/findings/` or `reports/historical/`.

| Series | Question | Observed result |
|---|---|---|
| N090–N100 | Initial RL, PUCT, RTA and oracle-diagnostic ancestry | N093 pretrained PUCT retained as frozen baseline. N098's seven-action privileged sequence was for `vc33` **Level 2**, not a Level-3 completion. |
| N101 | Bellman/search identifiability audit | Search/backup assumptions investigated; no promoted deep-level gain |
| N102 | Affordance and contrastive goals | Insufficient action grounding |
| N103–N104 | Frame and action-latent prediction | Predictive pixels did not translate to native wins |
| N105 | Native macro-actions | No additional Level-2 reward |
| N106–N107 | Object parser / O-DSL / SMDP options | No licensed native options producing additional wins |
| N108–N109 | UI grammar / deictic object matching | No proven transferable native Level-2 option |
| N111 | Global grid DSL | 0/9 exact short programs; not an interactive executor |
| N112 | Forward model / internal MCTS | 0 trusted new plans and no additional wins |
| N113 | Top-5 pruning / inheritance / alignment | `vc33` Level 3: no native completion |
| **N114** | **25-game full available public benchmark** | **13 L1, 1 L2, 0 L3** |
| N115 | Native joint-control bi-grams | No gain over the 14-level frozen result |
| N116 | Object-derived checkpoint reward | Zero reliably licensed progress checkpoints |
| **N117 — deep RL audit** | **Cross-level, local-effect, curiosity and skill ablations** | **Best observed 13 L1, 2 L2, 0 L3** |
| N117 effect-prior | Soft and hard action-change filtering | No additional win beyond existing 15-level candidate |
| N118 | History-conditioned effect predictions | Better Brier/log-loss but no reward improvement |
| N119 | Delayed credit and terminal-risk proxies | Trajectory changes, no extra level rewards |
| N120 | Monte Carlo return and TD(lambda) value networks | No Level-3 win; insufficient higher-level positive training labels |
| **E124–E126** | **Observation-conditioned click ranking and transferred pretrained effect prior** | **16 levels for each of three public seeds vs 15/14/15 N117; no L3 or hidden-game evidence** |

`N117` is used here as a repository catalog label for the **2026-10-26 deep-RL audit**; the archived directory does not claim this was an official N117 experiment number. This label is organizational, not an attempt to rewrite experiment history.

For provenance and individual protocol, inspect the unmodified original reports rather than relying only on this summary.
