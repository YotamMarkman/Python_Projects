import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import requests

API_key = "156DW7OTQGTLJESV"

# Functions
def return_ticker(full_name_of_stock: str) -> str:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": full_name_of_stock,
        "apikey": API_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "bestMatches" in data and data["bestMatches"]:
        return data["bestMatches"][0]["1. symbol"]
    else:
        return "No ticker found"

def fetch_stock_data():
    stock_name = stock_name_entry.get()
    if not stock_name:
        messagebox.showerror("Input Error", "Please enter a stock name.")
        return

    ticker = return_ticker(stock_name)
    if "No ticker found" in ticker:
        messagebox.showerror("Error", ticker)
    else:
        messagebox.showinfo("Ticker Found", f"The ticker for {stock_name} is: {ticker}")
        ticker_var.set(ticker)

def add_to_portfolio():
    ticker = ticker_var.get()
    if not ticker:
        messagebox.showerror("Input Error", "No ticker to add. Find a ticker first.")
        return
    portfolio.append(ticker)
    portfolio_listbox.insert(tk.END, ticker)
    messagebox.showinfo("Success", f"{ticker} added to your portfolio.")

def show_portfolio():
    portfolio_string = "\n".join(portfolio)
    if portfolio:
        messagebox.showinfo("Portfolio", f"Your portfolio:\n{portfolio_string}")
    else:
        messagebox.showinfo("Portfolio", "Your portfolio is empty.")

def history_of_spec_stock(name_of_stock: str, time_period: str):
    ticker = yf.Ticker(name_of_stock)
    data = ticker.history(period=time_period)
    return data

# GUI Setup
root = tk.Tk()
root.configure(bg="lightblue")
root.title("Stock Tracker")

# Variables
portfolio = []
ticker_var = tk.StringVar()

# GUI Components
tk.Label(root, text="Enter Stock Name:", bg="lightblue", fg="white").grid(row=0, column=0, padx=10, pady=10)
stock_name_entry = tk.Entry(root, width=30)
stock_name_entry.grid(row=0, column=1, padx=10, pady=10)

find_ticker_button = tk.Button(root, text="Find Ticker", command=fetch_stock_data)
find_ticker_button.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Last Found Ticker:", bg="lightblue", fg="white").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=ticker_var, state="readonly", width=30).grid(row=1, column=1, padx=10, pady=10)

add_button = tk.Button(root, text="Add to Portfolio", command=add_to_portfolio)
add_button.grid(row=2, column=0, padx=10, pady=10)

show_portfolio_button = tk.Button(root, text="Show Portfolio", command=show_portfolio)
show_portfolio_button.grid(row=2, column=1, padx=10, pady=10)

show_data_of_stock_button = tk.Button(root, text="Show data", command=())
show_data_of_stock_button.grid(row=2, column=2, padx=10, pady=10 )

tk.Label(root, text="Portfolio:", bg="lightblue", fg="white").grid(row=3, column=0, padx=10, pady=10)
portfolio_listbox = tk.Listbox(root, height=10, width=50)
portfolio_listbox.grid(row=3, column=1, padx=10, pady=10)

# Run the GUI
root.mainloop()
