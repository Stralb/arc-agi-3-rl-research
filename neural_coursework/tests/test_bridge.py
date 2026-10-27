"""Step 9: the learner lifecycle survives the competition callback (real ARC-AGI-3-Agents Agent.main loop)."""
import importlib.util
import json
import sys

import pytest
import torch

from tests.conftest import ROOT

FW = ROOT / "vendor" / "ARC-AGI-3-Agents"
pytestmark = pytest.mark.skipif(not FW.exists(), reason="vendor/ARC-AGI-3-Agents not cloned")

TINY = {"id": "onehotcnn_stack2", "channels": 6, "context_dim": 24}
SLIM_INIT = ('"""slim"""\nfrom dotenv import load_dotenv\nfrom .agent import Agent, Playback\nfrom .swarm import Swarm\n'
             'from .templates.random_agent import Random\nload_dotenv()\nAVAILABLE_AGENTS = {"random": Random}\n')


def load_agent_module(monkeypatch, config: dict):
    (FW / "agents" / "__init__.py").write_text(SLIM_INIT, encoding="utf-8")   # same slimming the Kaggle sample does
    monkeypatch.syspath_prepend(str(FW))
    monkeypatch.setenv("ARC_LEARNER_CONFIG", json.dumps(config))
    for m in [m for m in sys.modules if m == "agents" or m.startswith("agents.")]:
        del sys.modules[m]
    spec = importlib.util.spec_from_file_location("learner_agent", ROOT / "kaggle" / "learner_agent.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("algo,params", [
    ("dqn", {"replay_capacity": 300, "warmup": 20, "train_every": 2, "batch": 8, "target_update": 25}),
    ("ppo", {"rollout": 32, "minibatches": 4, "epochs": 2})])
@pytest.mark.parametrize("game", ["ls20", "vc33"])          # vc33 reaches GAME_OVER quickly: exercises the reset path
def test_learning_persists_and_updates_through_framework_loop(arc, monkeypatch, algo, params, game):
    budget = 200
    mod = load_agent_module(monkeypatch, {"algo": algo, "budget": budget, "arch": TINY, "params": params, "seed": 4})
    card_id = arc.open_scorecard()                            # isolated scorecard: its count is this run's alone
    agent = mod.MyAgent(card_id=card_id, game_id=game, agent_name="t", ROOT_URL="http://localhost", record=False,
                        arc_env=arc.make(game, scorecard_id=card_id), tags=[])
    w0 = {k: v.clone() for k, v in agent.learner.net.state_dict().items()}
    sent, cmds = [], []
    orig_act, orig_choose = agent.learner.act, agent.choose_action

    def checked_act(obs):
        idx = orig_act(obs)
        assert obs.mask[idx], "learner produced an illegal action"
        sent.append(idx)
        return idx

    def logged_choose(frames, latest):
        a = orig_choose(frames, latest)
        cmds.append(a.name)
        return a

    agent.learner.act, agent.choose_action = checked_act, logged_choose
    agent.main()

    tk, br = agent.bridge.tracker, agent.bridge
    assert agent.action_counter == budget == len(cmds)                    # the framework enforced the budget
    assert cmds.count("RESET") == tk.resets >= (1 if game == "vc33" else 0)
    assert not any(a == b == "RESET" for a, b in zip(cmds, cmds[1:]))     # never two consecutive resets
    assert br.n_observed == len(sent) - 1                                 # every outcome delivered before the next act()
    #   (the outcome of the very last action is the only one the agent never sees)
    card = json.loads(arc.get_scorecard(card_id).model_dump_json())
    assert card["total_actions"] == budget == tk.actions + 1              # official count == our count + unseen last action
    assert agent.learner.diagnostics()["gradient_steps"] > 0              # learning happened inside the callback path
    w1 = agent.learner.net.state_dict()
    assert any(not torch.equal(w0[k], w1[k]) for k in w0)                 # weights persisted across levels/resets and moved
