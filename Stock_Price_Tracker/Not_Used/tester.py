import tkinter as tk
from tkinter import messagebox, simpledialog
import yfinance as yf
import requests

API_key = "156DW7OTQGTLJESV"


def stock_price_per_share(ticker_symbol: str) -> float:
        stock = yf.Ticker(ticker_symbol)
        try:
            current_price = stock.info['currentPrice']
            return round(current_price, 2)
        except KeyError:
            return None
        
def stock_price_per_share1(ticker_symbol: str) -> float:
    stock = yf.Ticker(ticker_symbol)
    try:
        current_price = stock.info['currentPrice']
        return round(current_price, 2)
    except KeyError:
        print(f"'regularMarketPrice' not found in data for {ticker_symbol}")
        return None
        
print(stock_price_per_share1("AMZN"))