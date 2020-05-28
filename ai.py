from env import Environment
from agent import *

import torch

import sys

def main(mode):
    test = False

    env = Environment()
    
    renderInterval = 2000
    episode_count = 20_000

    learningAgent = LearningAgent(env)
    learningAgent.q.load_state_dict(torch.load("model_data"))

    if mode == "human":
        test = True
        stupidAgent = HumanAgent()
        episode_count = 1
    elif mode == "random":
        test = True
        stupidAgent = RandomAgent()

    if test:
        learningAgent.q.eval()
    else:
        #stupidAgent = StupidAgent(learningAgent.state_dict())
        stupidAgent = MultiStupidAgent(3)

    epsilon = 0.08
    epsilon_reset = 5_000
    for episode in range(episode_count):
        if test:
            epsilon = 0
        else:
            if episode % epsilon_reset == 0:
                epsilon = 0.08
            # Decrease epsilon by 1% every 200 episodes
            epsilon = max(0.01, epsilon - 0.01/200)

        env.reset()
        isDone = False
        
        while not isDone:
            isDone = learningAgent.move(env, epsilon, flip=False)

            if episode % renderInterval == 0 or episode+1 == episode_count:
                env.render(flip=False)

                if not test:
                    torch.save(learningAgent.state_dict(), "model_data")
                
            stupidAgent.move(env, epsilon, flip=True)
        
        
        if not test:
            learningAgent.train()
            learningAgent.updateInfo(episode, epsilon)

            stupidAgent.update(episode, learningAgent.state_dict())
        else:
            learningAgent.updateInfo(episode, epsilon)

    if not test:
        torch.save(learningAgent.state_dict(), "model_data")


if __name__ == '__main__':
    arg = ""
    if len(sys.argv) >= 2:
        arg = str(sys.argv[1])

    main(arg)
