import numpy as np

from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
from tf_agents.specs import array_spec

import requests as req

ACTIONS = {-1: "DOWN", 0: "JUMP", 1: "DUCK"}
REWARDS = {"DOWN": -1, "JUMP": -1, "DUCK": -1}


class DinoEnv(py_environment.PyEnvironment):

    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=-1, maximum=1, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(7,), dtype=np.int32, minimum=0, name='observation')
        self._state = np.asarray([0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
        self._episode_ended = False

    def action_sped(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = np.asarray([0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
        self._episode_ended = False

        return ts.restart(self._state)

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        observable = req.get(f"http://0.0.0.0/act/{ACTIONS[action]}", timeout=10).json()

