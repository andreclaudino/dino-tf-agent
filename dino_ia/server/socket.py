import socketio

sio = socketio.Server()


@sio.on('connect')
def connect(sid, environ):
    print('cliente conectado ', sid)
    sio.send("UP")


@sio.on('TimeStep')
def my_message(sid, data):
    print('TimeStep ', data)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


def runner():
    return sio


