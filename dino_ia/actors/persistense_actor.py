import json
import os
from thespian.actors import *


class PersistenseActor(Actor):

    def __init__(self):
        super(PersistenseActor, self).__init__()

        if not os.path.exists("essays"):
            os.makedirs("essays")
        self.file = None

    def create_file(self, filename):
        self.file = open(f"essays/{filename}", "a+")

    def write_file(self, message):
        self.file.write(f"{json.dumps(message)}\n")
        print(message)

    def receiveMessage(self, data, sender):
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


