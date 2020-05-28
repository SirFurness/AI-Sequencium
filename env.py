import math

from player import Player
from winner import Winner
from game import Game

import os
import time

import torch

class Environment:
    def __init__(self):
        self.game = Game()

        self.winReward = 1
        self.loseReward = -1
        self.tieReward = 0
        self.notOverReward = 0

    def reset(self):
        self.game.restart()

    def getValidActions(self):
        availableCoordinates = [(row, col) 
                for row in range(self.game.size)
                for col in range(self.game.size)
                if self.game.isSquareAvailable(row, col)]

        availableActions = [self.convertCoordinateToAction(coord)
                for coord in availableCoordinates]

        if len(availableActions) == 0:
            availableActions = [36]

        return availableActions

    def step(self, action):
        self.applyAction(action)
        
        newState = self.getState()
        reward = self.getReward()
        isDone = self.game.isGameOver()

        return (newState, reward, isDone)

    def applyAction(self, action):
        # no-move action
        if action == 36:
            self.game.updateCurrentPlayer()
            return

        coordinate = self.convertActionToCoordinate(action)
        self.game.updateGrid(coordinate[0], coordinate[1]) 

    def convertActionToCoordinate(self, action):
        row = math.trunc(action / self.game.size)
        col = action % self.game.size

        return (row, col)

    def convertCoordinateToAction(self, coord):
        row, col = coord  

        return row*self.game.size + col

    def getState(self, flip=False):
        # flattens the list
        state = [self.getSquareContent(square, flip)
                for row in self.game.grid for square in row]

        if flip:
            state.reverse()

        if flip:
            state.append(self.game.highestContentForB)
            state.append(self.game.highestContentForA)
        else:
            state.append(self.game.highestContentForA)
            state.append(self.game.highestContentForB)

        return state

    def getStateTensor(self, flip=False):
        stateList = self.getState(flip)

        return torch.tensor(stateList, dtype=torch.float)

    def getStateNotFlat(self):
        return [[self.getSquareContent(square) for square in row]
                for row in self.game.grid]

    def getSquareContent(self, square, flip=False):
        scale = 1
        if flip:
            scale = -1

        if square.player == Player.A:
            return square.content * scale
        elif square.player == Player.B:
            return square.content * -1 * scale
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
        elif winner == Winner.A:
            return self.winReward
        else:
            return self.loseReward
        #elif winner == Winner.A and player == Player.A:
        #    return self.winReward
        #elif winner == Winner.B and player == Player.B:
        #    return self.winReward
        #else:
        #    return self.loseReward

    def render(self):
        state = self.getStateNotFlat()
        maxSpacing = 4

        os.system("cls||clear")
        for row in state:
            for num in row:
                spacing = maxSpacing - len(str(num))
                for i in range(spacing):
                    print(" ", end='')
                print(str(num), end='') 
            for j in range(maxSpacing-2):
                print("")
        time.sleep(1)
