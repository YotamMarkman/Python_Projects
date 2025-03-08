# import requests

# API_key = "156DW7OTQGTLJESV"
# url = "https://www.alphavantage.co/query"
# params = {
#     "function": "SYMBOL_SEARCH",
#     "keywords": "Apple",
#     "apikey": API_key,
# }
# response = requests.get(url, params=params)
# print(response.json())  # Check if response contains "bestMatches"

import yfinance as yf
import time
import random
from datetime import datetime, timedelta

class YFinanceTest:
    def __init__(self):
        self.success = False
    
    def simple_test(self, ticker="AAPL"):
        """A simple test to check if yfinance is working"""
        print(f"Testing yfinance with ticker: {ticker}")
        
        # Set dates to fetch a small amount of data (just 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        try:
            # Add a small random delay before request
            time.sleep(random.uniform(1.0, 3.0))
            
            print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            stock_data = yf.download(
                ticker,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                progress=False
            )
            
            if stock_data.empty:
                print("Error: Yahoo Finance returned empty data.")
                return False
            
            # Print the first few rows to verify data
            print("\nData retrieved successfully!")
            print(f"Shape of data: {stock_data.shape}")
            print("\nFirst 3 rows:")
            print(stock_data.head(3))
            
            # Print the last price
            print(f"\nMost recent closing price: ${stock_data['Close'].iloc[-1]:.2f}")
            
            self.success = True
            return True
            
        except Exception as e:
            print(f"Error: {type(e).__name__}: {str(e)}")
            return False

if __name__ == "__main__":
    test = YFinanceTest()
    
    # Try with a few different tickers
    tickers = ["AAPL", "MSFT", "GOOG"]
    
    for ticker in tickers:
        print("\n" + "="*50)
        result = test.simple_test(ticker)
        if result:
            print(f"✅ Test passed for {ticker}")
            break
        else:
            print(f"❌ Test failed for {ticker}")
            # Wait longer between requests if we're going to try another ticker
            wait_time = random.uniform(5.0, 10.0)
            print(f"Waiting {wait_time:.2f} seconds before trying next ticker...")
            time.sleep(wait_time)
    
    if not test.success:
        print("\n❌ All tests failed. There may be an issue with your yfinance installation or network connection.")
        print("Possible solutions:")
        print("1. Check your internet connection")
        print("2. Try reinstalling yfinance: pip install --upgrade yfinance")
        print("3. Yahoo Finance may be temporarily blocking requests from your IP")
