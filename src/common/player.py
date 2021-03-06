import uuid


class Player(object):
    """
    Class representing a player
    """
    def __init__(self, socket, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.spectator = True
        self.location = [200, 200]
        self.velocity = [0, 0]
        self.socket = socket

        # Client button events
        self.up = False
        self.left = False
        self.down = False
        self.right = False
        self.heavy = False
