# Original earlier DQN component study

This directory contains the **actual archived** Wits DQN experiment source,
configuration, component ablations and tests, transferred without modifying
its historical experimental results. The development comparison evaluated
75 game-seed runs per arm with a 600-action upper budget. The four original
ablation arms isolate D14 structured exploration and the dueling head.
This is a distinct protocol from the later DQN/PPO four-game 256-action panel;
these results must not be pooled or described as that panel's chronological
second improvement.

Main neural source is in ../src/; the primary Double DQN/PPO baseline and
selected DQN V1 are separate from this historical component test.
The original 600-action records are preserved under results/ and any
experiment-specific supplementary dependencies must be checked before
claiming end-to-end native SDK replay.
