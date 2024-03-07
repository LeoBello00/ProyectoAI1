from utils import return_text_colour

class Board():
    def __init__(self, size=3):
        self.size = size
        # edge : [idx_colour, (i, j), (i', j')]
        self.grid = []
        for i in range(size + 1):
            for j in range(size + 1):
                if i != size:
                    self.grid.append([0, (i, j), (i+1, j)])
                if j != size:
                    self.grid.append([0, (i, j), (i, j+1)])
        self.grid[0][0] = 1
            
        

    def __str__(self):
        board_str = ""
        for j in range(self.size * 2 + 1):
            for i in range(self.size):
                if i % 2 == 0 and j % 2 == 0:
                    board_str += "."
                    board_str += "____"  # Ligne horizontale
                elif i % 2 == 0:
                    idx = (i // 2) + (j // 2) * (self.size - 1)
                    board_str += "|" + return_text_colour("    ", self.grid[idx][0])  # Espace entre les lignes verticales
                elif j % 2 == 0:
                    idx = (i // 2) + (j // 2) * self.size
                    board_str += "."
                    board_str += return_text_colour("____", self.grid[idx][0])  # Ligne horizontale
                else:
                    idx = (i // 2) + (j // 2) * (self.size - 1)
                    board_str += "|" + return_text_colour("    ", self.grid[idx][0])  # Espace entre les lignes horizontales
            board_str += "|\n"
        return board_str + str(self.grid)
    
    def is_full(self):
        pass

    def get_score(self,lastPlayer):
        size = self.size
        winningLines = []
        counter = 0
        counterTaken = 0
        score = 0
        for line in self.grid:
            if line[0] != 0:
                winningLines.append(line)
        for line in winningLines:
            if(line[0] != lastPlayer):
                counterTaken += 1
            for line2 in winningLines:
                if line != line2:
                    if line2[0] != lastPlayer:
                        counterTaken += 1
                    if line[1] == line2[1]:
                        if (line2[2][0] == line2[1][0] + 1 and line2[2][1] == line2[1][1]):
                            counter += 1
                    elif (line2[1][0] == line[1][0] + 1 )and (line2[1][1] == line[1][1]) and (line2[2][0] == line[2][0]+1) and (line2[2][1] == line[2][1]):
                        counter += 1
                    elif line[2] == line2[1]:
                        if (line2[2][0] == line2[1][0] + 1 and line2[2][1] == line2[1][1]):
                            counter += 1
            if counter == 3:
                if(counterTaken != 4):
                    score += lastPlayer
                else:
                    score -= lastPlayer

             
        return 1
    
    def make_move(self, move, player):
        pass