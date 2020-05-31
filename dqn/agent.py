from qnet import Qnet
import qnet

from replay_buffer import ReplayBuffer

import torch.optim as optim
from torch.optim.lr_scheduler import StepLR

import random
import math

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

        self.learning_rate = 0.1
        self.optimizer = optim.Adam(self.q.parameters(), lr=self.learning_rate)

        # gamma = decaying factor
        self.scheduler = StepLR(self.optimizer, step_size=10, gamma=0.999)

        self.batch_size = 32
        self.gamma = 0.98
        
        self.state = env.getState()

    def move(self, env, epsilon, flip):
        action = self.q.sample_action(env, epsilon, flip)
        newState, reward, isDone = env.step(action, flip)
        newValidActionList = env.getValidActions()

        done_mask = 0.0 if isDone else 1.0
        self.memory.put((self.state, action, reward, newState, newValidActionList, done_mask))
        self.state = newState

        self.score += reward
        self.total_score += reward

        return isDone

    def updateInfo(self, episode, epsilon):
        if self.memory.size() > 2000:
            self.scheduler.step()

        if episode % self.print_interval == 0 and episode != 0:
            self.updateQTarget()
            print("episode: {}, lr: {:.2f}, total_score: {:.2f}, score: {:.1f}, buffer: {}, epsilon: {:.1f}%".format(
                episode, self.scheduler.get_last_lr()[0], self.total_score/episode, self.score/self.print_interval, self.memory.size(), epsilon*100))
            self.score = 0.0

    def train(self):
        if self.memory.size() > 2000:
            qnet.train(self.q, self.q_target, self.memory, self.optimizer, self.batch_size, self.gamma)

    def updateQTarget(self):
        self.q_target.load_state_dict(self.q.state_dict())

    def state_dict(self):
        return self.q.state_dict()

class MultiStupidAgent:
    def __init__(self, num_of_agents):
        self.num_of_agents = num_of_agents

        self.q_nets = [Qnet() for i in range(num_of_agents)]

        self.current_agent = 0

        self.update_interval = 1000 * num_of_agents
        self.update_offset = math.trunc(self.update_interval / num_of_agents)

        self.reset_interval = 10_000

    def move(self, env, epsilon, flip):
        current_q = self.q_nets[self.current_agent]

        action = current_q.sample_action(env, epsilon, flip)
        env.step(action, flip)

    def increaseCurrentAgent(self):
        self.current_agent = (self.current_agent + 1) % self.num_of_agents

    def update(self, episode, state_dict):
        self.increaseCurrentAgent()

        if episode % self.reset_interval == 0:
            self.q_nets = [Qnet() for i in range(self.num_of_agents)]

        for i, q_net in enumerate(self.q_nets):
            if (episode + i * self.update_offset) % self.update_interval == 0:
                q_net.load_state_dict(state_dict)

class StupidAgent:
    def __init__(self, state_dict):
        self.q = Qnet()
        self.q.load_state_dict(state_dict)

        self.updateInterval = 2000

    def move(self, env, epsilon, flip):
        action = self.q.sample_action(env, epsilon, flip)
        
        env.step(action, flip)

    def update(self, episode, state_dict):
        if episode % self.updateInterval == 0 and episode != 0:
            self.q.load_state_dict(state_dict)

class HumanAgent:
    def move(self, env, _epsilon, flip):
        strMove = input("Row Space Column: ")
        listInput = strMove.split()
        rowAndCol = [int(string) for string in listInput]

        row = rowAndCol[0]
        col = rowAndCol[1]

        action = env.convertCoordinateToAction((row, col)) 

        if flip:
            action = 35 - action

        env.step(action, flip)

class RandomAgent:
    def move(self, env, _epsilon, flip):
        validActions = env.getValidActions()
        action = random.choice(validActions)

        env.step(action, flip)
