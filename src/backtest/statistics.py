import numpy as np
from src.backtest.display import display_space

class Statistics:
    @staticmethod
    def calculate_average(costs: list, profits: list) -> tuple[float, float]:
        """
        Calculate average
        Args:
            costs (list): The costs
            profits (list): The profits

        Returns:
        A tuple of the average cost and the average profit
        """
        return round(np.mean(costs), 2), round(np.mean(profits), 2)

    @staticmethod
    def calculate_median(costs: list, profits: list) -> tuple[float, float]:
        """
        Calculate median
        Args:
            costs (list): The costs
            profits (list): The profits

        Returns:
        A tuple of the costs and profits medians
        """
        return round(np.median(costs), 2), round(np.median(profits), 2)

    @staticmethod
    def calculate_min(costs: list, profits: list) -> tuple[float, float]:
        """
        Calculate minimum
        Args:
            costs (list): The costs
            profits (list): The profits

        Returns:
        A tuple of the costs and profits minimums
        """
        return round(np.min(costs), 2), round(np.min(profits), 2)

    @staticmethod
    def calculate_max(costs: list, profits: list) -> tuple[float, float]:
        """
        Calculate maximum
        Args:
            costs (list): The costs
            profits (list): The profits

        Returns:
        A tuple of the costs and profits maximums
        """
        return round(np.max(costs), 2), round(np.max(profits), 2)

    @staticmethod
    def calculate_variance(costs: list, profits: list) -> tuple[float, float]:
        """
        Calculate variance
        Args:
            costs (list): The costs
            profits (list): The profits

        Returns:
        A tuple of the costs and profits variances
        """
        return round(np.var(costs), 2), round(np.var(profits), 2)

    @staticmethod
    def calculate_standard_deviation(costs: list, profits: list) -> tuple[float, float]:
        """
        Calculate standard deviation
        Args:
            costs (list): The costs
            profits (list): The profits

        Returns:
        A tuple of the costs and profits standard deviations
        """
        return round(np.std(costs), 2), round(np.std(profits), 2)

    def display(self, dataset: str, actions: list) -> None:
        """
        Display the statistics of a dataset. Call the different statistics methods.
        Args:
            dataset (str): The name of the dataset
            actions (list): The list of actions in the dataset
        """
        print(f"{dataset} statistics:\n")

        costs = [action[1] for action in actions]
        profits = [action[3] for action in actions]

        average1_costs, average1_profits = self.calculate_average(costs=costs, profits=profits)
        print(f"Average cost of actions : {average1_costs}€")
        print(f"Average profit of actions : {average1_profits}€")

        display_space()

        median1_costs, median1_profits = self.calculate_median(costs=costs, profits=profits)
        print(f"Median cost of actions : {median1_costs}€")
        print(f"Median profit of actions : {median1_profits}€")

        display_space()

        minimum1_costs, minimum1_profits = self.calculate_min(costs=costs, profits=profits)
        print(f"Minimum cost of actions : {minimum1_costs}")
        print(f"Minimum profit of actions : {minimum1_profits}")

        maximum1_costs, maximum1_profits = self.calculate_max(costs=costs, profits=profits)
        print(f"Maximum cost of actions : {maximum1_costs}")
        print(f"Maximum profit of actions : {maximum1_profits}")

        display_space()

        variance1_costs, variance1_profits = self.calculate_variance(costs=costs, profits=profits)
        print(f"Variance cost of actions : {variance1_costs}")
        print(f"Variance profit of actions : {variance1_profits}")

        display_space()

        deviance1_costs, deviance1_profits = self.calculate_standard_deviation(costs=costs, profits=profits)
        print(f"Deviance cost of actions : {deviance1_costs}")
        print(f"Deviance profit of actions : {deviance1_profits}")

        display_space()