import os

import socketio
import eventlet
from thespian.actors import *

from dino_ia.server import http

_sio = socketio.Server()


class StateActor(Actor, socketio.Namespace):

    def __init__(self):
        super(Actor, self).__init__()
        super(socketio.Namespace, self).__init__()

        self.state = None

    # Actor part
    def receiveMessage(self, data, sender):
        # Return socket connection
        if data == 'SERVE':
            self.start_service()
        else:
            # if data is an action to game, send it
            self.act(data)
            # and wait until get a response by get_state
            self.send(sender, self.get_state())

    # State part
    def act(self, action):
        # Send command to game
        _sio.emit(action, {})

    def get_state(self):
        # Wait for response from game
        while not self.state:
            print("Waiting response", end='\r')

        state = self.state
        self.state = None

        return state

    # Server part
    async def start_service(self):
        """
        Starts game server: API + Socket.IO server
        :return:
        """
        http_runner = http.runner()
        socket_runner = _sio

        app = socketio.WSGIApp(socket_runner, http_runner)
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
        _sio.register_namespace(StateActor())

    def on_connect(self, sid, environ):
        self.act("START")

    def on_disconnect(self, sid):
        self.act("REFRESH")
        _sio.disconnect(sid)

    async def on_time_step(self, sid, message):
        # Should adjust to get only state vector and useful data
        self.state = message['observation']['state']


_sio.register_namespace(StateActor())
