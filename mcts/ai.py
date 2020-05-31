from game import *
import mcts

def main():
    root = mcts.Node(initial_state(), 0, 0)

    while not is_game_over(root.state):
        root = mcts.mcts(root)

        render(root.state)

        input_action = int(input("Action: "))

        if input_action in root.unvisited_actions:
            newState = play(root.state, input_action)
            root = mcts.Node(newState, root.action, input_action)
        else:
            for child in root.children:
                if child.action == input_action:
                    root = child
        render(root.state)

main()
        
