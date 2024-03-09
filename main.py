from board import Board
from strategy import Human, Random, Greedy, MinMax, AlphaBeta

def check_winner(board):
    if board.is_full():
        if board.get_score(0) == 0:
            print("It's a draw!")
            return True
        if board.get_score(0) < 0:
            print("Player 1 wins!")
            return True
        if board.get_score(0) > 0:
            print("Player 2 wins!")
            return True
    return False

def play_game(strategy1, strategy2):
    # Start the game
    print(f"{strategy1.__class__.__name__} VS {strategy2.__class__.__name__}")
    score = 0
    newScore = 0
    while not board.is_full():
        # Player 1
        if newScore == score:
            score = newScore
            move = strategy1.next_move(board)
            board.make_move(move, -1)
            newScore = board.get_score1(move, -1)
            print(newScore)
            print(board)
        else: 
            score = newScore
        if check_winner(board):
            return
        if newScore == score:
            score = newScore
            chosenMove =strategy2.next_move(board)
            board.make_move(chosenMove, 1)
            newScore = board.get_score1(chosenMove,1)
            print(newScore)
            print(board)
        else:
            score = newScore
        
        if check_winner(board):
            return

        # Player 2
        #move = strategy2.next_move(board)
        #print(f"Player 2: {move}")
        #board.make_move(move, 2)
        #print(board)


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
    strategy1 = Human()
    strategy2 = AlphaBeta(2, 1)

    play_game(strategy1, strategy2)