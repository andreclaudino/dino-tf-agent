import socketio
import eventlet

from dino_ia.server import socket
from dino_ia.server import http

http_runner = http.runner()
socket_runner = socket.socket


async def start_server(socket_runner, http_runner):
    app = socketio.WSGIApp(socket_runner, http_runner)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)


# def start():
#     http_runner = http.runner()
#     socket_runner = socket.socket
#
#     start_server(socket_runner, http_runner)
#
#     # while socket.enviroment.locked:
#     #     print("Wating client connect")
#
#     return socket.enviroment

