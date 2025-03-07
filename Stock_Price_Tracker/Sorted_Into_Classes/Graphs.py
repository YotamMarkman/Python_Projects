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
        plt.plot(self.df["Standard Deviation"], self.df["Expectation"], marker="o", linestyle="--", color="b", label="Expectation")
        plt.title("Standard Deviation vs Expectation")
        plt.xlabel("Standard Deviation")
        plt.ylabel("Expectation")
        plt.legend()
        plt.grid(True)
        plt.show()

# # Example Usage
# if __name__ == "__main__":
#     manager = DataManager()

#     # Adding data (but not plotting yet)
#     manager.add_data(5, 50)
#     manager.add_data(10, 80)
#     manager.add_data(15, 100)

#     # Plot only when requested
#     manager.plot_line_chart()
