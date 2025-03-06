import tkinter as tk
from tkinter import messagebox, simpledialog
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
            return data["bestMatches"][0]["1. symbol"]  # Extract the first matching ticker
        else:
            return "No ticker found"

    @staticmethod
    def stock_price_per_share(ticker_symbol: str) -> float:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker_symbol,
            "apikey": API_key,
        }
        response = requests.get(url, params=params)
        data = response.json()

        try:
            return float(data["Global Quote"]["05. price"])
        except (KeyError, TypeError):
            print(f"Error fetching data for {ticker_symbol}")
            return None

    @staticmethod
    def history_of_spec_stock(ticker_symbol: str, time_period: str):
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": ticker_symbol,
            "apikey": API_key,
            "outputsize": "compact",  # Use "full" for complete history
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        else:
            return None