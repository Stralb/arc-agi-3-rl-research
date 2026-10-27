import numpy as np

from src.synthetic import CueTask, NavTask, SyntheticSession


def test_synthetic_sessions_have_no_official_score_and_use_adapter_rewards():
    s = SyntheticSession("nav")
    s.start_run("nav", budget=500, env_seed=0)
    rng = np.random.default_rng(0)
    rewards = 0.0
    while not s.done:
        rewards += s.step(int(rng.integers(4))).reward
    assert s.scorecard() is None and s.tracker.actions == 500
    assert rewards == s.tracker.high_water > 0                 # reward comes from the shared Tracker (high-water)


def test_nav_goal_reward_and_timeout_reset():
    s = SyntheticSession("nav")
    s.start_run("nav", budget=1000, env_seed=1)
    t = None
    for _ in range(NavTask.LIMIT):                             # stand still against a wall until the attempt times out
        s.task.pos = [0, 0]
        t = s.step(0)                                          # index 0 = ACTION1 (up): stays at the wall
    assert t.terminal and t.info["state"] == "GAME_OVER" and s.tracker.resets == 2
    s.task.pos = [3, 4]
    t = s.step(3)                                              # ACTION4 = right -> goal (4,4)
    assert t.reward == 1.0 and t.next_obs.progress == 1


def test_cue_task_is_beyond_the_local_receptive_field_and_rewards_only_the_cued_square():
    t = CueTask(0)
    for _ in range(50):
        t.reset()
        # Chebyshev distance from the cue block (rows/cols 2..5) to every square pixel: a 9x9 receptive field sees
        # +-4 px, so distance > 4 means no click location can "see" the cue locally.
        for (x, y) in t.boxes:
            assert max(y - 5, x - 5) > 4
        f = t._draw()
        (x0, y0), (x1, y1) = t.boxes
        assert f[y0, x0] == 3 and f[y1, x1] == 4 and f[3, 3] == 5 + t.cue     # squares differ in colour; cue block colour
        for cue in (0, 1):
            t.cue = cue
            correct, wrong = t.boxes[cue], t.boxes[1 - cue]
            before = t.levels
            t.send(6, (wrong[0] + 3, wrong[1] + 3))
            assert t.levels == before                          # wrong colour: no reward
            t.send(6, (correct[0] + 3, correct[1] + 3))
            assert t.levels == before + 1                      # cued colour: reward, new level
