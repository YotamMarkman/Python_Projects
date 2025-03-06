import numpy as np
import yfinance as yf
from StockAPI import StockAPI
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ExpectationAndDeviationCalc:
    def __init__(self):
        self.expectation = None
        self.deviation = None
        
        
    def history_of_prices(self, prices:list):
        ticker = StockAPI.return_ticker
        start_date = datetime.now()
        end_date = start_date - relativedelta(years=1)
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        prices = stock_data["Close"].tolist()
        
    def calc_expectation(prices:list) -> float:
        return np.mean(prices)
    
        
    def calculate_deviation(self, prices:list):
        self.deviation = np.std(prices, ddof=0)