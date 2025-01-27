import tkinter as tk
from tkinter import messagebox, simpledialog
import yfinance as yf
import requests

API_key = "156DW7OTQGTLJESV"


class PortfolioManager:
    def __init__(self):
        self.portfolio = []

    def add_stock(self, ticker: str):
        company_name = yf.Ticker(ticker).info.get("longName", "Unknown Company")
        self.portfolio.append({"ticker": ticker, "name": company_name})
        return company_name

    def remove_stock(self, index: int):
        return self.portfolio.pop(index)

    def get_portfolio_string(self):
        return "\n".join([f"{item['name']}: {item['ticker']}" for item in self.portfolio])

    def get_portfolio(self):
        return self.portfolio