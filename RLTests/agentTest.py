from RLTests.SingleAgentEnv import SingleAgentEnvironment
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Input, Dense, Conv2D, Dropout, BatchNormalization, Concatenate, Flatten

gamma = 0.99  # Discount factor for past rewards
max_steps_per_episode = 10000
env = SingleAgentEnvironment("worlds/editorTest.world")
eps = np.finfo(np.float32).eps.item()  # Smallest number such that 1.0 + eps != 1.0

num_actions = 8
num_hidden = 32
num_hidden_pre = 8
mapInputs = Input(shape=(40, 40, 3))
stateInputs = Input(shape=(3,))
vicConv = Conv2D(16, (5, 5), padding='same', activation='relu')(mapInputs)
vicConv = Conv2D(1, (5, 5), padding='same', activation='relu')(vicConv)
vicConv = Flatten()(vicConv)
d0 = Dense(num_hidden_pre, activation="relu")(stateInputs)
x = Concatenate()([d0, vicConv])
x = Dense(2*num_hidden, activation='relu')(x)
common = Dense(num_hidden, activation="relu")(x)
action = Dense(num_actions, activation="softmax")(common)
critic = Dense(1)(common)

model = keras.Model(inputs=[mapInputs, stateInputs], outputs=[action, critic])

model.summary()

optimizer = keras.optimizers.Adam(learning_rate=0.01)
huber_loss = keras.losses.Huber()
action_probs_history = []
critic_value_history = []
rewards_history = []
running_reward = 0
episode_count = 0

while True:  # Run until solved
    state = env.reset()
    episode_reward = 0
    with tf.GradientTape() as tape:
        for timestep in range(1, max_steps_per_episode):
            state = tf.expand_dims(state[0], 0), tf.expand_dims(state[1], 0)

            # Get probabilities of the learned policy, as well as the value approximation given current state
            action_probs, critic_value = model(state)
            critic_value_history.append(critic_value[0, 0])

            # Sample action from action probability distribution
            action = np.random.choice(num_actions, p=np.squeeze(action_probs))
            action_probs_history.append(tf.math.log(action_probs[0, action]))

            # Apply the sampled action in our environment
            state, reward, done, _ = env.step(action)
            rewards_history.append(reward)
            episode_reward += reward

            if done:
                break

        # Calculate the return at each timestep
        returns = []
        discounted_sum = 0
        for r in rewards_history[::-1]:
            discounted_sum = r + gamma * discounted_sum
            returns.insert(0, discounted_sum)

        # Normalize
        returns = np.array(returns)
        returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
        returns = returns.tolist()

        # Calculating loss values to update our network
        history = zip(action_probs_history, critic_value_history, returns)
        actor_losses = []
        critic_losses = []
        for log_prob, value, ret in history:
            actor_losses.append(-log_prob * (ret - value))  # actor loss

            critic_losses.append(huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0))) # critic loss

        # Backpropagation
        loss_value = sum(actor_losses) + sum(critic_losses)
        grads = tape.gradient(loss_value, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        # Reset memories
        action_probs_history.clear()
        critic_value_history.clear()
        rewards_history.clear()

    # Output reward
    episode_count += 1
    if episode_count % 10 == 0:
        template = "running reward: {:.2f} at episode {}"
        print(template.format(running_reward, episode_count))