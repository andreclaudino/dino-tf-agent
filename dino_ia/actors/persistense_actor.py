import json
from thespian.actors import *


class PersistenseActor(Actor):

    def __init__(self):
        super(PersistenseActor, self).__init__()
        self.file = None

    def create_file(self, filename):
        self.file = open(f"essays/{filename}.json", "a+")

    def write_file(self, message):
        self.file.write(f"{json.dumps(message)}\n")

    def receiveMessage(self, data, _):
        """
        Persist a message on filesystem
        :param data: A tuple containing (action, socket_id, message)
        :return:
        """

        action, filename, message = data

        if action == 'CREATE':
            self.create_file(filename)
        elif action == 'WRITE':
            self.write_file(message)


