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
        mtx_str = [["0"]*(3*(self.size+1)+1) for _ in range(2*self.size + 1)]
        for idx_line, line in enumerate(mtx_str):
            if idx_line == 0:
                for idx_chr, chr in enumerate(line):
                    if (1+idx_chr) % 4 == 1:
                        line[idx_chr] = " "
            elif idx_line != 0 and idx_line % 2 == 1:
                for idx_chr, chr in enumerate(line):
                    if (idx_chr) % 4 != 0:
                        line[idx_chr] = " "

        # board_str = ""
        # line0 = []
        # lines_txt = line0 + [[] for _ in range(2*self.size + 1)]
        # for edge in self.grid:
        #     idx_line = edge[]
        #     if num % 2 == 0:
        #         ...
        #     else:
        #         ...

        # line0 = [" "]
        # for line in range(self.size):
        #     line0.append(return_text_colour("_"*3, self.grid[i][0], end=" "))
        #     # for edge in self.grid:
        #     #     if edge[2][1] - edge[1][1] == 1: #it's an horizontal edge
        #     #         line0.append(return_text_colour("|", edge[0], end=" "))
        #     # colour0 = edge[0]
        # board_str += "".join(line0) + "\n"

        # for i in range(2*(self.size+1)+2):
        #     for j in range(self.size):
        #         line1.append([
        #             [return_text_colour("|", self.grid[1 + i//2][0], end="") +" "*3]
        #             for j in range(self.size)].flatten()

        #         )
        #     line1 = []
        #     line2 = []
        #     board_str += "".join(["|" + " "*3 for _ in range(self.size)] + ["|"]) + "\n"
        #     board_str += "".join(["|" + "_"*3 for _ in range(self.size)] + ["|"]) + "\n"
        for line in mtx_str:
            print(line)
        board_str = ""
        return board_str
    
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

    def get_edge_from_location(self, location1, location2):
        for edge in self.grid:
            if edge[1] == location1 and edge[2] == location2:
                return edge

    def get_colour_from_location(self, location1, location2):
        return self.get_edge_from_location(location1, location2)[0]