from board import Board
from strategy import Human, Random, Greedy, MinMax, AlphaBeta

def play_game(strategy1, strategy2):
    ...

if __name__ == '__main__':
    board = Board()
    print(board)
    strategy1 = Random()
    strategy2 = Random()

    play_game(strategy1, strategy2)