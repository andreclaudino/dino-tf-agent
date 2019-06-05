import socketio

from dino_ia.environment.dino_enviroment import DinoEnv

socket = socketio.Server()
enviroment = DinoEnv()
socket.register_namespace(enviroment)

