from thespian.actors import ActorSystem
import socketio

from  dino_ia.actors import PersistenseActor

_sio = socketio.Server()
_persister = ActorSystem().createActor(PersistenseActor)
_system = ActorSystem()


def tell(action, message):
    _system.tell(_persister, message)


@_sio.on('connect')
def connect(sid, environ):
    tell('CREATE', sid)
    _sio.send("START")


@_sio.on('TimeStep')
def my_message(sid, message):
    tell('WRITE', sid, message)


@_sio.on('disconnect')
def disconnect(sid):
    tell('CLOSE', ())
    print('disconnect ', sid)


def runner():
    return _sio


