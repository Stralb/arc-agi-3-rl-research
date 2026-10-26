# N097B — Terminal Frame Homomorphism (corrected)

This is the complete, offline-native ARC-AGI-3 research experiment derived from the frozen N096 package. It corrects a critical SDK-frame interpretation: reward-producing `step()` calls may return multiple frames, with outgoing Level-1 imagery preceding the incoming Level-2 frame. The *last outgoing* frame is `out.frame[-2]`; the *incoming* frame is `out.frame[-1]`.

Read **N097B_RESULTS_20261025.md** before interpreting the results. The positive terminal geometry on `vc33` is *correlated with* success, but it does not establish an independently causal or sufficient goal or require any particular submit action.

Commands after extraction:

```bash
cd N097_TERMINAL_GOAL_HOMOMORPHISM
./RUN_N097B_CHECKS.sh
./RUN_N097B_NATIVE_REPLAY.sh
./RUN_N097B.sh
```

N097B's main policy is `terminal_geometry`, with `blind_schedule` and `no_symbolic_control` controls. `protocol/N097B_TERMINAL_FROZEN.json` lists the exact 10 allowed and 15 excluded public-game families, seeds, budgets and action semantics. The archived neural checkpoint and B1 Bellman implementation are not modified. No game-ID-dependent goal or action scripts are present. All native reward checks derive from the SDK level counter.

`results/n097b/N097B_10X3X3.json` is the complete new 90-episode action ledger. `results/n097b/N097B_SOURCE_SCREEN.json` contains independently natively verified Level-1 source and terminal-frame metadata. `results/n097b/N097B_ANALYSIS.json` contains matched aggregate statistics.

`n097/` and `results/n097/` preserve the **superseded N097A preflight**, which erroneously assumed the outgoing terminal frame was inaccessible. It was not used as an N097B performance result. Original N096 source and all frozen predecessors remain packaged for verification.