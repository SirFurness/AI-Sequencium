from game import *
from winner import Winner
from player import Player

import random
import datetime
import math

from timeit import default_timer as timer

def mcts(root):
    start_time = datetime.datetime.utcnow()
    delta_time = datetime.timedelta(seconds=5)
    while datetime.datetime.utcnow() - start_time < delta_time:
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        backpropagate(leaf, simulation_result)
    return root.best_child()

def traverse(node):
    while node.is_fully_expanded():
        node = node.best_uct()
    return node.pick_unvisited()

def rollout(node):
    previous_previous_action = node.previous_action
    previous_action = node.action
    state = node.state
    player = current_player(state)
    while not is_game_over(state):
        valid_actions = valid_actions_for_player(state, player)
        #action = random_rollout_policy(valid_actions)
        action = rollout_policy(state, valid_actions, player, previous_previous_action, previous_action)

        previous_previous_action = previous_action
        previous_action = action

        state = play(state, action)

        player = current_player_from_previous(state, player)
        
    return winner(state)

def random_rollout_policy(actions):
    return random.choice(actions)

def rollout_policy(state, actions, player, previous_previous_action, previous_action):
    urgency = assign_urgency_to_actions(state, actions, player, previous_previous_action, previous_action)
    action = random.choices(actions, weights=urgency, k=1)[0]
    
    return action

def assign_urgency_to_actions(state, actions, player, previous_previous_action, previous_action):
    urgency = []
    for action in actions:
        if are_adjacent(previous_action, action): 
            urgency.append(5)
        elif are_adjacent(previous_previous_action, action):
            urgency.append(5)
        elif is_adjacent_to_opponent(state, action, player):
            urgency.append(2)
        else:
            urgency.append(1)

    return urgency

def backpropagate(node, result):
    node.update_stats(result)
    if not node.is_root():
        backpropagate(node.parent, result)

def best_child(node):
    return node.best_uct()

class Node:
    def __init__(self, state, previous_action, action, parent=None):
        self.state = state
        self.player = current_player(state)

        self.previous_action = previous_action
        self.action = action

        self.actions = valid_actions_for_player(self.state, self.player)
        self.unvisited_actions = self.actions[:]

        self.children = []
        self.parent = parent

        self.stats = {'wins': 0.0, 'plays': 0.0}

    def is_fully_expanded(self):
        return len(self.unvisited_actions) == 0

    def best_child(self):
        return self.best_child_robust()

    def best_child_max(self):
        best_child = self.children[0]
        best_avg = self.calc_avg(best_child)

        for child in self.children:
            avg = self.calc_avg(child)
            if avg > best_avg:
                best_child = child
                best_avg = avg

        return best_child

    def best_child_robust(self):
        best_child = self.children[0]
        best_num_of_visits = self.children[0].stats['plays']

        for child in self.children:
            if child.stats['plays'] > best_num_of_visits:
                best_child = child
                best_num_of_visits = child.stats['plays']

        return best_child

    def best_uct(self):
        best_child = self.children[0]
        best_uct = self.calc_uct(best_child)

        for child in self.children:
            uct = self.calc_uct(child)
            if uct > best_uct:
                best_child = child
                best_uct = uct

        return best_child
    
    def calc_avg(self, child):
        return child.stats['wins']/child.stats['plays']

    def calc_uct(self, child):
        return child.stats['wins']/child.stats['plays'] + math.sqrt(2*math.log(self.stats['plays'])/child.stats['plays'])

    def pick_unvisited(self):
        unvisited = self.unvisited_actions.pop()

        child = Node(play(self.state, unvisited), self.action, unvisited, parent=self)
        self.children.append(child)

        return child

    def is_root(self):
        return self.parent is None

    def update_stats(self, result):
        self.stats['plays'] += 1.0
        if(self.did_i_win(result)):
            self.stats['wins'] += 1.0
        if(result == Winner.Tie):
            self.stats['wins'] += 0.5

    def did_i_win(self, result):
        if result == Winner.A and self.player == Player.A:
            return True
        elif result == Winner.B and self.player == Player.B:
            return True
        else:
            return False

    def pick_random_child(self):
        newState = play(self.state, random.choice(self.actions))
        return newState
