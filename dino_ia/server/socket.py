import socketio
from thespian.actors import ActorSystem
from  dino_ia.actors import PersistenseActor

_sio = socketio.Server()
_system = ActorSystem()
_persister = ActorSystem().createActor(PersistenseActor)


def persist(action, filename, data):
    message = (action, filename, data)
    _system.tell(_persister, message)


@_sio.on('connect')
def connect(sid, _):
    print(f"Connected {sid}")
    persist('CREATE', f"{sid}.json", None)
    send("START")


@_sio.on('TimeStep')
def step(sid, data):
    persist('WRITE', f"{sid}.json", data)


@_sio.on('disconnect')
def disconnect(sid):
    persist('CLOSE', f"{sid}.json", ())
    print('disconnect ', sid)


def send(action):
    _sio.emit(action, {})


def runner():
    return _sio


