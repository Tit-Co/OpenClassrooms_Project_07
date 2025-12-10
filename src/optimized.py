import os
import pandas as pd
from pathlib import Path


ACTIONS_FILE = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"

CURRENT_DIR = Path(os.getcwd())

ACTIONS_FILEPATH = CURRENT_DIR / "../data" / ACTIONS_FILE

MAX_COST = 500


def get_actions() -> list | None:
    """
    Get actions from a file. Round the cost of actions calling int method.
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

def get_actions_2() -> list | None:
    """
    Get actions from a file. Multiply the cost of actions in order to manipulate integer numbers.
    Returns:
    The list of actions.
    """
    try:
        df = pd.read_csv(ACTIONS_FILEPATH)
        actions_list = df.values.tolist()
        actions_list.remove(actions_list[0])

        actions = []

        for action in actions_list:
            cost = int(float(action[1]) * 100)
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
    print(f"{'ACTION':<15} {'COST (€)':<10} {'BENEFICE (%)':<25} {'PROFIT (€)':<12}")
    print("-" * 65)

    for action in actions:
        name = action[0]
        cost = action[1]
        benefit = action[2]
        profit = action[3]

        print(f"{name:<15} {cost:<10} {benefit:<25} {profit:<12}")

    print()

def real_values(best_profit: float, total_cost: float, best_path: list) -> tuple[float, float, list]:
    """
    Return the real values of costs and profits in a list of actions given.
    Args:
        best_profit (float): The profit of the best action
        total_cost (float): The total cost of the best action
        best_path (list): The list of action

    Returns:
    A tuple of the real values of costs and profits and the list of updated actions.
    """
    new_best_profit = best_profit / 100
    new_total_cost = total_cost / 100
    new_best_path = [
        [action[0], round(action[1] / 100, 2), action[2], round(action[3] / 100, 2)]
        for action in best_path
    ]
    return new_best_profit, new_total_cost, new_best_path

def display_results(results: list, profit: float, cost:float) -> None:
    """
    Display the results list of action and profit and cost calculation. Call the display_actions() method.
    Args:
        results (list): The list of results actions.
        profit (float): The total profit.
        cost (float): The total cost.
    """
    print("-" * 65)
    print(f"|                       Best actions path                       |")
    print("-" * 65)
    display_actions(actions=results)
    print("-" * 65)
    print(f"   WITH BEST PROFIT = {profit}€, and TOTAL COST = {cost}€")
    print("-" * 65)

def max_profits(actions: list, max_cost: int) -> tuple[int, list[list[int]]]:
    """
    Get the maximum profit for the given list of actions. Based on the Dynamic Programming optimization algorithm.
    Args:
        actions (list): The list of actions.
        max_cost (int): The maximum cost to spend.

    Returns:
    A tuple of the maximum profit realizable for the given list of actions and the costs table.
    """
    actions_profits = [action[3] for action in actions]
    actions_costs = [action[1] for action in actions]

    n = len(actions)

    costs_table = [[0 for _ in range(max_cost + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for c in range(max_cost + 1):
            if actions_costs[i - 1] > c:
                costs_table[i][c] = costs_table[i - 1][c]
            else:
                costs_table[i][c] = max(costs_table[i - 1][c],
                                        costs_table[i - 1][c - actions_costs[i - 1]] + actions_profits[i - 1])

    return costs_table[n][max_cost], costs_table

def optimized_solution(actions: list, max_cost: int) -> tuple[float, int, list]:
    """
    Generate the optimal solution for the given list of actions. Based on the Dynamic Programming optimization algorithm.
    Args:
        actions (list): The list of actions.
        max_cost (int): The maximum cost to spend.

    Returns:
    A tuple of the best profit realizable for the given list of actions, the total cost,
    and the backtracked list of actions.
    """
    actions_costs = [action[1] for action in actions]

    n = len(actions)

    max_profit, costs_table = max_profits(actions, max_cost)

    cost = max_cost
    selection = []
    total_cost = 0

    for i in range(n, 0, -1):
        if costs_table[i][cost] != costs_table[i - 1][cost]:
            selection.append(actions[i - 1])
            cost -= actions_costs[i - 1]
            total_cost += actions_costs[i - 1]

    return round(max_profit, 2), total_cost, selection

def main():
    """
    The main method.
    """
    # actions = get_actions()
    #
    # # Short list for test purpose
    # # actions = [["action-1", 3, 12, 0.36], ["action-2", 2, 9, 0.18], ["action-3", 4, 19, 0.76]]
    #
    # print("List of actions :\n")
    # display_actions(actions=actions)
    #
    # best_profit, total_cost, best_path = optimized_solution(actions=actions, max_cost=MAX_COST)
    #
    # display_results(results=best_path, profit=best_profit, cost=total_cost)

    actions = get_actions_2()

    # Short list for test purpose
    # actions = [["action-1", 3, 12, 0.36], ["action-2", 2, 9, 0.18], ["action-3", 4, 19, 0.76]]

    print("List of actions :\n")
    display_actions(actions=actions)

    best_profit, total_cost, best_path = optimized_solution(actions=actions, max_cost=MAX_COST * 100)

    real_best_profit, real_total_cost, real_best_path = real_values(best_profit, total_cost, best_path)

    display_results(results=real_best_path, profit=real_best_profit, cost=real_total_cost)


if __name__ == "__main__":
    main()
