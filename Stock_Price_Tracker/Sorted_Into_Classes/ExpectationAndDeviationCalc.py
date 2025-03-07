import numpy as np
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
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
                stock_data = yf.download(
                    ticker, 
                    start=start_date.strftime("%Y-%m-%d"), 
                    end=end_date.strftime("%Y-%m-%d"),
                    progress=False  # Disable unnecessary output
                )
                
                if stock_data.empty:  # If empty, retry
                    raise ValueError("Yahoo Finance returned empty data (possible rate limit).")

                return stock_data["Close"].dropna().values.tolist()
            
            except requests.exceptions.HTTPError as e:  # Handles API errors
                print(f"HTTP Error: {e}. Retrying in {2 ** attempt} seconds...")
            except ValueError as e:  # Handles empty data (possible rate limit)
                print(f"{e} Retrying in {2 ** attempt} seconds...")
            except Exception as e:  # General error handling
                print(f"Unexpected Error: {e}. Retrying in {2 ** attempt} seconds...")

            time.sleep(2 ** attempt)  # Exponential backoff

        print(f"Failed to retrieve data for {ticker} after {max_attempts} attempts.")
        return None  # Return None instead of an empty list

    def calc_expectation(self, prices):
        """Calculate the mean of the given prices, handling empty cases."""
        if not prices:  # Check if prices is empty or None
            print("No data available for expectation calculation.")
            return None
        return np.mean(prices)

    def calculate_deviation(self, prices):
        """Calculate the standard deviation, handling empty cases."""
        if not prices:  # Check if prices is empty or None
            print("No data available for deviation calculation.")
            return None
        self.deviation = np.std(prices, ddof=0)
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
