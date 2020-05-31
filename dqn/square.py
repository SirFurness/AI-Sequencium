from player import Player

class Square:
    def __init__(self):
        self.isEmpty = True
        self.content = 0
        self.isAvailableForA = False
        self.isAvailableForB = False
        self.player = Player.NoPlayer

    def makeAvailable(self, player):
        if player == Player.A:
            self.isAvailableForA = True
        elif player == Player.B:
            self.isAvailableForB = True

    def isAvailable(self, player):
        if player == Player.A:
            return self.isAvailableForA
        elif player == Player.B:
            return self.isAvailableForB

    def __str__(self):
        return str(self.content)
