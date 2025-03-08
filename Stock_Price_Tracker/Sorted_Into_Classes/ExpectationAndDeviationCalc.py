import numpy as np
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import random
import requests  # Needed for handling HTTP errors

class ExpectationAndDeviationCalc:
    def __init__(self):
        self.expectation = None
        self.deviation = None
        
    def history_of_prices(self, ticker) -> list:
        """Fetch stock prices from the last year, handling API rate limits."""
        end_date = datetime.now()
        start_date = end_date - relativedelta(years=1)
        
        max_attempts = 5  # Number of retry attempts
        for attempt in range(max_attempts):
            try:
                # Add a longer initial delay
                if attempt > 0:
                    backoff_time = 5 + (2 ** attempt) + (random.random() * 2)
                    print(f"Waiting {backoff_time:.2f} seconds before retry {attempt}...")
                    time.sleep(backoff_time)
                
                stock_data = yf.download(
                    ticker, 
                    start=start_date.strftime("%Y-%m-%d"), 
                    end=end_date.strftime("%Y-%m-%d"),
                    progress=False  # Disable unnecessary output
                )
                
                if stock_data.empty:  # If empty, retry
                    raise ValueError("Yahoo Finance returned empty data (possible rate limit).")

                return stock_data["Close"].dropna().values.tolist()
            
            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error: {e}")
            except ValueError as e:
                print(f"{e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")

        print(f"Failed to retrieve data for {ticker} after {max_attempts} attempts.")
        return None
        
    def calc_expectation(self, prices):
        """Calculate the mean of the given prices, handling empty cases."""
        if not prices:  # Check if prices is empty or None
            print("No data available for expectation calculation.")
            return None
        expectation = np.mean(prices)
        return round(expectation,2)

    def calculate_deviation(self, prices):
        """Calculate the standard deviation, handling empty cases."""
        if not prices:  # Check if prices is empty or None
            print("No data available for deviation calculation.")
            return None
        self.deviation = round(np.std(prices, ddof=0),2)
        return self.deviation

# Example Usage
if __name__ == "__main__":
    data = ExpectationAndDeviationCalc()
    ticker = "AAPL"

    prices = data.history_of_prices(ticker)
    
    if prices is None:
        print(f"Could not retrieve prices for {ticker}.")
    else:
        expectation = data.calc_expectation(prices)
        deviation = data.calculate_deviation(prices)
        print(f"Expectation: {expectation}, Deviation: {deviation}")
