from board import Board
from strategy import Random, Greedy, MinMax, AlphaBeta

def play_game(strategy1, strategy2):
    print(f"{strategy1.__class__.__name__} VS {strategy2.__class__.__name__}")

if __name__ == '__main__':
    board = Board()
    strategy1 = Random()
    strategy2 = Random()

    play_game(strategy1, strategy2)