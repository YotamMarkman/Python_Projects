import tkinter as tk
from tkinter import messagebox, simpledialog
import yfinance as yf
import requests
from PortfolioManager import PortfolioManager
from StockAPI import StockAPI
import sys
from InvestmentManager import InvestmentManager
from ExpectationAndDeviationCalc import ExpectationAndDeviationCalc
from Graphs import DataManager


API_key = "156DW7OTQGTLJESV"

class StockGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="lightblue")
        self.root.title("Stock Tracker")
        self.expectanddeviate = ExpectationAndDeviationCalc()
        self.api = StockAPI()
        self.portfolio_manager = PortfolioManager()
        self.investment_manager = InvestmentManager()
        self.graph = DataManager()
        self.ticker_var = tk.StringVar()
        self.price_ticker = tk.StringVar(value="")
        self.investment_manager.set_update_callback(self.update_investment_amount_label)
        self.ticker_var.trace_add("write", self.update_price_ticker)
        self.build_gui()

        # Ask for the investment amount on startup
        self.investment_manager.ask_for_investment_amount(self.root)

    def build_gui(self):
        # Investment Section
        tk.Label(self.root, text="Amount:", bg="lightblue", fg="white").grid(row=0, column=0, padx=10, pady=10)
        self.amount_label = tk.Label(self.root, text="$0.00", bg="lightblue", fg="white")
        self.amount_label.grid(row=0, column=1, padx=10, pady=10)
        self.update_investment_amount_label()

        # Stock Entry
        tk.Label(self.root, text="Enter Stock Name:", bg="lightblue", fg="white").grid(row=1, column=0, padx=10, pady=10)
        self.stock_name_entry = tk.Entry(self.root, width=30)
        self.stock_name_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Find Ticker", command=self.fetch_stock_data).grid(row=1, column=2, padx=10, pady=10)

        # Display Ticker
        tk.Label(self.root, text="Last Found Ticker:", bg="lightblue", fg="white").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.ticker_var, state="readonly", width=30).grid(row=2, column=1, padx=10, pady=10)
        
        # Display price of stock
        tk.Label(self.root, text="Price Per Share", bg="lightblue", fg="white").grid(row=3,column=0,padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.price_ticker, state="readonly", width=30).grid(row=3,column=1,padx=10, pady=10)
        
        # Portfolio Section
        tk.Label(self.root, text="Portfolio:", bg="lightblue", fg="white").grid(row=5, column=0, padx=10, pady=10)
        self.portfolio_listbox = tk.Listbox(self.root, height=10, width=50)
        self.portfolio_listbox.grid(row=5, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Add to Portfolio", command=self.add_to_portfolio).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Show Portfolio", command=self.show_portfolio).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Remove Stock", command=self.remove_stock).grid(row=10, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Show Data", command=self.show_stock_data).grid(row=4, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Add Funds", command=self.add_funds_to_amount).grid(row= 10, column= 1, padx=10, pady=10)
        tk.Button(self.root, text="Exit Program", command=self.close_program).grid(row= 10, column= 0, padx=10, pady=10)
        tk.Button(self.root, text="Show Graph", command=self.show_graph).grid(row= 7, column= 2, padx=10, pady=10)
    
    def update_investment_amount_label(self):
        amount = self.investment_manager.get_investment_amount()
        if amount is not None:
            self.amount_label.config(text=f"${amount:.2f}")
            
    def show_graph(self):
        self.graph.plot_line_chart()
    
    def update_price_ticker(self, *args):
        ticker = self.ticker_var.get()
        if ticker:
            price = self.api.stock_price_per_share(ticker)
            print(price) 
            if price:
                self.price_ticker.set(f"${price:.2f}")
            else:
                self.price_ticker.set("Price not available")
    
    def close_program(self):
        sys.exit()
                
    def add_funds_to_amount(self):
        added_funds = simpledialog.askinteger("Amount You Wish to Add", "Please enter an amount?")
        if not added_funds:
            messagebox.showerror("Input Error", "Please provide an amount.")
            return
        amount = self.investment_manager.get_investment_amount()
        amount = amount + added_funds
        if amount is not None:
            self.amount_label.config(text=f"${amount:.2f}")
        return

    def fetch_stock_data(self):
        stock_name = self.stock_name_entry.get()
        if not stock_name:
            messagebox.showerror("Input Error", "Please enter a stock name.")
            return
        ticker = self.api.return_ticker(stock_name)
        if ticker == "No ticker found":
            messagebox.showerror("Error", ticker)
        else:
            self.ticker_var.set(ticker)
            messagebox.showinfo("Ticker Found", f"The ticker for {stock_name} is: {ticker}")

    def add_to_portfolio(self):
        ticker = self.ticker_var.get()
        if not ticker:
            messagebox.showerror("Input Error", "No ticker to add. Find a ticker first.")
            return
        requested_amount = simpledialog.askstring(f"Amount of {ticker} shares","How many shares would you like to buy?")
        if not requested_amount:
            messagebox.showerror("Input Error", "Please provide an amount.")
            return
        total = int(requested_amount) * self.api.stock_price_per_share(ticker)
        amount = self.investment_manager.get_investment_amount()
        if int(amount) < total:
            messagebox.showerror("Input Error", "Insufficent Funds!")
            return
        prices = []
        prices = self.expectanddeviate.history_of_prices(ticker)
        expectation = self.expectanddeviate.calc_expectation(prices)
        deviation = self.expectanddeviate.calculate_deviation(prices)
        self.graph.add_data(deviation,expectation)
        company_name = self.portfolio_manager.add_stock(ticker, int(requested_amount))
        self.portfolio_listbox.insert(tk.END, f"{company_name}: {ticker}")
        messagebox.showinfo("Success", f"{ticker} added to your portfolio.")


    def remove_stock(self):
        selected = self.portfolio_listbox.curselection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a ticker from the portfolio.")
            return
        selected_index = selected[0]
        self.portfolio_listbox.delete(selected_index)
        self.portfolio_manager.remove_stock(selected_index)
        messagebox.showinfo("Success", "Selected stock removed from portfolio.")

    def show_portfolio(self):
        portfolio_string = self.portfolio_manager.get_portfolio_string()
        if portfolio_string:
            messagebox.showinfo("Portfolio", f"Your portfolio:\n{portfolio_string}")
        else:
            messagebox.showinfo("Portfolio", "Your portfolio is empty.")

    def show_stock_data(self):
        selected = self.portfolio_listbox.curselection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a ticker from the portfolio.")
            return
        selected_index = selected[0]
        ticker = self.portfolio_manager.get_portfolio()[selected_index]["ticker"]
        time_frame = simpledialog.askstring("Time Frame", "Enter the time frame (e.g., 1d, 1mo, 1y):")
        if not time_frame:
            messagebox.showerror("Input Error", "Please provide a valid time frame.")
            return
        data = self.api.history_of_spec_stock(ticker, time_frame)
        popup = tk.Toplevel(self.root)
        popup.title("Stock Data")
        tk.Text(popup, wrap=tk.WORD, height=15, width=50).pack(padx=10, pady=10)

    def run(self):
        self.root.mainloop()


# Run the GUI
if __name__ == "__main__":
    app = StockGUI()
    app.run()    