import socketio

from dino_ia.server.game_socket_rules import GameSocket

socket = socketio.Server(async_mode='threading')
gameSocket = GameSocket()
socket.register_namespace(gameSocket)

