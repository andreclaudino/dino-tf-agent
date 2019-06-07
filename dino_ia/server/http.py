import os
from time import sleep

from flask import Flask
from flask import send_from_directory

from dino_ia.server.game_socket import socket
from dino_ia.server.game_socket import gameSocket

import json

# if the environment variable with static files root path is set,
# send from there, else, send from static folder in current dir by default
STATIC_ROOT = os.environ.get('DINO_STATIC_ROOT', f'{os.getcwd()}{os.sep}static')

app = Flask(__name__)


@app.route('/')
def index():
    """
    flask route to access static files
    :param path:
    :return:
    """
    return send_from_directory(STATIC_ROOT, "index.html")


@app.route('/<path:path>')
def root_files(path):
    """
    flask route to access static files
    :param path:
    :return:
    """
    return send_from_directory(f"{STATIC_ROOT}", path)


@app.route('/assets/<path:path>')
def assets(path):
    """
    flask route to access static files
    :param path:
    :return:
    """
    return send_from_directory(f"{STATIC_ROOT}/assets", path)


@app.route("/act/<action>")
def act(action):
    socket.emit(action.upper())
    sleep(.05)
    return json.dumps(gameSocket.get_observable())


def runner():
    """
    Start http server
    :return:
    """
    return app
