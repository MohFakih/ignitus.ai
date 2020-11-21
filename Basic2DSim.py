import numpy as np


class World:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.grid = None
        self.init_grid()
    
    def load_world_from_file(self, filename):
        f = open(filename, 'r')
        s = f.read()
        self.load_world_from_string(s)

    def load_world_from_string(self, s):
        lines = s.splitlines()
        self.W, self.H = [int(v) for v in lines[0].split()]
        self.load_grid_from_string_list(lines[1:])

    def load_grid_from_string_list(self, s_list):
        self.init_grid()
        for line in s_list:
            x, y, block_type = line.split()
            x, y = int(x), int(y)
            self.grid[x][y] = Cell((x, y), self, self.grid, block_type=block_type)

    def load_grid_from_string(self, s):
        self.load_grid_from_string_list(s.splitlines())

    def serialize(self):
        s = str(self.W) + " " + str(self.H) + "\n"
        for cell in self.list_cells():
            s += cell.serialize()
        return s
    
    def create_empty_grid(self):
        newGrid = [None]*self.H
        for i in range(self.H):
            newGrid[i] = [None] * self.W
        return newGrid

    def init_grid(self, default_type='air'):
        """
            Initialize the grid and fill it with default block types
        """
        self.grid = self.create_empty_grid()

        for x in range(self.H):
            for y in range(self.W):
                self.grid[x][y] = Cell((x, y), self, self.grid, default_type)
    
    def list_cells(self):
        L = []
        for x in range(self.H):
            for y in range(self.W):
                L.append(self.grid[x][y])
        return L

    def __str__(self):
        s = "+" + " -"*self.W + "+\n"
        for row in self.grid:
            s += "|"
            for cell in row:
                s += " "+str(cell)
            s += "|\n"
        s += "+" + " -"*self.W + "+\n"
        return s
    
    def step(self):
        newGrid = self.create_empty_grid()
        for old_cell in self.list_cells():
            x = old_cell.x
            y = old_cell.y

            countVicinitylames = 0
            for vicinity_cell in old_cell.list_vicinity_cells():
                if vicinity_cell.block.block_type == 'fire':
                    countVicinitylames += 1

            foundAdjacentFlammable = False
            for adjacent_cell in old_cell.list_adjacent_cells():
                if adjacent_cell.block.block_type == 'wood':
                    foundAdjacentFlammable = True
                    break
            
            if old_cell.block.block_type == 'fire':
                # Check for flammable adjacent:
                if not foundAdjacentFlammable:
                    newGrid[x][y] = Cell((x, y), self, newGrid, 'air')
                else:
                    # Check for flames in the vicinity
                    if countVicinitylames < 4 and np.random.randn() < 0.2:
                        newGrid[x][y] = Cell((x, y), self, newGrid, 'air')
                    else:
                        newGrid[x][y] = Cell((x, y), self, newGrid, 'fire')
            elif old_cell.block.block_type == 'air':
                if foundAdjacentFlammable:
                    probability_of_fire = 0.04*countVicinitylames
                    if np.random.randn() < probability_of_fire:
                        newGrid[x][y] = Cell((x, y), self, newGrid, 'fire')
                    else:
                        newGrid[x][y] = Cell((x, y), self, newGrid, 'air')
                else:
                    newGrid[x][y] = Cell((x, y), self, newGrid, 'air')
            else:
                newGrid[x][y] = Cell((x, y), self, newGrid, old_cell.block.block_type)
        self.grid = newGrid


class Cell:
    def __init__(self, coords, parent_world, parent_grid, block_type='air'):
        self.x, self.y = coords
        self.parent_world = parent_world
        self.parent_grid = parent_grid
        self.block = Block(self, block_type)
    
    # TODO: ALL OF THIS CAN BE PRECOMPUTED. i.e.: for each cell, have the indices of its vicnity/adjacents precomputed in some structure instead of computing them when needed.
    def list_cells_k_distant(self, k):
        L = []
        for i in range(-k, k+1):
            if not (self.x + i < 0 or self.x + i >= self.parent_world.H):
                for j in range(-k, k+1):
                    if not(i == 0 and j == 0):
                        if not (self.y + j < 0 or self.y + j >= self.parent_world.W):
                            L.append(self.parent_grid[self.x+i][self.y+j])
        return L
    def list_adjacent_cells(self):
        return self.list_cells_k_distant(k=1)
    def list_vicinity_cells(self):
        return self.list_cells_k_distant(k=2)
    
    def serialize(self):
        return str(self.x) + " " + str(self.y) + " " + self.block.block_type+"\n"

    def __str__(self):
        return str(self.block)


type_to_char = {}
type_to_char['air']  =' '
type_to_char['fire'] ='X'
type_to_char['block']='#'
type_to_char['wood'] ='W'
class Block:
    def __init__(self, occupying_cell, block_type='air'):
        self.block_type = block_type
        self.occupying_cell = occupying_cell
    
    def __str__(self):
        return type_to_char[self.block_type]



