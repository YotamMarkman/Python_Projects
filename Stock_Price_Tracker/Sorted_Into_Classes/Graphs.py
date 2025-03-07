import pandas as pd
import matplotlib.pyplot as plt



#Class which uses the pandas and matplotlib classes to create and add data
# to graphs to help user see his/her stock effciency

class DataManager:
    def __init__(self):
        """Initialize an empty DataFrame to store data."""
        self.df = pd.DataFrame(columns=["Standard Deviation", "Expectation"])
        

    def add_data(self, standard_deviation: float, expectation: float):
        """Adds new data to the DataFrame without plotting immediately."""
        new_data = {"Standard Deviation": standard_deviation, "Expectation": expectation}
        self.df = self.df._append(new_data, ignore_index=True)

    def plot_line_chart(self):
        """Plots the stored data as a single graph."""
        if self.df.empty:
            print("No data available to plot.")
            return
        plt.figure(figsize=(8, 5))
        plt.plot(self.df["Standard Deviation"], self.df["Expectation"], marker="o", linestyle="--", color="b", label="Efficiency")
        plt.title("Portfolio Efficiency")
        plt.xlabel("Standard Deviation")
        plt.ylabel("Expectation")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    manager = DataManager()
    manager.add_data(4.65,8.9)
    manager.add_data(5.65,8.5)
    manager.add_data(3.65,9.9)
    manager.plot_line_chart()