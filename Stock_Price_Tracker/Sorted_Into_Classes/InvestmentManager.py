import tkinter as tk
from tkinter import messagebox, simpledialog
import yfinance as yf
import requests

API_key = "156DW7OTQGTLJESV"

class InvestmentManager:
    def __init__(self):
        self.amount = None
        self.update_callback = None
        
    def set_update_callback(self, callback):
        self.update_callback = callback

    def set_investment_amount(self, amount: float):
        self.amount = amount
        if self.update_callback:
            self.update_callback()

    def get_investment_amount(self):
        return self.amount
    
    def ask_for_investment_amount(self, root):
        
        investment_popup = tk.Toplevel(root)
        investment_popup.title("Amount To Invest")
        investment_popup.config(bg="lightblue")

        # Input and label
        tk.Label(investment_popup, text="How much can you invest($):", bg="lightblue", fg="white").grid(row=0, column=0, padx=10, pady=10)
        amount_entry = tk.Entry(investment_popup, width=30)
        amount_entry.grid(row=0, column=1, padx=10, pady=10)

        def submit_amount():
            try:
                amount = float(amount_entry.get())
                self.set_investment_amount(amount)
                messagebox.showinfo("Success", f"Amount of ${amount:.2f} saved!")
                investment_popup.destroy()  # Close the popup
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numeric amount.")

        # Submit button
        submit_button = tk.Button(investment_popup, text="Submit", command=submit_amount)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Center the popup
        investment_popup.geometry("400x100")
        investment_popup.transient(root)
        investment_popup.grab_set()
        investment_popup.focus_set()
