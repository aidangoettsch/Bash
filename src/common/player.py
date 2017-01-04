class Player:
    def __init__(self, socket, name):
        self.name = name
        self.spectator = True
        self.location = ()
        self.velocity = (0, 0)

        # Client button events
        self.up = False
        self.left = False
        self.down = False
        self.right = False
