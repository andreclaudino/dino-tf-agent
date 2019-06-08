import os
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
from tf_agents.specs import array_spec

import requests as req

BASE_ADDRESS = os.environ.get('BASE_ADDRESS', '0.0.0.0:3000')


class DinoEnv(py_environment.PyEnvironment):

    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=-1, maximum=1, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(7,), dtype=np.float32, name='observation')
        self._state = np.asarray([0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
        self._episode_ended = False
        self.state_reward = 0

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = np.asarray([0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
        self._episode_ended = False

        self.send('START')

        return ts.restart(self._state)

    def _step(self, action):
        if self._episode_ended:

            return self.reset()

        action_message, reward = self.act(action)
        request_result = self.send(action_message)

        if request_result['crashed']:
            self._episode_ended = True

            reward = -100000
            self.state_reward += reward
            value = np.asarray(request_result['value'], dtype=np.float32)

            print(f"Finished with {self.state_reward} scores")

            return ts.termination(value, reward)

        value = np.asarray(request_result['value'], dtype=np.float32)
        self.state_reward += reward

        print(f"Act with {self.state_reward} scores")

        return ts.transition(value, reward)

    def act(self, action):
        reward = 0
        action_message = ''

        if action == -1:
            action_message = 'RUN'
            reward = 10
        elif action == 0:
            action_message = 'JUMP'
            reward = -5
        elif action == 1:
            action_message = 'DUCK'
            reward = -5
        return action_message, reward

    def send(self, action_message, timeout=0.1):
        try:
            return req.get(f"http://{BASE_ADDRESS}/act/{action_message.upper()}", timeout=timeout).json()
        except:
            return dict(value=[0, 0, 0, 0, 0, 0, 0], crashed=True)

