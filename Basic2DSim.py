import numpy as np
import pygame


TYPE_TO_CHAR = {}
TYPE_TO_CHAR['air']  =' '
TYPE_TO_CHAR['fire'] ='X'
TYPE_TO_CHAR['block']='#'
TYPE_TO_CHAR['wood'] ='W'


BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BROWN = (150, 100, 50)

def passthrough(x):
    return x

def prettyGrid(grid, f=passthrough):
    W = len(grid[0])
    s = "+" + " -"*W + "+\n"
    for row in grid:
        s += "|"
        for cell in row:
            s += " "+str(f(cell))
        s += "|\n"
    s += "+" + " -"*W + "+\n"
    return s


class CellFactory:
    def __init__(self, parent_world, parent_grid):
        self.parent_world = parent_world
        self.parent_grid = parent_grid
    
    def createCell(self, coords, block_type):
        if block_type == 'air':
            return Cell_AIR(coords, self.parent_world, self.parent_grid)
        elif block_type == 'fire':
            return Cell_FIRE(coords, self.parent_world, self.parent_grid)
        elif block_type == 'wood':
            return Cell_WOOD(coords, self.parent_world, self.parent_grid)



class World:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self.grid = None
        self.init_grid()
    
    def _dbg_adjacent_flammable_grid(self):
        adjFlameGrid = self.create_empty_grid()
        for cell in self.list_cells():
            adjFlameGrid[cell.x][cell.y] = cell.foundAdjacentFlammable
        return adjFlameGrid
    
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
        cellFactory = CellFactory(self, self.grid)
        for line in s_list:
            x, y, block_type = line.split()
            x, y = int(x), int(y)
            self.grid[x][y] = cellFactory.createCell((x, y), block_type)
        self.propagate()

    def load_grid_from_string(self, s):
        self.load_grid_from_string_list(s.splitlines())

    def serialize(self):
        s = str(self.W) + " " + str(self.H) + "\n"
        for cell in self.list_cells():
            serialized_cell = cell.serialize()
            if serialized_cell != None:
                s += serialized_cell
        return s
    
    def create_empty_grid(self):
        newGrid = [None]*self.H
        for i in range(self.H):
            newGrid[i] = [None] * self.W
        return newGrid

    def init_grid(self, block_type='air'):
        """
            Initialize the grid and fill it with default block types
        """
        self.grid = self.create_empty_grid()
        cellFactory = CellFactory(self, self.grid)
        for x in range(self.H):
            for y in range(self.W):
                self.grid[x][y] = cellFactory.createCell((x, y), block_type)
        self.propagate()
    
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
    
    def draw(self, screen, block_width, block_height, debug=None):
        for cell in self.list_cells():
            cell.draw(screen, block_width, block_height, debug)

    def step(self):
        newGrid = self.create_empty_grid()
        for old_cell in self.list_cells():
            x = old_cell.x
            y = old_cell.y
            newGrid[x][y] = old_cell.step(self, newGrid)
        self.grid = newGrid
        self.propagate()
    
    def propagate(self):
        for cell in self.list_cells():
            cell.propagate(self.grid, self)

class Cell:
    def __init__(self, coords, parent_world, parent_grid, block_type='air'):
        self.x, self.y = self.coords = coords
        self.parent_world = parent_world
        self.parent_grid = parent_grid
        self.block_type =  block_type
        self.foundAdjacentFlammable = False
        self.countVicinitylames = 0
        self.color = BLACK
    
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
    
    def addAdjacentFlammable(self):
        self.foundAdjacentFlammable = True

    def addVicinityFlame(self):
        self.countVicinitylames += 1

    def serialize(self):
        if self.block_type == 'air':
            return None
        return str(self.x) + " " + str(self.y) + " " + self.block_type+"\n"

    def __str__(self):
        return TYPE_TO_CHAR[self.block_type]
    
    def step(self, newWorld, newGrid):
        pass

    def propagate(self, newWorld, newGrid):
        pass
    
    def getRect(self, block_width, block_height):
        return [self.y * block_height, self.x * block_width, block_width, block_height]
    
    def draw(self, screen, block_width, block_height, debug=None):
        rect = self.getRect(block_width, block_height)
        if debug == None:
            pygame.draw.rect(screen, self.color, rect)
        elif debug == 'adjacentFlammable':
            pygame.draw.rect(screen, RED if self.foundAdjacentFlammable else BLACK, rect)
        elif debug == 'vicinityFlameCount':
            pygame.draw.rect(screen, (self.countVicinitylames*10, 0, 0), rect)
    

class Cell_FIRE(Cell):
    def __init__(self, coords, parent_world, parent_grid):
        super().__init__(coords, parent_world, parent_grid, 'fire')
        self.color = RED
    
    def step(self, newWorld, newGrid):
        if not self.foundAdjacentFlammable:
            return Cell_AIR(self.coords, newWorld, newGrid)
        else:
            # Check for flames in the vicinity
            if self.countVicinitylames < 4 and np.random.random() < 0.05:
                return Cell_AIR(self.coords, newWorld, newGrid)
            else:
                return Cell_FIRE(self.coords, newWorld, newGrid)

    def propagate(self, newWorld, newGrid):
        for cell in self.list_vicinity_cells():
            cell.addVicinityFlame()


class Cell_WOOD(Cell):
    def __init__(self, coords, parent_world, parent_grid, hp=100):
        super().__init__(coords, parent_world, parent_grid, 'wood')
        self.hp = hp
        self.color = BROWN
    
    def step(self, newWorld, newGrid):
        damage = self.countVicinitylames
        newHP = self.hp-damage
        if newHP <= 0:
            return Cell_AIR(self.coords, newWorld, newGrid)
        else:
            return Cell_WOOD(self.coords, newWorld, newGrid, newHP)

    def propagate(self, newWorld, newGrid):
        for cell in self.list_adjacent_cells():
            cell.addAdjacentFlammable()



class Cell_AIR(Cell):
    def __init__(self, coords, parent_world, parent_grid):
        super().__init__(coords, parent_world, parent_grid, 'air')
        self.color = BLACK
    
    def step(self, newWorld, newGrid):
        if self.foundAdjacentFlammable:
            probability_of_fire = 0.04*self.countVicinitylames
            # if probability_of_fire != 0:
            #     print(self.coords, probability_of_fire)
            if np.random.random() < probability_of_fire:
                return Cell_FIRE(self.coords, newWorld, newGrid)
        return Cell_AIR(self.coords, newWorld, newGrid)