from src.optimized import display_actions

def display_title(title: str) -> None:
    """
    Display a title.
    Args:
        title (str): The title to display.
    """
    str_length = len(title)
    spaces = int((65 - (str_length + 2)) / 2)
    print("-" * 65)
    if str_length % 2 == 0:
        print("|" + " " * spaces + f"{title}" + " " * (spaces + 1) + "|")
    else:
        print("|" + " " * spaces + f"{title}" + " " * spaces + "|")

    print("-" * 65)

def display(actions: list) -> None:
    """
    Display the actions. Call display actions method.
    Args:
        actions (list): The list of actions.
    """
    display_title("LIST OF ACTIONS")
    display_actions(actions=actions)

def display_dataset(dataset: str, actions: list) -> None:
    """
    Display the actions list in a dataset. Call display actions method.
    Args:
        dataset (str): The name of the dataset.
        actions (list): The list of actions.
    """
    str_length = len(dataset)
    print()
    print("_" * (str_length + 4))
    print(f"| {dataset} |")
    display(actions=actions)

def display_trash(dataset: str, duplicated: list, not_positive) -> None:
    """
    Display the actions list in a trash.
    Args:
        dataset (str): The name of the dataset.
        duplicated (list): The list of duplicated actions.
        not_positive (list): The list of not positive actions.
    """
    print(f"Duplicated actions in {dataset} : {len(duplicated)}")
    print(f"Not positive cost actions in {dataset} : {len(not_positive)}")

def display_separator():
    """
    Display a dah line.
    """
    display_space()
    print("-" * 65)

def display_space():
    print()