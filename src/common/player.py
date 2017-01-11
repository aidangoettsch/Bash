import uuid


class Player(object):
    def __init__(self, socket, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.spectator = False
        self.location = (0, 0)
        self.velocity = (0, 0)
        self.socket = socket

        # Client button events
        self.up = False
        self.left = False
        self.down = False
        self.right = False
        self.heavy = False
