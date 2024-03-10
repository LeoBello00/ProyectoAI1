from abc import abstractmethod
from numpy import random
from board import Board
from copy import deepcopy
import concurrent.futures

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
        if len(freeLines) <= 1:
            return freeLines[0]
        randomChoice = random.randint(0, len(freeLines) - 1)
        return freeLines[randomChoice]
        

class Greedy(Strategy):
    def __init__(self,player):
        self.player = player
    def next_move(self, board):
        boardTmp = deepcopy(board)
        scoreTmp = 100000
        freeLines = self.getFreeLines(boardTmp)
        for line in freeLines:
            boardTmp = deepcopy(board)
            boardTmp.make_move(line, self.player)
            if boardTmp.get_score1(line,self.player) < scoreTmp:
                scoreTmp = boardTmp.get_score(0)
                chosenLine = line
                
        return chosenLine

class AlphaBeta(Strategy):
    def __init__(self, depth,player):
        self.depth = depth
        self.player = player

    def next_move(self, board):
        freeLines = self.getFreeLines(board)
        possibileEnd = False
        if len(freeLines) <= self.depth:
            possibileEnd = True
        if self.player == 1:
            results = self.alpha_beta(board, self.depth, -100000, 100000, True, freeLines)
        else:
            results = self.alpha_beta(board, self.depth, -100000, 100000, False, freeLines)
        text_file = open("AlphaBeta.txt", "w")
        txt = results[2]
        txt += "\nFinal decision:\nChosenLine " + str(results[1]) + "\n" + "Eval " + str(results[0]) + "\n"
        if possibileEnd:
            txt += "Possibile end of game:\n"
            if results[0] == 0:
                txt += "It's a draw!\n"
            elif results[0] > 0:
                txt += "Player 2 wins!\n"
            else:
                txt += "Player 1 wins!\n"
        text_file.write(txt)
        text_file.close()
        return results[1]
    
    def alpha_beta(self, board, depth, alpha, beta, maximizingPlayer, freeLines):
        chosenLine = None
        log = ""
        if depth == 0 or board.is_full():
            return  board.get_score(0), chosenLine, ""
        if maximizingPlayer:         
            maxEval = -100000
            scoreTmp = [board.get_score_old(),board.get_score_old()]
            for line in freeLines:
                boardTmp = deepcopy(board)
                boardTmp.make_move(line, 1)
                scoreTmp[0] = boardTmp.get_score1(line,1)
                if scoreTmp[0] == scoreTmp[1]:
                    if depth != 1:
                        #indexTmp = freeLines.index(line)
                        #freeLineTmp = freeLines.pop(indexTmp)
                        results = self.alpha_beta(boardTmp, depth-1, alpha, beta, False, self.getFreeLines(boardTmp))
                        eval = results[0]
                        log += results[2]
                        #freeLines.insert(indexTmp,freeLineTmp)
                    else:
                        eval = scoreTmp[0]
                else:
                    scoreTmp[1] = scoreTmp[0]
                    #indexTmp = freeLines.index(line)
                    #freeLineTmp = freeLines.pop(indexTmp)
                    results = self.alpha_beta(boardTmp, depth - 1, alpha, beta, True, self.getFreeLines(boardTmp))
                    eval = results[0]
                    log += results[2]
                    #freeLines.insert(indexTmp,freeLineTmp)
                    #sprint("eval ",eval)
                if eval > maxEval:
                    #print("Maxeval ",eval, " ChosenLine ",line)
                    log += "\nMaxeval " + str(eval) + " ChosenLine " + str(line) + "\n"
                    #log += boardTmp.__str__()
                    chosenLine = line
                    maxEval = eval
                if alpha <= eval:
                    alpha = eval
                    if beta <= alpha:
                        break
            return maxEval, chosenLine , log
        else:
            minEval = 100000
            scoreTmp = [board.get_score_old(),board.get_score_old()]
            for line in freeLines:  
                boardTmp = deepcopy(board)          
                boardTmp.make_move(line, -1)
                scoreTmp[0] = boardTmp.get_score1(line,-1)
                if scoreTmp[0] == scoreTmp[1]:
                    if depth != 1:
                        #indexTmp = freeLines.index(line)
                        #freeLineTmp = freeLines.pop(indexTmp)
                        results = self.alpha_beta(boardTmp, depth-1, alpha, beta, True, self.getFreeLines(boardTmp))
                        eval = results[0]
                        log += results[2]
                        #freeLines.insert(indexTmp,freeLineTmp)
                    else:
                        eval = scoreTmp[0]
                else:
                    scoreTmp[1] = scoreTmp[0]
                    #indexTmp = freeLines.index(line)
                    #freeLineTmp = freeLines.pop(indexTmp)
                    results = self.alpha_beta(boardTmp, depth -1, alpha, beta, False, self.getFreeLines(boardTmp))
                    eval = results[0]
                    log += results[2]
                    #freeLines.insert(indexTmp,freeLineTmp)
                if eval < minEval:
                    log += "\nMineval " + str(eval) + " ChosenLine " + str(line) + "\n"
                    #log += boardTmp.__str__()
                    #print("Mineval ",eval, " ChosenLine ",line)
                    chosenLine = line
                    minEval = eval
                if beta >= eval:
                    beta = eval
                    if beta <= alpha:
                        break
            return minEval,chosenLine , log

class MinMax(Strategy):
    def __init__(self, depth):
        self.depth = depth

    def next_move(self, board):
        chosenLine = self.min_max(board, False, self.depth)[1]
        return chosenLine
    
    def min_max(self,board,maximazingPlayer,depth):
        chosenLine = None
        
        if depth == 0 or board.is_full():
            #print(board.get_score1(line,1))
            return board.get_score(0), chosenLine
        elif maximazingPlayer:
            maxEval = -100000
            for line in self.getFreeLines(board):
                boardTmp = deepcopy(board)
                boardTmp.make_move(line, 1)
                boardTmp.get_score1(line,1)
                eval = self.min_max(boardTmp, False, depth-1)[0]
                if eval > maxEval:
                    chosenLine = line
                    maxEval = eval
                maxEval = max(maxEval, eval)
            return maxEval, chosenLine
        else:       
            minEval = 100000
            for line in self.getFreeLines(board):
                boardTmp = deepcopy(board)
                boardTmp.make_move(line, -1)
                boardTmp.get_score1(line,-1)
                eval = self.min_max(boardTmp, True, depth-1)[0]
                if eval < minEval:
                    chosenLine = line 
                    minEval = eval
                    if(depth == 3):
                        print("mineval ",minEval)
                minEval = min(minEval, eval)
            return minEval, chosenLine

