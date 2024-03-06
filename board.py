from utils import print_colour

class Board():
    def __init__(self, size=3):
        self.size = size
        # edge : [colour, (i, j), (i', j')]
        self.grid = []
        for j in range(size-1):
            for i in range(size-1):
                self.grid.append(["black", (i, j), (i+1, j)])
                self.grid.append(["black", (i, j+1), (i+1, j+1)])
    
    def __str__(self):
        for line in self.grid:
            for edge in line:
                print_colour("___", edge[0])
            
    
    def is_full(self):
        pass

    def get_score(self):
        return 1
    
    def make_move(self, move, player):
        pass