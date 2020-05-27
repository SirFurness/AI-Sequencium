import math

from player import Player
from winner import Winner
from game import Game

class Environment:
    def __init__(self):
        self.game = Game()

        self.winReward = 1
        self.loseReward = -1
        self.tieReward = 0
        self.notOverReward = 0

    def restart(self):
        self.game.restart()

    def step(self, action):
        self.applyAction(action)
        
        newState = self.getState()
        reward = self.getReward()
        isDone = self.game.isGameOver()

        return (newState, reward, isDone)

    def applyAction(self, action):
        # no-move action
        if action < 0:
            return

        coordinate = self.convertActionToCoordinate(action)
        self.game.updateGrid(coordinate[0], coordinate[1]) 

    def convertActionToCoordinate(self, action):
        row = math.trunc(action / self.game.size)
        col = action % self.game.size

        return (row, col)

    def getState(self):
        # flattens the list
        return [self.getSquareContent(square)
                for row in self.game.grid for square in row]

    def getSquareContent(self, square):
        if square.player == Player.A:
            return square.content
        elif square.player == Player.B:
            return square.content * -1
        else:
            # NoPlayer
            return 0

    def getReward(self):
        winner = self.game.getWinner()
        player = self.game.currentPlayer

        if winner == Winner.NotOver:
            return self.notOverReward
        elif winner == Winner.Tie:
            return self.tieReward
        elif winner == Winner.A and player == Player.A:
            return self.winReward
        elif winner == Winner.B and player == Player.B:
            return self.winReward
        else:
            return self.loseReward

    def render(self):
        print(self.game)
