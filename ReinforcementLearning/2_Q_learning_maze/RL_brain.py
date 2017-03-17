# utf-8
# python3.5

import numpy as np
import pandas as pd

class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions   # list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions)

    def choose_action(self, observation):
        self.check_state_exit(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.ix[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))  # some action have same value
            action = state_action.argmax()
        else:
        # choose random action
            action = np.random.choice(self.actions)

        return action

    def learn(self, s, a, r, s_):
        self.check_state_exit(s_)
        q_predict = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.ix[s_, :].max()    # next state is not terminal
        else:
            q_target = r    # next state is terminal

        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)   # update

    def check_state_exit(self, state):
        if state not in self.q_table.index:
            # append new state too q table
            self.q_table = self.q_table.append(
                    pd.Series(  
                        [0]*len(self.actions),
                        index=self.q_table.columns,
                        name=state,
                        )
                    )
