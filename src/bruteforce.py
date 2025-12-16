import csv
import os
from pathlib import Path

from src.timer import Timer


ACTIONS_FILE = "actions_list.csv"

CURRENT_DIR = Path(os.getcwd())

ACTIONS_FILEPATH = CURRENT_DIR / "../data" / ACTIONS_FILE

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

def display_actions(actions: list) -> None:
    """
    Display the list of actions given.
    Args:
        actions (list): The list of actions.
    """
    print(f"{'ACTION':<15} {'COST (€)':<10} {'BENEFICE (%)':<15} {'PROFIT (€)':<12}")
    print("-" * 65)

    for action in actions:
        name = action[0]
        cost = action[1]
        benefit = action[2]
        profit = action[3]

        print(f"{name:<15} {cost:<10} {benefit:<15} {profit:<12}")

    print()

def display_results(results: list, profit: float) -> None:
    """
    Display the results list. Call the display_actions method.
    Args:
        results (list): The list of results.
        profit (float): The profit.
    """
    print("-" * 65)
    print(f"|                       Best actions path                       |")
    print("-" * 65)
    display_actions(results)
    print("-" * 65)
    print(f"            For the best profit : {round(profit, 2)}€")
    print("-" * 65)

def build_tree(actions: list, current_profit: float, current_cost: int, current_path: list) -> tuple[list, float]:
    """
    Build a recursive tree for the best actions path to take. Based on a brute-force algorithm (all combinations).
    Args:
        actions (list): The list of actions.
        current_profit (float): The current profit.
        current_cost (int): The current cost.
        current_path (list): The current path of actions.

    Returns:
    A tuple of the list of best actions and the total profit.
    """
    if not actions:
        print("All actions are done.")
        return current_path, current_profit

    action = actions[0]
    action_cost = action[1]
    action_profit = action[3]

    # Right branch
    print(f"Building right tree without action {action[0]}...")
    right_best_path, right_best_profit = build_tree(actions[1:].copy(), current_profit, current_cost,
                                                    current_path)

    # Left branch
    if current_cost + action_cost <= MAX_COST:
        new_path = current_path + [action]
        print(f"Building left tree with action {action[0]}...")
        left_best_path, left_best_profit = build_tree(actions[1:], current_profit + action_profit,
                                                      current_cost + action_cost, new_path)
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
    """
    The main method.
    """
    # 20 actions
    timer = Timer()

    actions = get_actions()

    display_actions(actions=actions)

    best_path, best_profit = build_tree(actions=actions, current_profit=0.0, current_cost=0, current_path=[])

    display_results(results=best_path, profit=best_profit)

    time_20 = timer.get_time()

    # 10 actions
    timer.restart()

    actions = get_actions()[10:]

    display_actions(actions=actions)

    best_path, best_profit = build_tree(actions=actions, current_profit=0.0, current_cost=0, current_path=[])

    display_results(results=best_path, profit=best_profit)

    time_10 = timer.get_time()

    # 3 actions
    timer.restart()

    actions = [["action-1", 3, 12, 0.36], ["action-2", 2, 9, 0.18], ["action-3", 4, 19, 0.76]]

    display_actions(actions=actions)

    best_path, best_profit = build_tree(actions=actions, current_profit=0.0, current_cost=0, current_path=[])

    display_results(results=best_path, profit=best_profit)

    time_3 = timer.get_time()

    print()
    print(f"Brute-force algorithm for 3 actions executed in : {time_3*1000: .3f} milliseconds.\n")
    print(f"Brute-force algorithm for 10 actions executed in : {time_10*1000: .3f} milliseconds.\n")
    print(f"Brute-force algorithm for 20 actions executed in : {time_20: .3f} seconds.\n")


if __name__ == "__main__":
    main()
