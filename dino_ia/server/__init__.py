import socketio
import eventlet

from dino_ia.server import socket
from dino_ia.server import http


def start():
    http_runner = http.runner()
    socket_runner = socket.runner()

    app = socketio.WSGIApp(socket_runner, http_runner)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)

