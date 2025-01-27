import tkinter as tk
from tkinter import messagebox, simpledialog
import yfinance as yf
import requests

API_key = "156DW7OTQGTLJESV"


class StockAPI:
    @staticmethod
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

    @staticmethod
    def stock_price_per_share(ticker_symbol: str) -> float:
        stock = yf.Ticker(ticker_symbol)
        try:
            current_price = stock.info['currentPrice']
            return round(current_price, 2)
        except KeyError:
            print(f"'regularMarketPrice' not found in data for {ticker_symbol}")
            return None

    @staticmethod
    def history_of_spec_stock(ticker_symbol: str, time_period: str):
        ticker = yf.Ticker(ticker_symbol)
        return ticker.history(period=time_period)