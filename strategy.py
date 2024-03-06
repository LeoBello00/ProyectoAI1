from abc import abstractmethod

class Strategy():
    def __init__(self):
        pass

    @abstractmethod
    def next_move(self, board):
        pass

class Human(Strategy):
    def next_move(self, board):
        pass

class Random(Strategy):
    def next_move(self, board):
        pass

class Greedy(Strategy):
    def next_move(self, board):
        pass

class MinMax(Strategy):
    def __init__(self, depth):
        self.depth = depth

    def next_move(self, board):
        pass

class AlphaBeta(Strategy):
    def __init__(self, depth):
        self.depth = depth

    def next_move(self, board):
        pass