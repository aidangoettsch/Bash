import uuid


class Player(object):
    def __init__(self, socket, name):
        self.id = str(uuid.UUID())
        self.name = name
        self.spectator = True
        self.location = ()
        self.velocity = (0, 0)
        self.socket = socket

        # Client button events
        self.up = False
        self.left = False
        self.down = False
        self.right = False
        self.heavy = False
