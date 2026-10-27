import numpy as np

from src.adapter import NO_ACTION, ArcSession, action_to_index, sample_type_uniform


def test_ft09_diagnostic_replay_gives_exactly_one_reward(arc):
    """Replays the Phase 1 recorded seed-7 trajectory (diagnostic only, not a policy): one level-up at step 1915."""
    s = ArcSession(arc)
    s.start_run("ft09", budget=2100)
    acts = s.env.action_space
    rng = np.random.RandomState(7)
    rewards = []
    for i in range(2100):
        a = acts[rng.randint(len(acts))]
        if a.is_complex():
            idx = action_to_index(a.value, (int(rng.randint(64)), int(rng.randint(64))))
        else:
            idx = action_to_index(a.value)
        t = s.step(idx)
        if t.reward:
            rewards.append((i, t.reward, t.next_obs.progress, t.next_obs.high_water))
            break
    assert rewards == [(1915, 1.0, 1, 1)]


class LoggingSession(ArcSession):
    def __init__(self, arc):
        super().__init__(arc)
        self.cmds = []

    def _reset(self):
        self.cmds.append("R")
        return super()._reset()

    def _send(self, aid, xy):
        self.cmds.append("S")
        return super()._send(aid, xy)


def test_never_two_consecutive_resets_and_history_cleared_on_reset(arc):
    rng = np.random.default_rng(0)
    s = LoggingSession(arc)
    s.start_run("vc33", budget=800)                        # dies within ~50 steps: many GAME_OVERs
    saw_reset_obs = 0
    while not s.done:
        t = s.step(sample_type_uniform(rng, s.obs.mask))
        if t.terminal and not s.done:
            saw_reset_obs += 1
            o = s.obs
            assert o.prev_action == NO_ACTION and np.array_equal(o.frame, o.prev_frame)
            assert t.next_obs.prev_action == t.action      # terminal transition keeps its own frame/context
    assert saw_reset_obs >= 3
    assert "RR" not in "".join(s.cmds)
    assert s.tracker.actions == 800                        # counters persisted across resets


def test_high_water_and_counters_persist_through_resets(arc):
    s = ArcSession(arc)
    s.start_run("ft09", budget=2100)
    acts = s.env.action_space
    rng = np.random.RandomState(7)
    for i in range(2100):
        a = acts[rng.randint(len(acts))]
        idx = action_to_index(a.value, (int(rng.randint(64)), int(rng.randint(64)))) if a.is_complex() \
            else action_to_index(a.value)
        t = s.step(idx)
        if t.reward:
            break
    hw, n = s.tracker.high_water, s.tracker.actions
    assert hw == 1 and n > 1900
    while s.status == "running" and s.tracker.episode < 20 and not (t.terminal):
        t = s.step(sample_type_uniform(np.random.default_rng(1), s.obs.mask))
    assert s.tracker.high_water >= hw and s.tracker.actions > n
