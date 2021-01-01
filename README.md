# IGNITUS.AI
RL agent to coordinate fire fighting and rescue operations

# Purpose and Description
Built as the final project of the EECE 699 (Topics in AI) course in the FALL2020 semester.
Uses a  cellular automata based environment to simulate fire spread and building destruction, with victims that need to be saved.
Agent trained using the Actor-Critic method.

# Results
Agent learned some basic behavior:
- Picking up closest victim,
- Putting out fires near the end of the episode
- Conditionally exploiting a bug in the simulation which terminates the episode early in case of an inevitable victim death, which avoids the negative reward.
- Waiting for "flimsy" buildings to collapse instead of going around a long way.
