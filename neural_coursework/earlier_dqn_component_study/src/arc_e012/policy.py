from __future__ import annotations

import random

from .action_bank import ActionKey


def type_prior_random_action(
    available: list[int] | tuple[int, ...],
    rng: random.Random,
    click_action_id: int,
    click_size: int,
    action6_prob: float,
) -> ActionKey:
    legal = [int(x) for x in available]
    if not legal:
        raise ValueError("No legal actions")
    click_legal = int(click_action_id) in legal
    simple = [x for x in legal if x != int(click_action_id)]
    if click_legal and simple:
        choose_click = rng.random() < float(action6_prob)
    else:
        choose_click = click_legal
    if choose_click:
        return ActionKey(int(click_action_id), rng.randrange(int(click_size)), rng.randrange(int(click_size)))
    return ActionKey(int(rng.choice(simple)))


def should_use_structured(system: dict, action_index: int, since_progress: int, rng: random.Random) -> bool:
    until = system.get("structured_until_action")
    if until is not None and int(action_index) >= int(until):
        return False
    after = system.get("structured_after_no_progress")
    if after is not None and int(since_progress) < int(after):
        return False
    p = float(system.get("structured_probability", 1.0))
    if p <= 0.0:
        return False
    if p >= 1.0:
        return True
    return rng.random() < p
