from player import Player
from square import Square
from winner import Winner

class Game:
    def __init__(self):
        self.size = 6

        self.restart()

    def restart(self):
        self.initializeGrid()
        self.initializePlayers()

    def initializeGrid(self):
        self.grid = [[Square() for j in range(self.size)] for i in range(self.size)]

    def initializePlayers(self):
        self.currentPlayer = Player.A
        self.availableSquaresForA = 0
        self.highestContentForA = 1
        self.setSquare(0, 0, Player.A, 1)
        self.updateAvailableSquares(self.getNeighborSquares(0, 0))

        self.currentPlayer = Player.B
        self.availableSquaresForB = 0
        self.highestContentForB = 1
        self.setSquare(self.size-1, self.size-1, Player.B, 1)
        self.updateAvailableSquares(self.getNeighborSquares(self.size-1, self.size-1))

        self.currentPlayer = Player.A

    def updateGrid(self, row, col):
        allNeighbors = self.getNeighborSquares(row, col)
        filledNeighbors = [n for n in allNeighbors if not n.isEmpty]
        sameTeamNeighbors = [n for n in filledNeighbors if n.player == self.currentPlayer]

        if len(sameTeamNeighbors) > 0:
            largestNeighbor = max(sameTeamNeighbors, key=lambda n: n.content)

            content = largestNeighbor.content + 1
            
            self.setSquare(row, col, self.currentPlayer, content)
            self.updateHighestContent(content)
            self.updateAvailableSquares(allNeighbors)
            self.updateCurrentPlayer()

    def updateAvailableSquares(self, neighbors):
        emptyNeighbors = [n for n in neighbors if n.isEmpty]
        makeAvailable = [n for n in emptyNeighbors if not n.isAvailable(self.currentPlayer)]
        makeAvailableLength = len(makeAvailable)
        
        for neighbor in makeAvailable:
            neighbor.makeAvailable(self.currentPlayer)

        if self.currentPlayer == Player.A:
            self.availableSquaresForA += makeAvailableLength
        elif self.currentPlayer == Player.B:
            self.availableSquaresForB += makeAvailableLength

    def updateHighestContent(self, content):
        if self.currentPlayer == Player.A:
            self.highestContentForA = max(content, self.highestContentForA)
        elif self.currentPlayer == Player.B:
            self.highestContentForB = max(content, self.highestContentForB)

    def updateCurrentPlayer(self):
        #if self.currentPlayer == Player.A:
        #    if self.availableSquaresForB > 0:
        #        self.currentPlayer = Player.B
        #    else:
        #        self.currentPlayer = Player.A
        #elif self.currentPlayer == Player.B:
        #    if self.availableSquaresForA > 0:
        #        self.currentPlayer = Player.A
        #    else:
        #        self.currentPlayer = Player.B
        if self.currentPlayer == Player.A:
            self.currentPlayer = Player.B
        else:
            self.currentPlayer = Player.A
                
    def isGameOver(self):
        return (self.availableSquaresForA == 0 and self.availableSquaresForB == 0)

    def getWinner(self):
        if not self.isGameOver():
            return Winner.NotOver
        elif self.highestContentForA == self.highestContentForB:
            return Winner.Tie
        elif self.highestContentForA > self.highestContentForB:
            return Winner.A
        else:
            return Winner.B

    def isSquareAvailable(self, row, column):
        return self.grid[row][column].isAvailable(self.currentPlayer)

    def getNeighborSquares(self, row, col):
        neighbors = []

        if row > 0:
          # Top
          neighbors.append(self.grid[row-1][col])
        
        if col > 0:
          # Left
          neighbors.append(self.grid[row][col-1])
        
        if row < self.size-1:
          # Bottom
          neighbors.append(self.grid[row+1][col])
        
        if col < self.size-1:
          # Right
          neighbors.append(self.grid[row][col+1])
        
        if row > 0 and col > 0:
          # Top-left
          neighbors.append(self.grid[row-1][col-1])
        
        if row < self.size-1 and col > 0:
          # Bottom-left
          neighbors.append(self.grid[row+1][col-1])
        
        if row > 0 and col < self.size-1:
          # Top-right
          neighbors.append(self.grid[row-1][col+1])
        
        if row < self.size-1 and col < self.size-1:
          # Bottom-right
          neighbors.append(self.grid[row+1][col+1])
        

        return neighbors
    
    def setSquare(self, row, col, player, content):
        square = self.grid[row][col]
        square.player = player
        square.content = content
        square.isEmpty = False

        if square.isAvailableForA:
            self.availableSquaresForA -= 1
        if square.isAvailableForB:
            self.availableSquaresForB -= 1

        square.isAvailableForA = False
        square.isAvailableForB = False
    
    def __str__(self):
        string = ""
        for row in self.grid:
            for square in row:
                string += str(square) + " "
            
            string += "\n"

        return string
