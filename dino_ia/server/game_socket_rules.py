from multiprocessing import Queue

import numpy as np
import socketio

STATES = {-1: "DOWN", 0: "JUMP", 1: "DUCK"}


class GameSocket(socketio.Namespace):

    def __init__(self):
        super().__init__()

        self.queue = Queue()
        self.game_connected = False
        print("Server stated")

    def on_connect(self, sid, environ):
        self.game_connected = True
        print("Game Connected")

    def on_time_step(self, sid, message):
        state = np.asarray(message['observation']['state'], dtype=np.float32)
        self.queue.put(state)
        print(message)

    def state(self):
        return self.queue.get()
