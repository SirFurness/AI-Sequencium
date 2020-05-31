import collections
import random

import torch

class ReplayBuffer():
    def __init__(self, buffer_limit):
        self.buffer = collections.deque(maxlen=buffer_limit)

    def put(self, transition):
        self.buffer.append(transition)

    def sample(self, n):
        mini_batch = random.sample(self.buffer, n)

        states = []
        actions = []
        rewards = []
        newStates = []
        newValidActions = []
        doneMasks = []

        for transition in mini_batch:
            state, action, reward, newState, newValidActionList, done_mask = transition

            states.append(state)
            actions.append([action])
            rewards.append([reward])
            newStates.append(newState)
            newValidActions.append(newValidActionList)
            doneMasks.append([done_mask])

        return (torch.tensor(states, dtype=torch.float),
                torch.tensor(actions),
                torch.tensor(rewards, dtype=torch.float),
                torch.tensor(newStates, dtype=torch.float),
                newValidActions,
                torch.tensor(doneMasks, dtype=torch.float))

    def size(self):
        return len(self.buffer)

