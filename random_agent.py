import random
import os
import time

from env import Environment

env = Environment()
isDone = False
while not isDone:
    validActions = env.getValidActions()
    action = random.choice(validActions)

    newState, reward, isDone = env.step(action)

    os.system('clear')
    env.render()
    time.sleep(1)
