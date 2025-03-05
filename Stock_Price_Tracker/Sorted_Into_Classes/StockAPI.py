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
            history = stock.history(period="1d")  # Fetch only today's price
            if not history.empty:
                return round(history["Close"].iloc[-1], 2)  # Get last closing price
            else:
                return None
        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")
            return None

    @staticmethod
    def history_of_spec_stock(ticker_symbol: str, time_period: str):
        ticker = yf.Ticker(ticker_symbol)
        return ticker.history(period=time_period)