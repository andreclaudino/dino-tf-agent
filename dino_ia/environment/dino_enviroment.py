import numpy as np
import socketio
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from thespian.actors import ActorSystem

from dino_ia.persist import PersistenseActor

STATES = {-1: "DOWN", 0: "JUMP", 1: "DUCK"}


class DinoEnv(py_environment.PyEnvironment, socketio.Namespace):

    def __init__(self):
        super(py_environment.PyEnvironment, self).__init__()
        super(socketio.Namespace, self).__init__()

        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=-1, maximum=1, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(7,), dtype=np.float32, minimum=0, name='observation')
        self._state = 0
        self._episode_ended = False

        self.state = None
        self.locked = True

        self._system = ActorSystem()
        self._persister = ActorSystem().createActor(PersistenseActor)

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = 0
        self._episode_ended = False
        return ts.restart(np.array([self._state], dtype=np.int32))

    def _step(self, action):
        self.emit(STATES[action])

        while True:
            if self.state is not None:
                state = self.state
                self.state = None
                print(state)
                return state

    def start(self):
        self.emit("START")

    def on_time_step(self, sid, message):
        # self.persist('WRITE', f"{sid}.json", data)
        state = np.asarray(message['observation']['state'], dtype=np.float32)
        ts.transition(state, reward=message['reward'], discount=message['discount'])

    def on_connect(self, sid, environ):
        print(f"Connected {sid}")
        # self.persist('CREATE', f"{sid}.json", None)

    def on_start(self, sid, message):
        self.locked = False

    def on_disconnect(self, sid):
        # self.persist('CLOSE', f"{sid}.json", ())
        print('disconnect ', sid)

    def persist(self, action, filename, data):
        message = (action, filename, data)
        self._system.tell(self._persister, message)