import os
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from pathlib import Path


CURRENT_DIR = Path(os.getcwd())


class Visualizer:
    def __init__(self):
        self.index = 1

    @staticmethod
    def save_fig(fig: Figure, dataset: str, path: Path) -> None:
        fig.savefig(f"{path}")
        print(f"⯈ Costs bar chart saved for {dataset} : {path}")

    def costs_bar_chart_per_action(self, dataset: str, dataframe: pd.DataFrame) -> None:
        """
        Generate a bar chart per action based on the given dataframe.
        Args:
            dataset (str): The name of the dataset
            dataframe (DataFrame): The Pandas dataframe
        """
        name_col = 'name' if 'name' in dataframe.columns else ('action' if 'action' in dataframe.columns else None)

        statistics = dataframe.describe()

        fig = plt.figure(figsize=(24, 12))
        plt.bar(dataframe[name_col], dataframe['price'], color='blue')
        plt.title(f"Bar chart of the costs of actions in {dataset}".upper())
        plt.xlabel('Action')
        plt.ylabel('Price')
        plt.xticks(rotation=90, ha='right')
        plt.tight_layout()
        plt.axhline(y=statistics['price']['mean'], color='red')
        plt.axhline(y=statistics['price']['std'], color='green')
        plt.legend(['Prices Mean', 'Prices Standard deviation', 'Prices'])
        plt.show()

        image_name = f"{self.index}_costs_barchart_" + dataset.replace(' ', '_').lower() + ".png"
        path = CURRENT_DIR / "data" / "images" / image_name
        self.save_fig(fig, dataset, path)

        self.index += 1
        plt.close(fig)

    def profits_bar_chart_per_action(self, dataset: str, dataframe: pd.DataFrame) -> None:
        """
        Generate a bar chart per action based on the given dataframe.
        Args:
            dataset (str): The name of the dataset
            dataframe (DataFrame): The Pandas dataframe
        """

        name_col = 'name' if 'name' in dataframe.columns else ('action' if 'action' in dataframe.columns else None)

        statistics = dataframe.describe()

        fig = plt.figure(figsize=(24, 12))
        plt.bar(dataframe[name_col], dataframe['profit'], color='orange')
        plt.title(f"Bar chart of the profits of actions in {dataset}".upper())
        plt.xlabel('Action')
        plt.ylabel('Profit')
        plt.xticks(rotation=90, ha='right')
        plt.tight_layout()
        plt.axhline(y=statistics['profit']['mean'], color='red')
        plt.axhline(y=statistics['profit']['std'], color='green')
        plt.legend(['Profits Mean', 'Profits Standard deviation', 'Profits'])
        plt.show()

        image_name = f"{self.index}_profits_barchart_" + dataset.replace(' ', '_').lower() + ".png"
        path = CURRENT_DIR / "data" / "images" / image_name
        self.save_fig(fig, dataset, path)
        self.index += 1
        plt.close(fig)

    def costs_profits_boxplot_per_action(self, dataset: str, dataframe: pd.DataFrame, log_scale: bool) -> None:
        """
        Generate a box plot per action based on the given dataframe.
        Change the scale to logarithmic scale accordingly to boolean given.
        Args:
            dataset (str): The name of the dataset
            dataframe (DataFrame): The Pandas dataframe
            log_scale (bool): The boolean flag
        """
        df_prices = pd.to_numeric(dataframe['price'], errors='coerce')

        df_profits = pd.to_numeric(dataframe['profit'], errors='coerce')

        fig = plt.figure(figsize=(24, 12))
        plt.boxplot([df_prices, df_profits], tick_labels=["Costs", "Profits"])
        if log_scale:
            plt.yscale('log')

        plt.title(f"Costs and Profits Comparison in {dataset}".upper())
        plt.show()

        image_name = f"{self.index}_boxplot_" + dataset.replace(' ', '_').lower() + ".png"
        path = CURRENT_DIR / "data" / "images" / image_name
        self.save_fig(fig, dataset, path)
        self.index += 1

        plt.close(fig)

    def roi_scatterplot_per_action(self, dataset: str, dataframe: pd.DataFrame, log_scale: bool) -> None:
        """
        Generate a scatter plot per action based on the given dataframe.
        Change the scale to logarithmic scale accordingly to boolean given.
        Args:
            dataset (str): The name of the dataset
            dataframe (DataFrame): The Pandas dataframe
            log_scale (bool): The boolean flag
        """
        dataframe = dataframe.copy()
        dataframe['price'] = pd.to_numeric(dataframe['price'], errors='coerce')
        dataframe['profit'] = pd.to_numeric(dataframe['profit'], errors='coerce')
        dataframe['roi'] = dataframe['profit'] / dataframe['price']

        dataframe = dataframe.dropna(subset=['price', 'profit', 'roi'])
        dataframe = dataframe[dataframe['price'] > 0]
        dataframe = dataframe[dataframe['profit'] > 0]
        dataframe = dataframe[dataframe['roi'] > 0]

        fig = plt.figure(figsize=(24, 12))
        plt.scatter(dataframe['price'], dataframe['profit'], c=dataframe['roi'], cmap='viridis', alpha=0.7)
        plt.colorbar(label="ROI")

        if log_scale:
            plt.xscale('log')

        plt.xlabel("Cost")
        plt.ylabel("Profit")
        plt.title(f"Profit vs Cost colored by ROI in {dataset}".upper())
        plt.show()

        image_name = f"{self.index}_scatterplot_" + dataset.replace(' ', '_').lower() + ".png"
        path = CURRENT_DIR / "data" / "images" / image_name

        self.save_fig(fig, dataset, path)
        self.index += 1

        plt.close(fig)

    def all(self, dataset: str, dataframe: pd.DataFrame, log_scale: bool) -> None:
        """
        Generate all diagrams based on the given dataframe.
        Change the scale to logarithmic scale accordingly to boolean given.
        Args:
            dataset (str): The name of the dataset
            dataframe (DataFrame): The Pandas dataframe
            log_scale (bool): The boolean flag
        """
        print(f"• Visualizing {dataset}...")

        self.costs_bar_chart_per_action(dataset=dataset, dataframe=dataframe)
        self.profits_bar_chart_per_action(dataset=dataset, dataframe=dataframe)
        self.costs_profits_boxplot_per_action(dataset=dataset, dataframe=dataframe, log_scale=log_scale)
        self.roi_scatterplot_per_action(dataset=dataset, dataframe=dataframe, log_scale=log_scale)
