import os
import pandas as pd
from pathlib import Path


ACTIONS_FILE = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

CURRENT_DIR = Path(os.getcwd())

ACTIONS_FILEPATH = CURRENT_DIR / "../data" / ACTIONS_FILE

MAX_COST = 500


def get_actions() -> list | None:
    """
    Get the list of actions from a file.
    Returns:
    The list of actions.
    """
    try:
        df = pd.read_csv(ACTIONS_FILEPATH)
        actions_list = df.values.tolist()
        actions_list.remove(actions_list[0])

        actions = []

        for action in actions_list:
            cost = int(action[1])
            benefice = int(action[2].strip('%'))
            profit = float((benefice / 100) * cost)
            action = [action[0], cost, benefice, profit]
            actions.append(action)
            print(action)
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
    print(f"            For the best profit : {profit}€")
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
    right_best_path, right_best_profit = build_tree(actions=actions[1:].copy(),
                                                    current_profit=current_profit,
                                                    current_cost=current_cost,
                                                    current_path=current_path)

    # Left branch
    if current_cost + action_cost <= MAX_COST:
        new_path = current_path + [action]
        print(f"Building left tree with action {action[0]}...")
        left_best_path, left_best_profit = build_tree(actions=actions[1:],
                                                      current_profit=current_profit + action_profit,
                                                      current_cost=current_cost + action_cost,
                                                      current_path=new_path)
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
    actions = get_actions()

    display_actions(actions=actions)

    best_path, best_profit = build_tree(actions=actions, current_profit=0.0, current_cost=0, current_path=[])

    display_results(results=best_path, profit=best_profit)


if __name__ == "__main__":
    main()
