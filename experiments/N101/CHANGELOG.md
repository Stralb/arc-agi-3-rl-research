# Change log

- Stopped N100 cluster checks and vc33 action experiments. Recovered actual N100 2026-10-25 interim archive and pinned source SHA.
- Diagnosed N101 rolling-history graph-key drift, missing complete-action Bellman coverage, exclusion of self-loop costs, no backward value propagation, and inconsistent learned-V scoring.
- Added `BellmanRTAFix` as separate source module, preserving originals for a controlled ablation; added explicit observation-alias flags and `GAME_OVER` no-reward fix.
- Added deterministic trap tests proving Bellman update changes decisions; new 96-case procedural matched on/off ablation and old 7x7 negative control.
- Native-replayed all 27 archived non-vc33 N093 Level-1 sources (518 actions, all pre/post hashes checked); recovered 24 real outgoing terminal frames and 3 s5i5 no-win sources.
- Reproduced exact N097B masked terminal induction on the eight rewarded seed-76 source traces and separately ran a no-mask diagnostic on all 24 terminal traces.
- Compared the correct last outgoing frame `frame[-2]` with reward `frame[0]`; found four genuine non-vc33 visual mismatches.
- Evaluated a fixed colour/geometry/topology feature grammar across all sources; added an exhaustive nonreward pseudo-terminal control after an initial three-checkpoint sample missed a stronger m0r0 pseudo-signal.
- No new controller number, no Level-2 native performance claim, no pretrained checkpoint changes.