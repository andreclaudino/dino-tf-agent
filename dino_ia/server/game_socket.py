import socketio

from dino_ia.server.game_socket_rules import GameSocket

socket = socketio.Server()
gameSocket = GameSocket()
socket.register_namespace(gameSocket)

