from simulation.Basic2DSim import World
from utils.Serialization import encode
from utils.Serialization import load_world_from_file
from RLTests.Environment import Environment
from tensorflow.keras.utils import to_categorical
import tensorflow as tf

class SingleAgentEnvironment(Environment):
    def __init__(self, worldFile):
        super().__init__(worldFile)
        self.x = 0
        self.y = 0
        self.carryingVictim = False
        self.waterSupply = 1.0
        self.hp = 1.0
    
    def preprocess_observation(self, observation):
        map_obs = to_categorical(observation, num_classes=6)
        map_obs[self.x, self.y, 5] = 1
        innerState= tf.constant([1 if self.carryingVictim else 0, self.waterSupply, self.hp])
        return (map_obs, innerState)

    def observe(self):
        return encode(self.world)

    def reset(self):
        self.world = load_world_from_file(self.worldFile)
        return self.preprocess_observation(self.observe())

    def getRect(self, block_width, block_height):
        return [self.y * block_height, self.x * block_width, block_width, block_height]

    def countVictimsAndFire(self):
        c = 0
        f = 0
        for cell in self.world.list_cells():
            if cell.block_type == 'victim':
                c += 1
            if cell.block_type == 'fire':
                f += 1
        return c, f
    
    def move(self, dir):
        if dir == 1:
            self.x = max(self.x-1, 0)
        elif dir == 2:
            self.y = min(self.y+1, self.world.W-1)
        elif dir == 3:
            self.x = min(self.x+1, self.world.H-1)
        elif dir == 4:
            self.y = max(self.y -1, 0)

    def extinguish(self):
        for cell in self.world.grid[self.x][self.y].list_vicinity_cells():
            if cell.block_type == 'fire':
                self.world.createCell(cell.coords, 'air')
    
    def pickup(self):
        if not self.carryingVictim and self.world.grid[self.x][self.y].block_type == 'victim':
            self.world.createCell((self.x, self.y), 'air')
            self.carryingVictim = True
    
    def dropdown(self):
        if self.carryingVictim and self.world.grid[self.x][self.y].block_type == 'air':
            self.world.createCell((self.x, self.y), 'victim')
            self.carryingVictim = False

    def action(self, action):
        if action == 0:
            pass #nop
        elif action in [1,2,3,4]:
            self.move(action)
        elif action == 5:
            self.extinguish()
        elif action == 6:
            self.pickup()
        elif action == 7:
            self.dropdown()
        else:
            raise Exception("Illegal action"+str(action))

    def reward(self, observation, terminal, stateBefore, stateAfter):
        victimsBefore, woodBefore = stateBefore
        victimsAfter, woodAfter = stateAfter
        if not terminal:
            reward = -1
        else:
            if self.isAgentDead():
                return -10000
            reward = -1
            for row in observation:
                for cell in row:
                    if cell == 3:
                        reward += 2
                    if cell == 4:
                        reward += 20
            if self.carryingVictim:
                reward += 20
        
        deltaVictims = victimsBefore - victimsAfter
        deltaWood = woodBefore - woodAfter
        deltaVictims += (1 if self.carryingVictim else 0)
        reward += deltaWood * 3
        reward += deltaVictims*20
        return reward

    def isAgentDead(self):
        return self.world.grid[self.x][self.y].block_type not in ['air', 'victim', 'fire'] or self.hp < 0

    def isTerminal(self):
        return self.world.isTerminal() or self.isAgentDead()

    def worldStep(self):
        stateBefore = self.countVictimsAndFire()
        self.world.step()
        stateAfter = self.countVictimsAndFire()
        return stateBefore, stateAfter

    def step(self, action):
        self.action(action)
        stateBefore, stateAfter = self.worldStep()
        observation = self.observe()
        terminal = self.isTerminal()
        reward = self.reward(observation, terminal, stateBefore, stateAfter)
        preprocessed_observation = self.preprocess_observation(observation)

        return preprocessed_observation, reward, terminal