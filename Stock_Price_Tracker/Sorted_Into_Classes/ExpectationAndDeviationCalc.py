import numpy as np
import yfinance as yf
from StockAPI import StockAPI
from datetime import datetime
from dateutil.relativedelta import relativedelta


#Class which recieves a ticker and uses the yfinance to produce a list of prices 
# of a specific stock to return its expectation and standard deviation
class ExpectationAndDeviationCalc:
    def __init__(self):
        self.expectation = None
        self.deviation = None
        
        
    def history_of_prices(self, ticker) -> list:
        start_date = start_date - relativedelta(years=1) 
        end_date = datetime.now()
        stock_data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
        if "Close" in stock_data.columns:
            prices = stock_data["Close"].values.tolist() 
            return prices
        else:
            print(f"No 'Close' column found for {ticker}")
            return []
        
        
    def calc_expectation(self, prices:list) -> int:
        return np.mean(prices)
    
        
    def calculate_deviation(self, prices:list) -> int:
        self.deviation = np.std(prices, ddof=0)