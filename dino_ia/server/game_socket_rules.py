import numpy as np
import socketio
from multiprocessing import Queue


class GameSocket(socketio.Namespace):

    def __init__(self):
        super().__init__()

        self.game_connected = False
        self._queue = Queue()

        print("Server stated")

    def on_connect(self, sid, environ):
        self.game_connected = True
        print("Game Connected")

    def on_disconnect(self, sid):
        self.game_connected = False
        print("Game Disconnected")

    def on_time_step(self, sid, message):
        print(message)
        state = message['state']['observation']
        self._queue.put(state)
        print(f"Action {message} returns {state}")

    def get_observable(self):
        return self._queue.get()
