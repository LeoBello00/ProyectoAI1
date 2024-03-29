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
        if self.getFreeLines(self) == []:
            return True

    def getFreeLines(self,board):
        freeLines = []
        for line in board.grid:
            if line[0] == 0:
                freeLines.append(line)
        return freeLines

    def get_score_old(self):
        return self.score

    def get_score1(self,line, lastPlayer):
        if line[1][0] == line[2][0]:
            lineHdown = self.get_edge_from_location((line[1][0] + 1,line[1][1]), (line[2][0] + 1,line[2][1]))
            lineHup = self.get_edge_from_location((line[1][0] - 1,line[1][1]), (line[2][0] - 1,line[2][1]))
            if(lineHup != []):
                if lineHup[0] != 0:                    
                    lineVleft = self.get_edge_from_location((line[1][0]-1, line[1][1]), (line[1][0],line[1][1]))
                    if lineVleft != []:
                        if lineVleft[0] != 0:
                            lineVright = self.get_edge_from_location((line[2][0] - 1,line[2][1]), line[2])
                            if lineVright != []:
                                if lineVright[0] != 0:
                                    self.score += lastPlayer
            if lineHdown != []:
                if lineHdown[0] != 0: 
                    lineVleft = self.get_edge_from_location(line[1], (line[1][0] + 1,line[1][1])) 
                    if lineVleft != []:   
                        if lineVleft[0] != 0:
                            lineVright = self.get_edge_from_location(line[2], (line[2][0] + 1,line[2][1]))
                            if lineVright != []:
                                if lineVright[0] != 0:
                                    self.score += lastPlayer   
        else:
            lineVleft = self.get_edge_from_location((line[1][0],line[1][1] - 1), (line[2][0],line[2][1] - 1))
            lineVright = self.get_edge_from_location((line[1][0],line[1][1] + 1), (line[2][0],line[2][1] + 1))
            if lineVleft != []:
                if lineVleft[0] != 0:
                    lineHup = self.get_edge_from_location((line[1][0],line[1][1]-1), line[1])
                    if lineHup != []:
                        if lineHup[0] != 0:
                            lineHdown = self.get_edge_from_location((line[2][0],line[2][1] - 1), line[2])
                            if lineHdown != []:
                                if lineHdown[0] != 0:
                                    self.score += lastPlayer
            if lineVright != []:
                if lineVright[0] != 0:
                    lineHup = self.get_edge_from_location(line[1], (line[1][0],line[1][1] + 1))
                    if lineHup != []:
                        if lineHup[0] != 0:
                            lineHdown = self.get_edge_from_location(line[2], (line[2][0],line[2][1] + 1))
                            if lineHdown != []:
                                if lineHdown[0] != 0:
                                    self.score += lastPlayer       
        return self.score

    def get_score(self,lastPlayer):
        size = self.size
        winningLines = []
        counter = 1
        counterTaken = 0
        score = 0
        linesToChange = []
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
                    if(line[3] == 0):
                        tmp += 1
                        line[3] = 1
                    for t in linesToChange:
                        if t[3] == 0:
                            t[0] = lastPlayer
                            t[3] = 1
                            tmp += 1
                    if tmp > 0:
                        #print("Player ",lastPlayer," scored ",tmp)
                        score += lastPlayer
            
            linesToChange = []
            counter = 1
            counterTaken = 0

        self.score += score     
        return self.score
    
    def make_move(self, move, player):
        self.get_edge_from_location(move[1], move[2])[0] = player
        pass

    def unmake_move(self, move):
        self.get_edge_from_location(move[1], move[2])[0] = 0
        pass

    def get_edge_from_location(self, location1, location2):
        for edge in self.grid:
            if edge[1] == location1 and edge[2] == location2:
                return edge
        return []

    def get_colour_from_location(self, location1, location2):
        return (self.get_edge_from_location(location1, location2))[0]