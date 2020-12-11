from simulation.Basic2DSim import World
import numpy as np

def load_world_from_file(filename):
    f = open(filename, 'r')
    s = f.read()
    return load_world_from_string(s)

def load_world_from_string(s):
    lines = s.splitlines()
    W, H = [int(v) for v in lines[0].split()]
    world = World(W, H)
    for line in lines[1:]:
        x, y, block_type = line.split()
        x, y = int(x), int(y)
        world.createCell((x, y), block_type)
    world.propagate()
    return world

def serialize(world):
    s = str(world.W) + " " + str(world.H) + "\n"
    for cell in world.list_cells():
        serialized_cell = cell.serialize()
        if serialized_cell != None:
            s += serialized_cell
    return s

def encode(world):
    W, H = world.W, world.H
    g = np.zeros((W, H))
    for cell in world.list_cells():
        g[cell.x, cell.y] = int(cell)
    return g