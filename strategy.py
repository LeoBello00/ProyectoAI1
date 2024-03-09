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
        if self.player == 1:
            return self.alpha_beta(board, self.depth, -100000, 100000, True, freeLines)[1]
        else:
            return self.alpha_beta(board, self.depth, -100000, 100000, False, freeLines)[1]
    
    def next_move1(self, board):
        free_lines = self.getFreeLines(board)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a list of future objects representing the evaluations of each move
            futures = [executor.submit(self.alpha_beta_worker, board, self.depth, -float('inf'), float('inf'), False, line) for line in free_lines]

            # Gather the results
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # Find the best move based on the results
        print(results)
        if(len(results) == 1):
            return results[0][1]
        best_score = min(results[1:])[0]
        for score, line in results[1:]:
            if score == best_score:
                best_line = line
        return best_line
    
    def alpha_beta_worker(self, board, depth, alpha, beta, maximizing_player, line):
        chosen_line = None

        if depth == 0 or board.is_full():
            return board.get_score(0), chosen_line

        if maximizing_player:
            max_eval = -float('inf')
            score_tmp = [board.get_score_old(), board.get_score_old()]

            board_tmp = deepcopy(board)
            board_tmp.make_move(line, 1)
            score_tmp[0] = board_tmp.get_score1(line, 1)

            if score_tmp[0] == score_tmp[1]:
                if depth != 1:
                    eval = self.alpha_beta(board_tmp, depth - 1, alpha, beta, False, self.getFreeLines(board_tmp))[0]
                else:
                    eval = score_tmp[0]
            else:
                score_tmp[1] = score_tmp[0]
                eval = self.alpha_beta(board_tmp, depth - 1, alpha, beta, True, self.getFreeLines(board_tmp))[0]

            if eval > max_eval:
                chosen_line = line
                max_eval = eval

            if alpha <= eval:
                alpha = eval
                if beta <= alpha:
                    return max_eval, chosen_line

        else:
            min_eval = float('inf')
            score_tmp = [board.get_score_old(), board.get_score_old()]

            board_tmp = deepcopy(board)
            board_tmp.make_move(line, -1)
            score_tmp[0] = board_tmp.get_score1(line, -1)

            if score_tmp[0] == score_tmp[1]:
                if depth != 1:
                    eval = self.alpha_beta(board_tmp, depth - 1, alpha, beta, True, self.getFreeLines(board_tmp))[0]
                else:
                    eval = score_tmp[0]
            else:
                score_tmp[1] = score_tmp[0]
                eval = self.alpha_beta(board_tmp, depth - 1, alpha, beta, False, self.getFreeLines(board_tmp))[0]

            if eval < min_eval:
                chosen_line = line
                min_eval = eval
            if beta >= eval:
                beta = eval
                if beta <= alpha:
                    return min_eval, chosen_line

        return max_eval if maximizing_player else min_eval, chosen_line
    
    def alpha_beta(self, board, depth, alpha, beta, maximizingPlayer, freeLines):
        chosenLine = None

        if depth == 0 or board.is_full():
            return  board.get_score(0), chosenLine
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
                        eval = self.alpha_beta(boardTmp, depth-1, alpha, beta, False, self.getFreeLines(boardTmp))[0]
                        #freeLines.insert(indexTmp,freeLineTmp)
                    else:
                        eval = scoreTmp[0]
                else:
                    scoreTmp[1] = scoreTmp[0]
                    #indexTmp = freeLines.index(line)
                    #freeLineTmp = freeLines.pop(indexTmp)
                    eval = self.alpha_beta(boardTmp, depth - 1, alpha, beta, True, self.getFreeLines(boardTmp))[0]
                    #freeLines.insert(indexTmp,freeLineTmp)
                    #sprint("eval ",eval)
                if eval > maxEval:
                    #print("Maxeval ",eval, " ChosenLine ",line)
                    chosenLine = line
                    maxEval = eval
                if alpha <= eval:
                    alpha = eval
                    if beta <= alpha:
                        break
            return maxEval, chosenLine
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
                        eval = self.alpha_beta(boardTmp, depth-1, alpha, beta, True, self.getFreeLines(boardTmp))[0]
                        #freeLines.insert(indexTmp,freeLineTmp)
                    else:
                        eval = scoreTmp[0]
                else:
                    scoreTmp[1] = scoreTmp[0]
                    #indexTmp = freeLines.index(line)
                    #freeLineTmp = freeLines.pop(indexTmp)
                    eval = self.alpha_beta(boardTmp, depth -1, alpha, beta, False, self.getFreeLines(boardTmp))[0]
                    #freeLines.insert(indexTmp,freeLineTmp)
                if eval < minEval:
                    #print("Mineval ",eval, " ChosenLine ",line)
                    chosenLine = line
                    minEval = eval
                if beta >= eval:
                    beta = eval
                    if beta <= alpha:
                        break
            return minEval,chosenLine

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

