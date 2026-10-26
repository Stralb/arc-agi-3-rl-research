# Architectures

## Frozen B1 + N093 (immutable control)

1. Observe public native 64×64 frame and legal action menu.
2. Level 1: B1 optimistic empirical Q (`Q_initial=1.0`, `gamma=0.985`) with frozen neural prior for ties/grounding.
3. Level 2+: rank candidates by `Q(s,a) + 0.10 * P(a|s)/(1+N(s,a))`, with prior logits softmax temperature 2.0.
4. Update Bellman value exclusively on real SDK `levels_completed` advancement; stop at 200 selected actions on any non-advancing level, or earlier on native terminal.
5. Cross-level hypothesis memory is stored, but N093 Level-2 action ranking does not consume it directly.

This is **one-step PUCT-style action ranking, not MCTS**. It cannot simulate effects for free.

## Best measured public variant: local effect-memory

- Preserves frozen Level-1 behavior and pretrained model.
- For Level 2+, adds a bounded confidence-weighted local action-descriptor effect term to the N093 action score.
- The inherited source defines meaningful visible effects as `changed_pixels >= 4` (approximately); repeated tiny effects can lower a control's preference relative to alternatives.
- No imaginary reward, object semantics, control macros or native reset.

This achieved one additional `tu93` Level-2 completion on a historically exposed layout. It has **not** achieved Level 3 or demonstrated holdout generalization.

## Experimental branches

All other branches under `experiments/` are archived research variants, not default imports, and many require restored original `inputs/` and public SDK runtime. See full findings and original scripts.
