import tkinter as tk
from tkinter import messagebox, simpledialog
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
    company_name = yf.Ticker(ticker).info.get("longName", "Unknown Company")
    portfolio.append({"ticker": ticker, "name": company_name})
    portfolio_listbox.insert(tk.END, f"{company_name}: {ticker}")
    messagebox.showinfo("Success", f"{ticker} added to your portfolio.")

def show_portfolio():
    if portfolio:
        portfolio_string = "\n".join([f"{item['name']}: {item['ticker']}" for item in portfolio])
        messagebox.showinfo("Portfolio", f"Your portfolio:\n{portfolio_string}")
    else:
        messagebox.showinfo("Portfolio", "Your portfolio is empty.")

def history_of_spec_stock(name_of_stock: str, time_period: str):
    ticker = yf.Ticker(name_of_stock)
    data = ticker.history(period=time_period)
    return data

def show_data():
    selected = portfolio_listbox.curselection()
    if not selected:
        messagebox.showerror("Selection Error", "Please select a ticker from the portfolio.")
        
    selected_index = selected[0]
    ticker = portfolio[selected_index]["ticker"]
    time_frame = simpledialog.askstring("Time Frame", "Enter the time frame (e.g., 1d, 1mo, 1y):")
    if not time_frame:
        messagebox.showerror("Input Error", "Please provide a valid time frame.")
        
    popup = tk.Toplevel(root)
    popup.title("Data Of Stock")
    popup.geometry("400x300")
    text_frame = tk.Frame(popup)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15, width=50)
    scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    long_message = (history_of_spec_stock(ticker, time_frame))
    text_widget.insert(tk.END, long_message)
    text_widget.config(state=tk.DISABLED)
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)
    
def remove():
    selected = portfolio_listbox.curselection()
    if not selected:
        messagebox.showerror("Selection Error", "Please select a ticker from the portfolio.")
        return

    selected_index = selected[0]
    portfolio_listbox.delete(selected_index) 
    portfolio.pop(selected_index)  
    messagebox.showinfo("Success", "Selected stock removed from portfolio.")

def submit_amount():
    global investment_amount
    amount = amount_entry.get()  
    if not amount:
        messagebox.showerror("Input Error", "Please enter an amount.")
        return
    try:
        # Try to convert the input to a float
        investment_amount = float(amount)
        messagebox.showinfo("Success", f"Amount of ${investment_amount:.2f} saved!")
        amount_label.config(text=f"${investment_amount}")  # Update the Amount label
        root1.destroy()  # Close the investment amount window
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric amount.")
    
        
# GUI Setup
root1 = tk.Tk()
root1.config(bg="lightblue")
root1.title("Amount To Invest")
tk.Label(root1, text="How much can you invest($):", bg="lightblue", fg="white").grid(row=0, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root1, width=30)
amount_entry.grid(row=0, column=1, padx=10, pady=10)
submit_amount_button = tk.Button(root1, text="Sumbit", command=submit_amount)
submit_amount_button.grid(row=0, column=3, padx=10, pady=10)

root = tk.Tk()
root.configure(bg="lightblue")
root.title("Stock Tracker")

# Variables
portfolio = []
ticker_var = tk.StringVar()
investment_amount = None

# Labels and inputs for Stock Tracker
tk.Label(root, text="Amount:", bg="lightblue", fg="white").grid(row=0, column=0, padx=10, pady=10)
amount_label = tk.Label(root, text="$0.00", bg="lightblue", fg="white") 
amount_label.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter Stock Name:", bg="lightblue", fg="white").grid(row=1, column=0, padx=10, pady=10)
stock_name_entry = tk.Entry(root, width=30)
stock_name_entry.grid(row=1, column=1, padx=10, pady=10)

find_ticker_button = tk.Button(root, text="Find Ticker", command=fetch_stock_data)
find_ticker_button.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Last Found Ticker:", bg="lightblue", fg="white").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=ticker_var, state="readonly", width=30).grid(row=2, column=1, padx=10, pady=10)

add_button = tk.Button(root, text="Add to Portfolio", command=add_to_portfolio)
add_button.grid(row=3, column=0, padx=10, pady=10)

show_portfolio_button = tk.Button(root, text="Show Portfolio", command=show_portfolio)
show_portfolio_button.grid(row=3, column=1, padx=10, pady=10)

show_data_of_stock_button = tk.Button(root, text="Show Data", command=show_data)
show_data_of_stock_button.grid(row=3, column=2, padx=10, pady=10)

reset_button = tk.Button(root, text="Remove Stock", command=remove)
reset_button.grid(row=4, column=2, padx=10, pady=10)

tk.Label(root, text="Portfolio:", bg="lightblue", fg="white").grid(row=4, column=0, padx=10, pady=10)
portfolio_listbox = tk.Listbox(root, height=10, width=50)
portfolio_listbox.grid(row=4, column=1, padx=10, pady=10)

# Run the GUI
root.mainloop()
