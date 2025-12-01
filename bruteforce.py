import csv
import os
from pathlib import Path


ACTIONS_FILE = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

CURRENT_DIR = Path(os.getcwd())

ACTIONS_FILEPATH = CURRENT_DIR / "data" / ACTIONS_FILE

MAX_COST = 500


def get_actions():
    try:
        with open(str(ACTIONS_FILEPATH), "r", encoding="utf-8") as f:

            reader = csv.reader(f)
            actions_list = list(reader)
            actions_list.remove(actions_list[0])

            actions = []
            for action in actions_list:
                cost = int(action[1])
                benefice = int(action[2].strip('%'))
                profit = float((benefice / 100) * cost)
                actions.append([action[0], cost, benefice, profit])
            return actions

    except Exception as e:
        print(f"ERROR reading {ACTIONS_FILEPATH}: {e}")
        return None

def display_actions(actions_list):
    for action in actions_list:
        print(f"{action[0]} - COST per action : {action[1]}€, BENEFICE (after 2 years) : {action[2]}%, PROFIT (after 2 years) : {action[3]}€")
    print("\n")

def build_tree(actions_list, current_profit, current_cost, current_path):
    if not actions_list:
        print("All actions are done.")
        return current_path, current_profit

    action = actions_list[0]
    action_cost = action[1]
    action_profit = action[3]

    # Right branch
    print(f"Building right tree without action {action[0]}...")
    right_best_path, right_best_profit = build_tree(actions_list[1:].copy(), current_profit, current_cost, current_path)

    # Left branch
    if current_cost + action_cost <= MAX_COST:
        new_path = current_path + [action]
        print(f"Building left tree with action {action[0]}...")
        left_best_path, left_best_profit = build_tree(actions_list[1:], current_profit + action_profit, current_cost + action_cost, new_path)
    else:
        print("Max cost exceeded!")
        left_best_path, left_best_profit = ([], 0.0)

    if left_best_profit > right_best_profit:
        print(f"Best profit : {left_best_profit}")
        return left_best_path, left_best_profit
    else:
        print(f"Best profit : {right_best_profit}")
        return right_best_path, right_best_profit

def main():
    actions = get_actions()
    # actions = [["action-1", 34, 12, 22.0], ["action-2", 64, 9, 19.2], ["action-3", 34, 19, 16.3]]

    display_actions(actions)

    best_path, best_profit = build_tree(actions, 0.0, 0, [])
    print(f"\nThe best actions path is : {best_path}\nFor the best profit : {best_profit}€")


if __name__ == "__main__":
    main()
