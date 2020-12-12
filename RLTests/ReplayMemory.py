import numpy as np

# TODO: Consider changing numpy implementation into tensor-based memory (way faster)

class ReplayMemory:
	def __init__(self, size=10_000, state_size=4, action_size=1):
		"""
		Helper class that manages storing and loading transition vectors
		:param size: maximum number of transitions held at the same time
		:param state_size: size of the state vector, environment specific
		:param action_size: size of the action vector, environment specific
		"""
		self.state_size = state_size
		self.action_size = action_size
		self.transitionCount = 0            # Holds how many transitions the memory currently holds
		self.maxSize = size                 # Maximum number of transitions memory can hold
		self.StMemory   = np.zeros((size, state_size))  # Initialize memory arrays
		self.AtMemory   = np.zeros((size, 1), dtype=int)
		self.Stp1Memory = np.zeros((size, state_size))
		self.Rtp1Memory = np.zeros((size, 1))
		self.FinalMemory= np.zeros((size, 1))

	def addTransition(self, st, at, stp1, rtp1, final):
		"""
		If the memory can hold a transition, appends it to the end of the current array.
		Else, choose a random old transition and overwrite it.
		:param st: state vector s at timestep t
		:param at: action vector a at timestep t
		:param stp1: state vector at timestep t+1
		:param rtp1: reward value at timestep t
		:param final: boolean indicating if we have reached a final state
		"""
		if self.transitionCount == self.maxSize:
			index = np.random.randint(0, self.maxSize)
		else:
			index = self.transitionCount
			self.transitionCount += 1
		self.StMemory[index] = np.array(st)
		self.AtMemory[index] = np.array([at])
		self.Stp1Memory[index] = np.array(stp1)
		self.Rtp1Memory[index] = np.array([rtp1])
		self.FinalMemory[index] = np.array([final])

	def sampleTransitions(self, n):
		"""
		Sample n transitions from the memory
		:param n: number of transition tuples to sample
		:return: n transitions in a tuple of vectors where each transition is a "row" in the combined vectors
		"""
		indices = np.random.choice(self.transitionCount, n, replace=False)
		StVect = self.StMemory[indices]
		AtVect = self.AtMemory[indices]
		Stp1Vect = self.Stp1Memory[indices]
		Rtp1Vect = self.Rtp1Memory[indices]
		FinalVect = self.FinalMemory[indices]
		return StVect, AtVect, Stp1Vect, Rtp1Vect, FinalVect

	def getMemorySize(self):
		return self.transitionCount

	def getEntireMemory(self):
		"""
		Get all the available transitions
		:return: returns all transitions curently held.
		"""
		StVect = self.StMemory[:self.transitionCount]
		AtVect = self.AtMemory[:self.transitionCount]
		Stp1Vect = self.Stp1Memory[:self.transitionCount]
		Rtp1Vect = self.Rtp1Memory[:self.transitionCount]
		FinalVect = self.FinalMemory[:self.transitionCount]
		return StVect, AtVect, Stp1Vect, Rtp1Vect, FinalVect
