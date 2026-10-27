"""Steps 4-7: checkpoint reconstruction, architecture substitution, DQN/PPO correctness, updates-disabled control."""
from types import SimpleNamespace

import numpy as np
import pytest
import torch
import torch.nn as nn

from src import config, model
from src.adapter import N_ACTIONS, N_SIMPLE, Observation, Transition, build_mask
from src.config import RunConfig
from src.dqn import DQN
from src.model import RepresentationOutput, collate
from src.ppo import PPO, compute_gae, evaluate_actions
from src.run import load_ckpt, run

TINY = {"id": "onehotcnn_stack2", "channels": 6, "context_dim": 24}
DQN_P = {"replay_capacity": 300, "warmup": 20, "train_every": 2, "batch": 8, "target_update": 25,
         "eps_decay_actions": 60}
PPO_P = {"rollout": 32, "minibatches": 4, "epochs": 2}


def obs_with(avail, seed=0, lv=0):
    r = np.random.default_rng(seed)
    f = r.integers(0, 13, (64, 64)).astype(np.int8)
    return Observation(f, r.integers(0, 13, (64, 64)).astype(np.int8), build_mask(avail), 2, lv, lv, 6)


def trans(o, a, reward=0.0, terminal=False, nxt=None):
    return Transition(o, a, reward, nxt or obs_with([1, 2, 3, 4], 1), terminal, False, {})


# ---------------------------------------------------------------- step 4: identity + checkpoint reconstruction
@pytest.mark.parametrize("algo,params", [("dqn", DQN_P), ("ppo", PPO_P)])
def test_checkpoint_reconstructs_architecture_and_weights(arc, tmp_path, algo, params):
    cfg = RunConfig(algo=algo, game="ls20", budget=150, arch=dict(TINY), params=params, seed=3)
    rec = run(cfg, arc=arc, out_dir=str(tmp_path), save_checkpoint=True)
    ck = next(tmp_path.glob("*/checkpoint.pt"))
    cfg2, learner2 = load_ckpt(ck)
    assert cfg2.resolved().to_dict() == cfg.resolved().to_dict() and cfg2.hash() == cfg.hash()
    assert learner2.arch == cfg.resolved().arch and learner2.model_info()["parameters"] == \
        rec["identity"]["model_info"]["parameters"]
    a, b = rec["_learner"].net.state_dict(), learner2.net.state_dict()
    assert all(torch.equal(a[k], b[k]) for k in a)
    o = collate([obs_with([1, 2, 3, 4, 6])])
    with torch.no_grad():
        for x, y in zip(_out(rec["_learner"].net, o), _out(learner2.net, o)):
            assert torch.equal(x, y)


def _out(net, o):
    r = net(o)
    return r if isinstance(r, tuple) else (r,)


# ---------------------------------------------------------------- step 5: architecture substitution by config only
class TinyMLP(nn.Module):
    """A structurally different representation (no convolutions) added in a test: component + config only."""

    def __init__(self, dim=16):
        super().__init__()
        self.lin = nn.Linear(64 * 64, dim)
        self.spatial_channels, self.out_dim = 4, dim
        self.up = nn.Linear(dim, 4 * 64 * 64)

    def forward(self, b):
        x = self.lin(b.frame.float().flatten(1) / 12.0).relu()
        return RepresentationOutput(pooled=x, spatial=self.up(x).view(-1, 4, 64, 64))


@pytest.mark.parametrize("algo,params", [("dqn", DQN_P), ("ppo", PPO_P)])
def test_swap_architecture_through_config_only(arc, monkeypatch, algo, params):
    monkeypatch.setitem(model._ARCHS, "tinymlp", lambda a: TinyMLP(a["dim"]))
    monkeypatch.setitem(config.ARCH_DEFAULTS, "tinymlp", {"id": "tinymlp", "dim": 16})
    ids = {}
    for arch in (dict(TINY), {"id": "onehotcnn_stack1", "channels": 6, "context_dim": 24}, {"id": "tinymlp", "dim": 16}):
        rec = run(RunConfig(algo=algo, game="ls20", budget=120, arch=arch, params=params), arc=arc)
        assert rec["status"] == "budget" and rec["counters"]["scorer_actions"] == 120
        ids[arch["id"]] = rec["identity"]["config_hash"]
    assert len(set(ids.values())) == 3                      # identity distinguishes the architectures


# ---------------------------------------------------------------- step 6: DQN
def test_dqn_target_is_masked_double_dqn_and_finite_on_terminals():
    d = DQN(dict(TINY), {**config.ALGO_DEFAULTS["dqn"], **DQN_P})
    d.start_run(0)
    nxt_one_legal = obs_with([5], 7)                         # only ACTION5 legal next
    nxt_none = Observation(*[getattr(nxt_one_legal, f) for f in ("frame", "prev_frame")],
                           np.zeros(N_ACTIONS, bool), 0, 0, 0, 6)     # fully masked next state
    cases = [(obs_with([1, 2, 3, 4], 1), 2, 1.0, True, obs_with([1, 2, 3, 4], 2)),      # terminal
             (obs_with([1, 2, 3, 4], 3), 0, 0.0, False, nxt_one_legal),                 # single legal next
             (obs_with([6], 4), 200, 0.0, False, obs_with([6], 5)),                    # click next
             (obs_with([1, 2], 6), 1, 0.0, False, nxt_none)]                           # nothing legal next
    for o, a, r, term, n in cases:
        d.observe(trans(o, a, r, term, n))
    idx = np.arange(4)
    d.rng = SimpleNamespace(integers=lambda lo, hi, n: idx)
    captured = {}
    import src.dqn as dqn_mod
    orig = dqn_mod.F.huber_loss
    dqn_mod.F.huber_loss = lambda q, y, delta=1.0: (captured.update(y=y.clone(), q=q.detach().clone()), orig(q, y, delta=delta))[1]
    try:
        d.n_seen = 10
        d._train()
    finally:
        dqn_mod.F.huber_loss = orig
    y = captured["y"]
    assert torch.isfinite(y).all() and np.isfinite(d.loss_ema)
    nb = d.next_store.get(idx)
    with torch.no_grad():
        qo, qt = d.net(nb), d.target(nb)
    for j, (o, a, r, term, n) in enumerate(cases):
        if term:
            assert y[j] == pytest.approx(r)
        elif not n.mask.any():
            assert y[j] == pytest.approx(r)                   # nothing to bootstrap from
        else:
            legal = torch.from_numpy(n.mask)
            a2 = int(qo[j].masked_fill(~legal, -1e9).argmax())
            assert legal[a2]
            assert y[j] == pytest.approx(r + 0.99 * float(qt[j, a2]), abs=1e-5)


def test_dqn_greedy_never_illegal_and_epsilon_is_type_balanced():
    d = DQN(dict(TINY), {**config.ALGO_DEFAULTS["dqn"], **DQN_P})
    d.start_run(1)
    for avail in ([6], [1, 2, 3, 4], [3, 4, 6, 7], [5, 6, 7]):
        o = obs_with(avail)
        for eps in (0.0, 1.0):
            d.p = {**d.p, "eps_start": eps, "eps_end": eps}
            assert all(o.mask[d.act(o)] for _ in range(40))
    d.p = {**d.p, "eps_start": 1.0, "eps_end": 1.0}
    o = obs_with([1, 2, 3, 4, 5, 6])
    click = np.mean([d.act(o) >= N_SIMPLE for _ in range(1500)])
    assert abs(click - 1 / 6) < 0.04                          # type-balanced, not 99.9% clicks


# ---------------------------------------------------------------- step 7: PPO
def test_ppo_joint_logprob_agrees_with_independent_computation_before_any_update():
    p = PPO(dict(TINY), {**config.ALGO_DEFAULTS["ppo"], **PPO_P})
    p.start_run(0)
    for avail in ([1, 2, 3, 4, 6, 7], [6], [1, 2, 3, 4], [5, 6, 7]):
        o = obs_with(avail, 3)
        idxs, lps = [], []
        for _ in range(30):
            idxs.append(p.act(o))
            lps.append(p._pending[2])
        b = collate([o] * 30)
        logp, ent, _ = evaluate_actions(p.net, b, torch.tensor(idxs))
        assert torch.allclose(logp, torch.tensor(lps), atol=1e-5)
        with torch.no_grad():                                   # independent: full joint distribution over 4102 actions
            tl, cl, _ = p.net(collate([o]))
            tm = torch.from_numpy(np.concatenate([o.mask[:N_SIMPLE], [o.mask[N_SIMPLE:].any()]]))
            pt = torch.softmax(tl[0].masked_fill(~tm, -1e9), 0)
            pc = torch.softmax(cl[0].masked_fill(~torch.from_numpy(o.mask[N_SIMPLE:]), -1e9), 0)
            joint = torch.cat([pt[:N_SIMPLE], pt[N_SIMPLE] * pc])
        assert joint.sum().item() == pytest.approx(1.0, abs=1e-5)
        assert joint[~torch.from_numpy(o.mask)].max().item() < 1e-6            # illegal actions get ~0 probability
        assert (joint[torch.from_numpy(o.mask)] > 0).all()                      # every legal action stays reachable
        for i, lp in zip(idxs[:5], lps[:5]):
            assert lp == pytest.approx(float(joint[i].log()), abs=1e-4)
        h = -(joint[joint > 0] * joint[joint > 0].log()).sum()
        assert float(ent[0]) == pytest.approx(float(h), abs=1e-4)              # H(type) + p(click) * H(loc | click)


def test_gae_stops_at_terminal_boundaries():
    r = np.array([0, 0, 1, 0, 0], np.float32)
    d = np.array([0, 0, 1, 0, 0], np.float32)                    # terminal at t=2
    v = np.array([.5, .4, .3, .2, .1], np.float32)
    a1 = compute_gae(r, v, d, last_value=0.7, gamma=0.9, lam=0.8)
    v2 = v.copy(); v2[3:] += 5                                    # post-terminal values must not leak backwards
    a2 = compute_gae(r, v2, d, last_value=9.0, gamma=0.9, lam=0.8)
    assert np.allclose(a1[:3], a2[:3])
    assert a1[2] == pytest.approx(1.0 - 0.3)                      # r - V, no bootstrap
    assert not np.allclose(a1[3:], a2[3:])                        # but the open segment does bootstrap


def test_ppo_updates_finite_with_masks_terminals_and_partial_rollout(arc):
    for game in ("ls20", "sb26"):                                 # keyboard-only (click masked) and mixed, GAME_OVERs occur
        rec = run(RunConfig(algo="ppo", game=game, budget=170, arch=dict(TINY), params=PPO_P), arc=arc)
        lr = rec["learner"]
        assert lr["rollout_update_events"] >= 5 and lr["gradient_steps"] >= 5 * 2 * 4
        assert lr["partial_rollouts"] == 1
        assert all(np.isfinite(lr[k]) for k in lr if k.endswith("_ema"))


# ---------------------------------------------------------------- updates-disabled control
@pytest.mark.parametrize("algo,params", [("dqn", DQN_P), ("ppo", PPO_P)])
def test_updates_disabled_control_leaves_weights_untouched(arc, algo, params):
    on = run(RunConfig(algo=algo, game="ls20", budget=160, arch=dict(TINY), params=params, seed=2), arc=arc)
    off = run(RunConfig(algo=algo, game="ls20", budget=160, arch=dict(TINY), params=params, seed=2,
                        updates_disabled=True), arc=arc)
    assert on["learner"]["gradient_steps"] > 0 and off["learner"]["gradient_steps"] == 0
    init = (DQN if algo == "dqn" else PPO)(dict(TINY), {**config.ALGO_DEFAULTS[algo], **params}, True)
    init.start_run(2)
    w0, w1, w2 = init.net.state_dict(), off["_learner"].net.state_dict(), on["_learner"].net.state_dict()
    assert all(torch.equal(w0[k], w1[k]) for k in w0)             # identical to initialisation
    assert any(not torch.equal(w0[k], w2[k]) for k in w0)         # the learner did move
    assert on["identity"]["config_hash"] != off["identity"]["config_hash"]
