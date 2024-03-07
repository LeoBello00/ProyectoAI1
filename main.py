from board import Board
from strategy import Human, Random, Greedy, MinMax, AlphaBeta

def play_game(strategy1, strategy2):
    # Start the game
    print(f"{strategy1.__class__.__name__} VS {strategy2.__class__.__name__}")
    while not board.is_full():
        # Player 1
        move = strategy1.next_move(board)
        print(f"Player 1: {move}")
        board.make_move(move, 1)
        print(board)
        Human().next_move(board)
        if board.is_full():
            if board.get_score() == 0:
                print("It's a draw!")
                return
        if board.get_score() > 0:
            print("Player 1 wins!")
            return
        if board.get_score() < 0:
            print("Player 2 wins!")
            return

        # Player 2
        move = strategy2.next_move(board)
        print(f"Player 2: {move}")
        board.make_move(move, 2)
        print(board)


    if board.get_score() == 0:
        print("It's a draw!")
        return
    if board.get_score() > 0:
        print("Player 1 wins!")
        return
    if board.get_score() < 0:
        print("Player 2 wins!")
        return

if __name__ == '__main__':
    board = Board()
    strategy1 = Random()
    strategy2 = Random()

    play_game(strategy1, strategy2)