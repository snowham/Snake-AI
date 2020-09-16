import numpy as np
class QLAgent:
    def __init__(self):
        self.q_table = {'0 1 0 0  0 0 0 0 1 0 0 0': [0, 0, 0.99, 0]}

        self.trainEpisodes = 20000
        self.testEpisodes = 10

        self.learning_rate = 0.0009
        self.discount_rate = 0.99

        self.exploration_rate = 1
        self.min_exploration_rate = 0.001
        self.exploration_decay_rate = 0.001
    
    def predict_action(self, state):
        exploration_rate_threshold = np.random.uniform(0, 1)
        actions = self.q_table[state]
        if exploration_rate_threshold > self.exploration_rate:
            action = np.argmax(actions)
        else:
            action = np.random.choice(range(4))
        return action

    def update_exploration_rate(self):
        self.exploration_rate = (self.exploration_rate - self.min_exploration_rate) * np.exp(-self.exploration_decay_rate) + self.min_exploration_rate
    
    def update_q_table(self, state, action, new_state, reward):
        self.q_table[new_state] = self.q_table.get(new_state, [0, 0, 0, 0])
        new_actions = self.q_table[new_state]
        self.q_table[state][action] = (1 - self.learning_rate) * self.q_table[state][action] + self.learning_rate * (reward + self.discount_rate * np.max(new_actions))