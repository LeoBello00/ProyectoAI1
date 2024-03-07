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
        self.change_colour((0, 0), (0, 1), 1)
        self.change_colour((size, size-1), (size, size), -1)

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
        pass
    
    def make_move(self, move, player):
        pass

    def get_edge_from_location(self, location1, location2):
        for edge in self.grid:
            if edge[1] == location1 and edge[2] == location2:
                return edge

    def get_colour_from_location(self, location1, location2):
        return (self.get_edge_from_location(location1, location2))[0]