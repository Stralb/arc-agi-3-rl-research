import random
import unittest

import numpy as np
import torch

from arc_e012.action_bank import ActionBank, ActionKey
from arc_e012.agent import DQNAgent
from arc_e012.policy import should_use_structured, type_prior_random_action


class CoreTests(unittest.TestCase):
    def cfg(self):
        return {
            "click_action_id": 6,
            "click_size": 64,
            "max_action_id": 7,
            "training": {
                "gamma": 0.99,
                "learning_rate": 1e-4,
                "batch_size": 8,
                "replay_capacity": 128,
                "warmup_actions": 16,
                "train_every_actions": 8,
                "target_update_actions": 80,
                "gradient_clip_norm": 10.0,
                "hidden_dim": 32,
                "epsilon_start": 1.0,
                "epsilon_end": 0.1,
                "epsilon_decay_actions": 40,
                "per_alpha": 0.6,
                "per_beta_start": 0.4,
                "per_beta_end": 1.0,
                "per_eps": 1e-4,
                "c51_atoms": 51,
                "c51_vmin": 0.0,
                "c51_vmax": 5.0,
            },
        }

    def system(self):
        return {"learn": True, "n_step": 1, "per": False, "dueling": True, "distributional": False}

    def test_action7_and_full_click_space(self):
        bank = ActionBank(6, 64, max_action_id=7)
        keys, enc = bank.encode_candidates([3, 4, 6, 7])
        self.assertEqual(len(keys), 4099)
        self.assertEqual(enc.shape, (4099, 10))
        self.assertTrue(any(k.action_id == 7 for k in keys))

    def test_epsilon_coin_stream_is_independent_of_explorer_rng_consumption(self):
        a = DQNAgent(8, self.system(), self.cfg(), 1234, torch.device("cpu"))
        b = DQNAgent(8, self.system(), self.cfg(), 1234, torch.device("cpu"))
        state = np.zeros(8, dtype=np.float32)
        mask_a, mask_b = [], []
        for _ in range(60):
            _, la = a.act(state, [1, 6])
            def noisy_callback(rng, action_index):
                for _ in range(17):
                    rng.random()
                return ActionKey(1), "d14"
            _, lb = b.act(state, [1, 6], explore_fn=noisy_callback)
            mask_a.append(la != "greedy")
            mask_b.append(lb != "greedy")
        self.assertEqual(mask_a, mask_b)

    def test_type_prior_matches_requested_click_probability(self):
        rng = random.Random(77)
        n = 20000
        clicks = sum(type_prior_random_action([1, 2, 6, 7], rng, 6, 64, 0.7).action_id == 6 for _ in range(n))
        self.assertAlmostEqual(clicks / n, 0.7, delta=0.02)

    def test_structured_gates(self):
        rng = random.Random(1)
        self.assertTrue(should_use_structured({"structured_probability": 1.0}, 0, 0, rng))
        self.assertTrue(should_use_structured({"structured_until_action": 250}, 249, 0, rng))
        self.assertFalse(should_use_structured({"structured_until_action": 250}, 250, 0, rng))
        self.assertFalse(should_use_structured({"structured_after_no_progress": 50}, 10, 49, rng))
        self.assertTrue(should_use_structured({"structured_after_no_progress": 50}, 10, 50, rng))


if __name__ == "__main__":
    unittest.main()
