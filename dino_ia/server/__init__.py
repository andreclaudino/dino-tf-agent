import eventlet
import socketio

from dino_ia.server import game_socket
from dino_ia.server import http

http_runner = http.runner()
socket_runner = game_socket.socket


def start_server(socket_runner, http_runner):
    app = socketio.WSGIApp(socket_runner, http_runner)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)


def start():
    http_runner = http.runner()
    socket_runner = game_socket.socket

    start_server(socket_runner, http_runner)

    # while socket.enviroment.locked:
    #     print("Wating client connect")

    return game_socket.gameSocket

