# E126: What changed when click selection learned from observation?

**Research-only development result — no official Kaggle submission.**

## Hypothesis

Can observation-conditioned local action-effect feedback and a
pretrained action-effect prior improve a frozen ARC-AGI-3 exploration
agent without adding task-specific solutions, an LLM or privileged state?

## Controlled comparison

The frozen N117 agent is the baseline. E124 tests background removal,
click-contingency / rarity bonuses and short action chaining. E125
transfers the teammate CNN only into sparse click-only scenes. E126
combines contingency ranking outside these scenes with the trained
prior inside them. Random-weight and visual-salience controls use the
same gating rule. A wider 70% gate was tested and rejected after
regressing a public-game completion.

| Policy seed | Frozen completed levels | E126 completed levels | Frozen SDK mean | E126 SDK mean |
|---|---:|---:|---:|---:|
| 76 | 15 | 16 | 2.093242 | 2.211518 |
| 77 | 14 | 16 | 2.054775 | 2.223942 |
| 78 | 15 | 16 | 2.096435 | 2.240737 |

Mean across three seeds: frozen N117 **2.081484**, E126 **2.225399**,
difference **+0.143915 SDK points**, about **+6.9% relative**.
These are on the **local public SDK** (0–100 scale), NOT the hidden
competition leaderboard score of 0.33.

The trained prior adds the public **s5i5** completion in every original
seed. Local action ranking recovers **lf52** for seed 77. No previously
completed family regressed in these runs.

The four predeclared additional policy/native seed pairs (79/48, 80/49,
81/50, 82/51) gave SDK deltas of **+0.134875, +0.037532, +0.033191,
+0.128988**; level deltas **+1, 0, 0, +1**. No lost completions.
Changing the native seed did not change any initial game image.

## Mechanistic limitations

The E124 rarity-only and local-effect-only ablations can reproduce
the first seed's score advantage independently. Hence that
advantage is **not attributable uniquely to causal learning**.
The effect prior was pretrained to predict action effects; it does
not establish that online RL received more reward information.
The advantage in aggregate is concentrated in a small number of
familiar public game families.

## Evidence quality and acceptance gate

E127 checked 1,125 native episodes and 125,220 charged actions.
The packaged E128 submission reproduced all 75 E126 reference
episodes and all 8,632 actions, frames, and rewards exactly.
Checksums confirm the original teammate pretrained model.
See experiments/E126/results and the original 8.75 MB trace archive.

These games and the sparse threshold informed development, so this
is **not an independent generalisation test**. A descriptive
game-cluster bootstrap interval for improvement includes zero.
A better public SDK score need not beat 0.33 on hidden Kaggle games.
The candidate should be retained **alongside**, not silently
replace, the previously submitted 0.33 baseline.

The notebook is a reproducible candidate for **later optional**
submission, not evidence of a completed new competition run.
