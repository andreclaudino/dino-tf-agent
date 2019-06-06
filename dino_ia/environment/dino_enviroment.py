import numpy as np
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from thespian.actors import ActorSystem

from dino_ia.actors.state_actor import StateActor

STATES = {-1: "DOWN", 0: "JUMP", 1: "DUCK"}


class DinoEnv(py_environment.PyEnvironment):

    def __init__(self):
        self._action_spec =\
            array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=-1, maximum=1, name='action')

        self._observation_spec =\
            array_spec.BoundedArraySpec(shape=(7,), dtype=np.float32, minimum=0, name='observation')

        self._state = 0
        self._episode_ended = False

        self._actor = ActorSystem().createActor(StateActor)
        self._system = ActorSystem()

    async def serve(self):
        self.send("SERVE")

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = None
        self._episode_ended = False
        return ts.restart(np.array([self._state], dtype=np.float32))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        observed = self.send(STATES[action])
        return ts.restart(np.array(observed, dtype=np.int32))

    def start(self):
        self.send("START")

    def on_connect(self, sid, environ):
        self.start()

    def on_disconnect(self, sid):
        # self.persist('CLOSE', f"{sid}.json", ())
        print('disconnect ', sid)

    def send(self, message):
        return self._system.ask(self._actor, message)
