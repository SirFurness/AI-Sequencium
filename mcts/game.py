from player import Player
from winner import Winner

import random
import os
import time

def initial_state():
    init_state = [1]
    for i in range(36-2):
        init_state.append(0)
    init_state.append(-1)
    return init_state

def is_player_square(square_content, player):
    if player == Player.A and square_content > 0:
        return True
    elif player == Player.B and square_content < 0:
        return True
    else:
        return False

def square_player(square_content):
    if is_player_square(square_content, Player.A):
        return Player.A
    else:
        return Player.B

def valid_actions_for_player(state, player):
    valid_actions = []
    for i, square_content in enumerate(state):
        if is_player_square(square_content, player):
          valid_actions.extend(empty_neighbors(state, i)) 
    return valid_actions

def empty_neighbors(state, i):
    all_neighbors = neighbors(state, i)
    
    return [square_index for square_index in all_neighbors if state[square_index] == 0] 

def neighbors(state, i):
    neighbors = []

    # top
    if i >= 6:
        neighbors.append(i-6)
    # left
    if i % 6 != 0:
        neighbors.append(i-1)
        # top left
        if i >= 6:
            neighbors.append(i-7)
        # bottom left
        if i < 30:
            neighbors.append(i+5)
    # right
    if (i+1) % 6 != 0:
        neighbors.append(i+1)
        # top right
        if i >= 6:
            neighbors.append(i-5)
        # bottom right
        if i < 30:
            neighbors.append(i+7)
    # bottom
    if i < 30:
        neighbors.append(i+6)

    return neighbors

def current_player(state):
    num_player_a_actions = len(valid_actions_for_player(state, Player.A))
    num_player_b_actions = len(valid_actions_for_player(state, Player.B))

    num_player_a_moves = len([square for square in state if is_player_square(square, Player.A)])
    num_player_b_moves = len([square for square in state if is_player_square(square, Player.B)])

    if num_player_a_actions == 0:
        return Player.B
    elif num_player_b_actions == 0:
        return Player.A
    elif num_player_a_moves == num_player_b_moves:
        return Player.A
    elif num_player_a_moves > num_player_b_moves:
        return Player.B
    else:
        # why not
        return Player.B

def play(state, action_square_index):
    player = current_player(state)
    all_neighbors = neighbors(state, action_square_index)
    same_player_neighbors = [square_index
            for square_index in all_neighbors
            if square_player(state[square_index]) == player]

    if len(same_player_neighbors) > 0:
        max_content = max([abs(state[square_index]) for square_index in same_player_neighbors])
        
        if player == Player.A:
            scale = 1
        elif player == Player.B:
            scale = -1
        newState = [(max_content + 1)*scale if square_index == action_square_index else square_content for square_index, square_content in enumerate(state)]
        return newState

def is_game_over(state):
    num_player_a_actions = len(valid_actions_for_player(state, Player.A))
    num_player_b_actions = len(valid_actions_for_player(state, Player.B))

    return num_player_a_actions == 0 and num_player_b_actions == 0

def winner(state):
    if is_game_over(state):
        max_for_a = max(state)
        max_for_b = abs(min(state))

        if max_for_a == max_for_b:
            return Winner.Tie
        elif max_for_a > max_for_b:
            return Winner.A
        else:
            return Winner.B
    else:
        return Winner.NotOver

def render(state):
    maxSpacing = 4

    os.system("cls||clear")

    for i, square in enumerate(state):
        if i % 6 == 0:
            for j in range(maxSpacing-2):
                print("")
        spacing = maxSpacing - len(str(square))
        for i in range(spacing):
            print(" ", end='')
        print(str(square), end='')
    print("")
