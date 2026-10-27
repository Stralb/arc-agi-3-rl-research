import numpy as np
import pytest

from src.adapter import (ArcSession, IllegalAction, InterfaceError, N_ACTIONS, N_SIMPLE, RawFrame, Tracker,
                         action_to_index, action_type, build_mask, index_to_action, sample_flat_uniform,
                         sample_type_uniform, type_mask)


def raw(state="NOT_FINISHED", lv=0, avail=(1, 2, 3, 4), frames=1, fill=0):
    return RawFrame([np.full((64, 64), fill, np.int8) for _ in range(frames)], state, lv, 6, list(avail))


def test_index_round_trip_all_actions():
    for idx in range(N_ACTIONS):
        aid, xy = index_to_action(idx)
        assert action_to_index(aid, xy) == idx
    assert index_to_action(N_SIMPLE + 5 * 64 + 3) == (6, (3, 5))      # x = column, y = row
    with pytest.raises(ValueError):
        index_to_action(N_ACTIONS)


@pytest.mark.parametrize("avail,n_legal", [([6], 4096), ([1, 2, 3, 4], 4), ([3, 4, 6, 7], 4099), ([5, 6, 7], 4098)])
def test_masks(avail, n_legal):
    m = build_mask(avail)
    assert m.sum() == n_legal and len(m) == N_ACTIONS
    assert type_mask(m).sum() == len(set(avail))


def test_samplers_never_illegal():
    rng = np.random.default_rng(0)
    for avail in ([6], [1, 2, 3, 4], [3, 4, 6, 7], [5, 6, 7]):
        m = build_mask(avail)
        for fn in (sample_type_uniform, sample_flat_uniform):
            for _ in range(500):
                assert m[fn(rng, m)]


def test_type_uniform_vs_flat_click_share():
    rng = np.random.default_rng(1)
    m = build_mask([1, 2, 3, 4, 5, 6])
    n = 5000
    flat = np.mean([action_type(sample_flat_uniform(rng, m)) == 6 for _ in range(n)])
    typ = np.mean([action_type(sample_type_uniform(rng, m)) == 6 for _ in range(n)])
    assert flat > 0.99 and abs(typ - 1 / 6) < 0.03


def test_tracker_reward_is_first_ever_progress_and_high_water_survives_reset():
    tr = Tracker(budget=100)
    tr.note_reset_command(); tr.begin_episode(raw(lv=0))
    assert tr.advance(0, raw(lv=1)).reward == 1.0
    tr.begin_episode(raw(lv=0))                       # e.g. a full reset lowered progress to 0
    assert tr.high_water == 1 and tr.obs.progress == 0 and tr.obs.high_water == 1
    assert tr.advance(0, raw(lv=1)).reward == 0.0     # re-completing level 1 pays nothing
    assert tr.advance(0, raw(lv=2)).reward == 1.0


def test_tracker_budget_and_free_first_reset():
    tr = Tracker(budget=3)
    tr.note_reset_command()
    assert tr.actions == 0
    tr.begin_episode(raw())
    tr.advance(0, raw()); tr.note_reset_command()
    assert (tr.actions, tr.env_commands, tr.exhausted) == (2, 3, False)
    assert tr.advance(0, raw()).truncated and tr.exhausted


def test_tracker_terminal_and_masks_and_errors():
    tr = Tracker(budget=None)
    tr.note_reset_command(); tr.begin_episode(raw(avail=(1, 2)))
    t = tr.advance(0, raw("GAME_OVER", avail=()))       # empty available_actions -> reuse last non-empty mask
    assert t.terminal and not t.truncated and t.next_obs.mask.sum() == 2
    with pytest.raises(InterfaceError):
        tr.advance(0, raw(frames=0))                     # empty frame list during active play
    assert tr.obs.prev_action == 0 and np.array_equal(tr.obs.frame, tr.obs.prev_frame) is True


def test_previous_frame_is_last_frame_of_previous_step():
    tr = Tracker(budget=None)
    tr.note_reset_command(); tr.begin_episode(raw(fill=1))
    r = RawFrame([np.full((64, 64), 7, np.int8), np.full((64, 64), 9, np.int8)], "NOT_FINISHED", 0, 6, [1])
    t = tr.advance(0, r)
    assert t.next_obs.frame[0, 0] == 9 and t.next_obs.prev_frame[0, 0] == 1
    t2 = tr.advance(0, raw(fill=3))
    assert t2.next_obs.prev_frame[0, 0] == 9            # last frame of previous step, not second-to-last


# ---------------------------------------------------------------- real SDK
def test_click_placement_matches_sdk(arc):
    from arcengine import GameAction
    env = arc.make("ft09")
    env.reset()

    def direct(x, y):
        env.reset()
        return np.array(env.step(GameAction.ACTION6, data={"x": x, "y": y}).frame[-1])

    found = None
    for x in range(2, 64, 5):
        for y in range(2, 64, 5):
            if x != y and not np.array_equal(direct(x, y), direct(y, x)):
                found = (x, y)
                break
        if found:
            break
    assert found, "no asymmetric click found on ft09 grid"
    x, y = found
    s = ArcSession(arc)
    s.start_run("ft09", budget=10)
    t = s.step(action_to_index(6, (x, y)))
    assert np.array_equal(t.next_obs.frame, direct(x, y))
    assert not np.array_equal(t.next_obs.frame, direct(y, x))


def test_illegal_action_rejected(arc):
    s = ArcSession(arc)
    s.start_run("ls20", budget=10)                       # keyboard-only game
    with pytest.raises(IllegalAction):
        s.step(N_SIMPLE + 100)                           # a click
    with pytest.raises(IllegalAction):
        s.step(4)                                        # ACTION5 not available in ls20


@pytest.mark.parametrize("game", ["ft09", "ls20", "sb26"])
def test_random_run_budget_exact_and_matches_scorecard(arc, game):
    rng = np.random.default_rng(3)
    s = ArcSession(arc)
    s.start_run(game, budget=600)
    n = 0
    while not s.done:
        t = s.step(sample_type_uniform(rng, s.obs.mask)); n += 1
        assert not (t.terminal and s.status == "budget" and s.tracker.env_commands > 601 + s.tracker.resets)
    assert s.status == "budget" and s.tracker.actions == 600
    card = s.scorecard()
    assert card["total_actions"] == 600, card["total_actions"]                 # our counter == official counter
    assert card["environments"][0]["resets"] == s.tracker.resets - 1           # first reset is free/uncounted
