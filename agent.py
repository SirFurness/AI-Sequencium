from qnet import Qnet
import qnet

from replay_buffer import ReplayBuffer

import torch.optim as optim

import random

class LearningAgent:
    def __init__(self, env):
        self.q = Qnet()

        self.q_target = Qnet()
        self.q_target.load_state_dict(self.q.state_dict())

        self.buffer_limit = 50000
        self.memory = ReplayBuffer(self.buffer_limit)

        self.print_interval = 20
        self.score = 0.0
        self.total_score = 0

        self.learning_rate = 0.01
        self.optimizer = optim.Adam(self.q.parameters(), lr=self.learning_rate)

        self.batch_size = 32
        self.gamma = 0.98
        
        self.state = env.getState()

    def move(self, env, epsilon):
        action = self.q.sample_action(env, epsilon) 
        newState, reward, isDone = env.step(action)
        newValidActionList = env.getValidActions()

        done_mask = 0.0 if isDone else 1.0
        self.memory.put((self.state, action, reward, newState, newValidActionList, done_mask))
        self.state = newState

        self.score += reward
        self.total_score += reward

        return isDone

    def updateInfo(self, episode, epsilon):
        if episode % self.print_interval == 0 and episode != 0:
            self.updateQTarget()
            print("episode: {}, total_score: {:.2f}, score: {:.1f}, buffer: {}, epsilon: {:.1f}%".format(
                episode, self.total_score/episode, self.score/self.print_interval, self.memory.size(), epsilon*100))
            self.score = 0.0

    def train(self):
        if self.memory.size() > 2000:
            qnet.train(self.q, self.q_target, self.memory, self.optimizer, self.batch_size, self.gamma)

    def updateQTarget(self):
        self.q_target.load_state_dict(self.q.state_dict())

    def state_dict(self):
        return self.q.state_dict()

class StupidAgent:
    def __init__(self, state_dict):
        self.q = Qnet()
        self.q.load_state_dict(state_dict)

        self.updateInterval = 1000

    def move(self, env, epsilon):
        action = self.q.sample_action(env, epsilon, flip=True)
        
        env.step(action)

    def update(self, episode, state_dict):
        if episode % self.updateInterval == 0 and episode != 0:
            self.q.load_state_dict(state_dict)

class HumanAgent:
    def move(self, env, _epsilon):
        strMove = input("Row Space Column: ")
        listInput = strMove.split()
        rowAndCol = [int(string) for string in listInput]

        row = rowAndCol[0]
        col = rowAndCol[1]

        action = env.convertCoordinateToAction((row, col)) 

        env.step(action)

class RandomAgent:
    def move(self, env, _epsilon):
        validActions = env.getValidActions()
        action = random.choice(validActions)

        env.step(action)
