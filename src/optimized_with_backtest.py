from src.optimized import display_results, optimized_solution, real_values
from src.backtest.statistics import Statistics
from src.backtest.display import display_title, display_dataset, display_space, display_trash, display_separator
from src.backtest.visualizer import Visualizer
from src.backtest.filter import filter_actions

import pandas as pd
import os
from pathlib import Path


DATASET_1 = "dataset_1.csv"

DATASET_2 = "dataset_2.csv"

SIENNA_SOLUTION_1 = "sienna_solution_1.txt"

SIENNA_SOLUTION_2 = "sienna_solution_2.txt"

CURRENT_DIR = Path(os.getcwd())

ACTIONS_FILEPATH_1 = CURRENT_DIR / "../data" / DATASET_1

ACTIONS_FILEPATH_2 = CURRENT_DIR / "../data" / DATASET_2

SIENNA_FILEPATH_1 = CURRENT_DIR / "../data" / SIENNA_SOLUTION_1

SIENNA_FILEPATH_2 = CURRENT_DIR / "../data" / SIENNA_SOLUTION_2

MAX_COST = 500


def get_actions(actions_path: Path) -> list | None:
    """
    Get all actions from the given actions filepath.
    Args:
        actions_path (Path): The path of the actions file.

    Returns:
    A list of the actions or None if there are no actions when reading errors.
    """
    try:
        df = pd.read_csv(actions_path)
        actions_list = df.values.tolist()
        actions_list.remove(actions_list[0])

        actions = []

        for action in actions_list:
            cost = float(action[1])
            profit = float(action[2])
            if cost > 0:
                benefit = float((profit / cost) * 100)
            else:
                benefit = "unknown"
            actions.append([action[0], cost, benefit, profit])

        return actions

    except Exception as e:
        print(f"ERROR reading {actions_path}: {e}")
        return None

def multiply_actions(actions: list) -> list:
    """
    Multiply actions float costs and profits in order to manipulate integers.
    Args:
        actions (list): The list of actions.

    Returns:
    A list of the actions after multiplying costs and profits.
    """
    multiplied_actions = []
    for action in actions:
        cost = float(action[1]) * 100
        profit = float(action[3]) * 100
        new_action = [action[0], int(cost), action[2], int(profit)]
        multiplied_actions.append(new_action)
    return multiplied_actions

def get_sienna_solutions(file_path: Path) -> tuple[list, float, float] | None:
    """
    Get list of actions in Sienna solutions based on the given file path.
    Args:
        file_path (Path): The path of the Sienna solutions file.

    Returns:
    A tuple of the list of actions in Sienna solutions, the total cost and total profit.
    """
    try:
        with open(file_path, "r", encoding="utf8") as file:
            actions=[]
            total_cost = 0
            total_profit = 0
            lines = file.readlines()
            for i, line in enumerate(lines):
                if "Share" in line:
                    action = []
                    action_name = line.split()[0]
                    action.append(action_name)
                    if len(line.split()) > 1:
                        action_cost = float(int(line.split()[1]) / 100)
                        action.append(action_cost)
                    actions.append(action)

                elif "Total cost" in line:
                    total_cost = float(line.split(": ")[1].split('€')[0])

                elif "Total return" in line or "Profit" in line:
                    total_profit = float(line.split(": ")[1].split('€')[0])

                else:
                    continue

            return actions, total_cost, total_profit

    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return None

def check_sienna_solutions(dataset: str,
                           sienna_solution_actions: list,
                           sienna_total_cost: float,
                           sienna_total_profit: float,
                           dataset_actions: list) -> list:
    """
    Check the Sienna solutions compared to the datas in the given dataset.
    Args:
        dataset (str): The name of the dataset.
        sienna_solution_actions (list): The list of actions in Sienna solutions.
        sienna_total_cost (float): The total cost of the Sienna solutions.
        sienna_total_profit (float): The total profit of the Sienna solutions.
        dataset_actions (list): The list of actions in the dataset

    Returns:
    A tuple of corrected datas of Sienna solutions, if required
    """
    final_actions = []
    real_total_cost = 0
    real_total_profit = 0
    for action in sienna_solution_actions:
        for dataset_action in dataset_actions:
            if action[0] == dataset_action[0]:
                if len(action) > 1 and action[1] != dataset_action[1]:
                    print(f"The cost of action {action[0]} in {dataset} is wrong. "
                          f"Should be {dataset_action[1]}€ instead of {action[1]}€. Data corrected.")
                real_total_cost += dataset_action[1]
                real_total_profit += dataset_action[3]
                final_actions.append(dataset_action)

    if sienna_total_cost != real_total_cost:
        print(f"{dataset} has a real total cost of {round(real_total_cost, 2)}€ "
              f"instead of {sienna_total_cost}€.")
    else:
        print(f"{dataset} total cost ok.")

    if sienna_total_profit != real_total_profit:
        print(f"{dataset} has a real total profit of {round(real_total_profit, 2)}€ "
              f"instead of {sienna_total_profit}€.")
    else:
        print(f"{dataset} total profit ok.")

    return final_actions

def process_statistics(dataset: str, actions: list) -> None:
    display_title("STATISTICS")

    statistics = Statistics()

    statistics.display(dataset=dataset, actions=actions)

def process_visualization(dataset: str, dataframe: pd.DataFrame, log_scale: bool, visualizer: Visualizer) -> None:
    display_title(f"VISUALIZATION OF {dataset}")

    visualizer.all(dataset=dataset, dataframe=dataframe, log_scale=log_scale)

def process_dataset(dataset: str, path: Path, sienna_path: Path, log_scale: bool, visualizer: Visualizer) -> None:
    actions = get_actions(actions_path=path)

    multiplied_actions = multiply_actions(actions=actions)

    display_dataset(dataset=dataset, actions=actions)

    display_space()

    # Calculate optimized solution
    filtered, duplicated_trash, not_positive_trash = filter_actions(actions=multiplied_actions)

    best_profit, total_cost, best_path = optimized_solution(actions=filtered, max_cost=MAX_COST * 100)

    real_best_profit, real_total_cost, real_best_path = real_values(best_profit, total_cost, best_path)

    display_results(results=real_best_path, profit=real_best_profit, cost=real_total_cost)

    display_space()

    display_trash(dataset=dataset, duplicated=duplicated_trash, not_positive=not_positive_trash)

    display_space()

    # Statistics
    process_statistics(dataset=dataset, actions=filtered)

    display_separator()

    # Visualization
    dataframe = to_dataframe(filter_actions(actions=actions)[0])
    process_visualization(dataset=dataset, dataframe=dataframe, log_scale=log_scale, visualizer=visualizer)

    display_space()

    # My solution for dataset - Backtest
    dataframe_bestpath = to_dataframe(real_best_path)
    process_visualization(dataset=f"My solution for {dataset}".upper(),
                          dataframe=dataframe_bestpath,
                          log_scale=(dataset=="DATASET 1"),
                          visualizer=visualizer)

    # Sienna solution for dataset - Backtest
    display_separator()

    sienna_choice, sienna_total_cost, sienna_total_profit = get_sienna_solutions(file_path=sienna_path)
    index_str = "1" if sienna_path==SIENNA_FILEPATH_1 else "2"
    checked_sienna_choice = check_sienna_solutions(
        dataset=f"SIENNA SOLUTION {index_str}",
        sienna_solution_actions=sienna_choice,
        sienna_total_cost=sienna_total_cost,
        sienna_total_profit=sienna_total_profit,
        dataset_actions=actions)

    display_dataset(dataset=f"SIENNA SOLUTION {index_str}", actions=checked_sienna_choice)

    dataframe_sienna = to_dataframe(checked_sienna_choice)
    if dataset.upper() == "DATASET 1":
        visualizer.roi_scatterplot_per_action(dataset=f"SIENNA SOLUTION FOR {dataset}",
                                              dataframe=dataframe_sienna,
                                              log_scale=False)
    else:
        process_visualization(dataset=f"SIENNA SOLUTION FOR {dataset}",
                              dataframe=dataframe_sienna,
                              log_scale=False,
                              visualizer=visualizer)

    display_space()

def round_actions_cost(actions: list) -> list:
    """
    Round the actions cost.
    Args:
        actions (list): The list of actions.

    Returns:
    The list of actions with rounded cost.
    """
    new_actions = []
    for action in actions:
        cost = round(action[1])
        new_actions.append([action[0], cost, action[2], action[3]])
    return new_actions

def to_dataframe(actions: list) -> pd.DataFrame:
    """
    Convert the actions list into a dataframe.
    Args:
        actions (list): The list of actions.

    Returns:
    The converted dataframe.
    """
    data = {"name": [action[0] for action in actions],
            "price": [action[1] for action in actions],
            "profit": [action[3] for action in actions]}

    dataframe = pd.DataFrame(data)

    return dataframe


def main():
    """
    The main method.
    """
    display_title("DATASETS")

    visualizer = Visualizer()

    process_dataset(dataset="DATASET 1",
                    path=ACTIONS_FILEPATH_1,
                    sienna_path=SIENNA_FILEPATH_1,
                    log_scale=True,
                    visualizer=visualizer)

    display_space()

    process_dataset(dataset="DATASET 2",
                    path=ACTIONS_FILEPATH_2,
                    sienna_path=SIENNA_FILEPATH_2,
                    log_scale=False,
                    visualizer=visualizer)


if __name__ == "__main__":
    main()
