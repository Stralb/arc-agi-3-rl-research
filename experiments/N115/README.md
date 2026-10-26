# N115: Native joint-control action-pair research

**Date:** 2026-10-26. **Experimental only, not a Kaggle submission.**

N115 re-tests the deployable *joint-control hypothesis* motivated by N098 using
strictly charged SDK calls on the 25 publicly distributed ARC-AGI-3 games.
Unlike the N098 laboratory shadow oracle, N115 never clones an environment,
performs an uncharged native transition, obtains a hidden state, hardcodes an
N098 oracle route, or dispatches on game ID.

## Original N098 provenance

The embedded N100 archive contains `N098_RESULTS_20261025.md` and original
source. N098's restricted seven-click shadow-oracle win was on **`vc33` Level 2,
not Level 3**. It required 373 additional privileged shadow SDK transitions.
The observation-only N098 route won Level 2 in 10 charged actions; it did not
add any new completed levels. The fixed Level-2 click sequences are not
used by N115's acting policy.

## N115 architecture

- Preserve the original N093 frozen B1/Puct action choice and RL updates on Level 1.
- On Level 2+, every five decisions or after two visually silent actions, allow
  one *two-click* option, capped at 34 proposed pairs per level.
- Choose candidate ordered pairs from the frozen N093 legal-action candidates
  and pretrained PUCT prior. Never consult the game ID, future frames or reward
  beyond actual SDK steps.
- Stage *each actual click* through frozen B1 so native-reward Bellman learning
  remains intact. Recheck legality before each SDK call. After the observed
  option endpoint, update an additional Q(s, pair) via
  `Q <- empirical mean[r_native_1 + gamma*r_native_2 + gamma**2*V(s')]`,
  truncated correctly on native level advancement or GAME_OVER.
- Reject an illegal second click without SDK execution and apply a distinct
  *internal preference penalty* to the pair; never invent a native reward.
- 200 charged native actions per unfinished level, including both clicks of pairs;
  no RESET calls beyond initial environment creation.

Three primary variants: `mixed` (any pair), `cross` (different controls),
`repeat` (same action twice). Controls: `mixed_no_q` (pair Bellman backups
blocked) and `adaptive` (select second step using the *observed* successor).
The adaptive arm is conditional and should not be described as precommitted.

## Reproduction (complete commands)

```bash
cd /path/to/N115_JOINT_CONTROL_NATIVE_20261026
python prepare_runtime.py
python -m pytest -q tests/test_n115.py
python aggregate.py
python verify_release.py
python verify_native_replay.py --arms mixed cross repeat mixed_no_q adaptive --out results/replay_again.json

# Fresh native acting evaluation of the main N115 controller:
python run_native.py --arm mixed --output-dir /tmp/n115_fresh
# Distinct ablations:
python run_native.py --arm cross --output-dir /tmp/n115_fresh
python run_native.py --arm repeat --output-dir /tmp/n115_fresh
python run_native.py --arm mixed_no_q --output-dir /tmp/n115_fresh
python run_native.py --arm adaptive --output-dir /tmp/n115_fresh
```

This requires local NumPy, SciPy, PyTorch, Pytest and the SDK code extracted
from the source archive. No Kaggle authentication or network access required.
Full-run captures use native seed **47** and policy seed **76**.

**Read `FINDINGS.md` before interpreting action counts.** Lower action counts can
mean earlier failure; one public seed cannot measure hidden-set generalization.