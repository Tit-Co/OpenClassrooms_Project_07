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
    print(f"{'ACTION':<15} {'COST (€)':<10} {'BENEFICE (%)':<15} {'PROFIT (€)':<12}")
    print("-" * 65)

    for action in actions_list:
        name = action[0]
        cost = action[1]
        benefit = action[2]
        profit = action[3]

        print(f"{name:<15} {cost:<10} {benefit:<15} {profit:<12}")

    print()

def display_results(results_list, profit):
    print("-" * 65)
    print(f"|                       Best actions path                       |")
    print("-" * 65)
    display_actions(results_list)
    print("-" * 65)
    print(f"            For the best profit : {profit}€")
    print("-" * 65)

def max_profits(actions_list, max_cost):
    actions_profits = [action[3] for action in actions_list]
    actions_costs = [action[1] for action in actions_list]

    n = len(actions_list)

    costs_table = [[0 for _ in range(max_cost + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for c in range(max_cost + 1):
            if actions_costs[i - 1] > c:
                costs_table[i][c] = costs_table[i - 1][c]
            else:
                costs_table[i][c] = max(costs_table[i - 1][c],
                                        costs_table[i - 1][c - actions_costs[i - 1]] + actions_profits[i - 1])

    return costs_table[n][max_cost], costs_table

def optimized_solution(actions_list, max_cost):
    actions_costs = [action[1] for action in actions_list]

    n = len(actions_list)

    max_profit, costs_table = max_profits(actions_list, max_cost)

    cost = max_cost
    selection = []

    for i in range(n, 0, -1):
        if costs_table[i][cost] != costs_table[i - 1][cost]:
            selection.append(actions_list[i - 1])
            cost -= actions_costs[i - 1]

    return max_profit, selection

def main():
    actions = get_actions()

    # list for test
    # actions = [["action-1", 3, 12, 0.36], ["action-2", 2, 9, 0.18], ["action-3", 4, 19, 0.76]]

    print("List of actions :\n")
    display_actions(actions)

    best_profit, best_path = optimized_solution(actions, MAX_COST)

    display_results(best_path, best_profit)


if __name__ == "__main__":
    main()
