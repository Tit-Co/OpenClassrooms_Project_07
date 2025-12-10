import pandas as pd


def filter_not_positive_actions(actions: list) -> tuple[list, list]:
    """
    Filter out actions that do not have positive values.
    Args:
        actions (list): The list of actions.

    Returns:
    A tuple of the actions after filtering out actions that do not have positive values
    and the list of removed actions (trash).
    """
    cleaned = []
    trash = []
    for action in actions:
        try:
            cost = action[1]
            if cost > 0:
                cleaned.append(action)
            else:
                trash.append(action)

        except (ValueError, TypeError):
            trash.append(action)
            print(f"Invalid action (conversion error): {action}")

    return cleaned, trash

def filter_duplicated_actions(actions: list) -> tuple[list, list]:
    """
    Filter out duplicated actions.
    Args:
        actions (list): The list of actions.

    Returns:
    A tuple of the actions after filtering out duplicated actions and the list of removed actions (trash).
    """
    cleaned = []
    trash = []
    already = set()

    for action in actions:
        action_tuple = tuple(action)

        if action_tuple not in already:
            cleaned.append(action)
            already.add(action_tuple)
        else:
            trash.append(action)

    return cleaned, trash

def filter_actions(actions: list) -> tuple[list, list, list]:
    """
    Filter the actions. Call the filtering methods.
    Args:
        actions (list): The list of actions.

    Returns:
    A tuple of the filtered actions after filtering out actions and the lists of removed actions (trash).
    """
    unique_actions, duplicated_trash = filter_duplicated_actions(actions)

    filtered_actions, not_positive_trash = filter_not_positive_actions(unique_actions)

    return filtered_actions, duplicated_trash, not_positive_trash

def filter_dataframe(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Filter out the datas in the column from the dataframe.
    Remove the not numeric elements, the NaN elements, the duplicated elements and the not positive elements.
    Args:
        dataframe (DataFrame): The dataframe to filter.
        column_name (str): The name of the column to filter.

    Returns:
    The filtered dataframe.
    """
    dataframe = dataframe.copy()
    dataframe[column_name] = pd.to_numeric(dataframe[column_name], errors='coerce')

    dataframe = (
        dataframe.dropna(subset=[column_name])
        .drop_duplicates(subset=[column_name])
    )
    dataframe = dataframe[dataframe[column_name] > 0]
    return dataframe
