import tkinter as tk
from tkinter import messagebox, simpledialog
# import yfinance as yf
import requests
from StockAPI import StockAPI

API_key = "156DW7OTQGTLJESV"


class PortfolioManager:
    def __init__(self):
        self.portfolio = []
        self.stock_cache = {}

    def add_stock(self, ticker: str):
        if ticker in self.stock_cache:
            company_name = self.stock_cache[ticker]
        else:
            company_name = StockAPI.return_ticker(ticker)
            self.stock_cache[ticker] = company_name  # Cache the result

        self.portfolio.append({"ticker": ticker, "name": company_name})
        return company_name

    def remove_stock(self, index: int):
        return self.portfolio.pop(index)

    def get_portfolio_string(self):
        return "\n".join([f"{item['name']}: {item['ticker']}" for item in self.portfolio])

    def get_portfolio(self):
        return self.portfolio