import socketio

from dino_ia.server import game_socket
from dino_ia.server import http

http_runner = http.runner()
socket_runner = game_socket.socket


def start():
    http_runner.wsgi_app = socketio.WSGIApp(socket_runner, http_runner.wsgi_app)
    http_runner.run(threaded=True, port=3000)

