from env import Environment
from agent import LearningAgent, StupidAgent

import torch

def main():
    env = Environment()

    learningAgent = LearningAgent(env)
    stupidAgent = StupidAgent(learningAgent.state_dict())

    for episode in range(10000):
        # Decrease epsilon by 1% every 200 episodes
        epsilon = max(0.01, 0.08 - 0.01*(episode/200))

        env.reset()
        isDone = False
        
        while not isDone:
            isDone = learningAgent.move(env, epsilon)
            stupidAgent.move(env, epsilon)

        learningAgent.train()
        learningAgent.updateInfo(episode, epsilon)

        stupidAgent.update(episode, learningAgent.state_dict())

    torch.save(learningAgent.state_dict(), "model_data")


if __name__ == '__main__':
    main()
