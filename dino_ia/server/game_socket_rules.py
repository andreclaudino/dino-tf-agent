import numpy as np
import socketio
from multiprocessing import Process, Queue

STATES = {-1: "DOWN", 0: "JUMP", 1: "DUCK"}


class GameSocket(socketio.Namespace):

    def __init__(self):
        self.queue = Queue()
        self.connected = False
        print("Server stated")

    def on_connect(self, sid, environ):
        self.connected = True
        print("WebPage Conected")

    def on_time_step(self, sid, message):
        state = np.asarray(message['observation']['state'], dtype=np.float32)
        self.queue.put(state)
