import os

from flask import Flask
from flask import send_from_directory

from dino_ia.server.game_socket import gameSocket

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


@app.route("/state")
def state():
    gameSocket.emit("STATE")


@app.route("/action/<action:string>")
def state(action):
    gameSocket.emit(action.upper())


def runner():
    """
    Start http server
    :return:
    """
    # app.run(host="0.0.0.0", port="3000")
    return app
