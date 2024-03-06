class Board():
    def __init__(self, size=3):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board])
    
    def is_full(self):
        pass

    def get_score(self):
        return 1
    
    def make_move(self, move, player):
        pass