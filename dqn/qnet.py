import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Qnet(nn.Module):
    def __init__(self):
        super(Qnet, self).__init__()
        self.fc1 = nn.Linear(36+2, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 37)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def sample_action(self, env, epsilon, flip=False):
        out = self.forward(env.getStateTensor(flip))

        validActions = env.getValidActions(flip)

        final_action = 36
        if random.random() < epsilon:
            final_action = random.choice(validActions) 
        else:
            valid = out.gather(0, torch.tensor(validActions))

            choice = valid.argmax().item()
            action = validActions[choice]

            final_action = action

        if flip and final_action != 36:
            final_action = 35 - final_action
            
        return final_action

def train(q, q_target, memory, optimizer, batch_size, gamma):
    total_loss = 0
    for i in range(10):
        states, actions, rewards, newStates, newValidActions, done_masks = memory.sample(batch_size)

        # q values for the given state
        q_values = q(states)

        # q values for the given action
        q_actions = q_values.gather(1, actions)

        # q values for the given new state
        q_primes = q_target(newStates)
        list_q_primes = q_primes.tolist()
       
        max_q_primes_list = []
        for state_index, q_primes in enumerate(list_q_primes):
            valid_q_primes = []
            for q_prime_index, q_prime in enumerate(q_primes):
                if q_prime_index in newValidActions[state_index]:
                    valid_q_primes.append(q_prime)

            max_valid = max(valid_q_primes)
            max_q_primes_list.append([max_valid])

        #valid_q_primes = q_primes.gather(1, newValidActions)

        # max valid q primes for the new state
        #max_q_primes = valid_q_primes.max(1)[0].unsqueeze(1)
        max_q_primes = torch.tensor(max_q_primes_list)

        # What the q value for the action should be
        targets = rewards + gamma * max_q_primes * done_masks

        loss = F.smooth_l1_loss(q_actions, targets)
        total_loss += loss

        # Zero the gradients
        optimizer.zero_grad()

        # Compute gradients
        loss.backward()

        # Gradient descent / whatever optimizer
        optimizer.step()
