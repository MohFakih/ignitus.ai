from simulation.Basic2DSim import World
from utils.Serialization import load_world_from_file

class Environment():
    def __init__(self, worldFile):
        self.worldFile = worldFile
        self.world = load_world_from_file(worldFile)

    def step(self, action):
        observation = None
        reward = None
        terminal = False
        return observation, reward, terminal