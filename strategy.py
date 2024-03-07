from abc import abstractmethod
from numpy import random
from board import Board
from copy import deepcopy

class Strategy():
    def __init__(self):
        pass

    @abstractmethod
    def next_move(self, board):
        pass

    def verifyLine(self,board,line):
        freeLines = self.getFreeLines(board)
        for lineTmp in freeLines:
            if (lineTmp[1] == line[0] and lineTmp[2] == line[1]):
                return True
        return False
    
    def getFreeLines(self,board):
        freeLines = []
        for line in board.grid:
            if line[0] == 0:
                freeLines.append(line)
        return freeLines

class Human(Strategy):    
    def next_move(self, board):
        chosenLine = input('Enter the line: ')
        if not chosenLine.isdigit():
            print('Invalid input. Please enter a number.')
            return self.next_move(board)
        else:
            if len(chosenLine) == 4:
                chosenLine = (int(chosenLine[0]), int(chosenLine[1])), (int(chosenLine[2]), int(chosenLine[3]))
                verify = self.verifyLine(board, chosenLine)
                if(verify == False):
                    print('Line already taken. Please enter another line.')
                    return self.next_move(board)
                return [0,chosenLine[0],chosenLine[1]]                
            else:
                print('Invalid input. Please enter 4 numbers.')
                return self.next_move(board)
        

class Random(Strategy):
    def next_move(self, board):
        freeLines = self.getFreeLines(board)
        randomChoice = random.randint(0, len(freeLines) - 1)
        return freeLines[randomChoice]
        

class Greedy(Strategy):
    def next_move(self, board):
        boardTmp = Board()
        scoreTmp = 100000
        freeLines = self.getFreeLines(boardTmp)
        for line in freeLines:
            boardTmp.grid = deepcopy(board.grid)
            boardTmp.make_move(line, -1)
            if boardTmp.get_score(0) < scoreTmp:
                scoreTmp = boardTmp.get_score(0)
                chosenLine = line
                
        return chosenLine

class AlphaBeta(Strategy):
    def __init__(self, depth):
        self.depth = depth

    def next_move(self, board):
        freeLines = self.getFreeLines(board)
        return self.alpha_beta(board, self.depth, -100000, 100000, False, freeLines)[1]
    
    def alpha_beta(self, board, depth, alpha, beta, maximizingPlayer, freeLines):
        chosenLine = None
        if depth == 0 or board.is_full():
            if maximizingPlayer:
                return board.get_score(1) , chosenLine
            else:
                return board.get_score(-1) , chosenLine
        if maximizingPlayer:
            maxEval = -100000
            for line in freeLines:
                boardTmp = Board()
                boardTmp.grid = deepcopy(board.grid)
                boardTmp.make_move(line, 1)
                eval = self.alpha_beta(boardTmp, depth-1, alpha, beta, False, self.getFreeLines(boardTmp))[0]
                if eval > maxEval:
                    chosenLine = line
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, chosenLine
        else:
            minEval = 100000
            for line in freeLines:
                boardTmp = Board()
                boardTmp.grid = deepcopy(board.grid)
                boardTmp.make_move(line, -1)
                eval = self.alpha_beta(boardTmp, depth-1, alpha, beta, True, self.getFreeLines(boardTmp))[0]
                if eval < minEval:
                    chosenLine = line
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval,chosenLine

class MinMax(Strategy):
    def __init__(self, depth):
        self.depth = depth

    def next_move(self, board):
        pass

