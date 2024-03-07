from utils import return_text_colour

class Board():
    def __init__(self, size=3):
        self.size = size
        # edge : [idx_colour, (i, j), (i', j')]
        self.grid = []
        self.score = 0
        for i in range(size + 1):
            for j in range(size + 1):
                if i != size:
                    self.grid.append([0, (i, j), (i+1, j),0])
                if j != size:
                    self.grid.append([0, (i, j), (i, j+1),0])
            
        

    def __str__(self):
        mtx_str = [["0"]*(3*(self.size+1)+1) for _ in range(2*self.size + 1)]
        for idx_line, line in enumerate(mtx_str):
            if idx_line % 2 == 1:
                for idx_chr, _ in enumerate(line):
                    if (idx_chr) % 4 != 0:
                        line[idx_chr] = " "
                    else:
                        colour = self.get_colour_from_location((idx_line//2, idx_chr//4), (idx_line//2+1, idx_chr//4))
                        line[idx_chr] = return_text_colour("|", colour, end="")
            else:
                for idx_chr, _ in enumerate(line):
                    if (idx_chr) % 4 == 0:
                        if idx_line == 0:
                            continue
                        colour = self.get_colour_from_location((idx_line//2-1, idx_chr//4), (idx_line//2, idx_chr//4))
                        line[idx_chr] = return_text_colour("|", colour, end="")
                    else:
                        colour = self.get_colour_from_location((idx_line//2, idx_chr//4), (idx_line//2, idx_chr//4+1))
                        line[idx_chr] = return_text_colour("_", colour, end="")
        for idx, _ in enumerate(mtx_str[0]):
            if idx % 4 == 0:
                mtx_str[0][idx] = " "
        return "".join(["".join(line) + "\n" for line in mtx_str])
    
    def change_colour(self, location1, location2, colour):
        for edge in self.grid:
            if edge[1] == location1 and edge[2] == location2:
                edge[0] = colour
    
    def is_full(self):
        pass

    def get_score(self,lastPlayer):
        size = self.size
        winningLines = []
        counter = 1
        counterTaken = 0
        score = 0
        linesToChange = []
        if lastPlayer == 0:
            lastPlayer = -1
        for line in self.grid:
            if line[0] != 0:
                winningLines.append(line)
        for line in winningLines:
            if(line[0] != lastPlayer):
                counterTaken += 1
            for line2 in winningLines:
                if line[1][0] != line[2][0]:
                    break
                if line != line2:
                    
                    if line[1] == line2[1]:
                        if (line2[2][0] == line2[1][0] + 1 and line2[2][1] == line2[1][1]):
                            counter += 1
                            if line2[0] != lastPlayer:
                                counterTaken += 1
                            linesToChange.append(line2)
                    elif (line2[1][0] == line[1][0] + 1 )and (line2[1][1] == line[1][1]) and (line2[2][0] == line[2][0]+1) and (line2[2][1] == line[2][1]):
                        counter += 1
                        if line2[0] != lastPlayer:
                                counterTaken += 1
                        linesToChange.append(line2)
                    elif line[2] == line2[1]:
                        if (line2[2][0] == line2[1][0] + 1 and line2[2][1] == line2[1][1]):
                            counter += 1
                            if line2[0] != lastPlayer:
                                counterTaken += 1
                            linesToChange.append(line2)
            if counter == 4:
                if(counterTaken != 4):
                    tmp = 0
                    for line in linesToChange:
                        if line[3] == 0:
                            line[0] = lastPlayer
                            line[3] = 1
                            tmp += 1
                    if(line[3] == 0):
                        tmp += 1
                    if tmp > 0:
                        score += lastPlayer
            
            linesToChange = []
            counter = 1
            counterTaken = 0

        self.score += score     
        return self.score
    
    def make_move(self, move, player):
        self.get_edge_from_location(move[1], move[2])[0] = player
        pass

    def get_edge_from_location(self, location1, location2):
        for edge in self.grid:
            if edge[1] == location1 and edge[2] == location2:
                return edge

    def get_colour_from_location(self, location1, location2):
        return (self.get_edge_from_location(location1, location2))[0]