import yfinance as yf
import requests

API_key = "156DW7OTQGTLJESV"

def history_of_spec_stock(name_of_stock: str, time_period: str):
    ticker = yf.Ticker(name_of_stock)
    data = ticker.history(period=time_period)
    return data

def return_ticker(full_name_of_stock: str) -> str:
    api_key = API_key
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": full_name_of_stock,
        "apikey": api_key,
    }
    # Make the API request
    response = requests.get(url, params=params)
    data = response.json()
    # Check if the response contains matches
    if "bestMatches" in data and data["bestMatches"]:
        ticker = data["bestMatches"][0]["1. symbol"]
        return ticker
    else:
        return f"No ticker found for {full_name_of_stock}"
    
def add_to_portfolio(portfolio : list[str], ticker:str):
    return portfolio.append(ticker)

def ticker_to_nameOfStock(ticker_symbol: str) -> str:
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    return info.get("longName", "Company name not available")
    
def show_portfolio(portfolio : list[str]):
    if not portfolio:
        print("Your portfolio is empty, please add stocks.")
    else:
        for ticker in portfolio:
            print(f"{ticker_to_nameOfStock(ticker)} : {ticker}")

if __name__ == "__main__":
    userInput = ""
    ticker = None
    my_portfolio = []
    while userInput.strip().lower() != "exit":
        userInput = input(
            "Hi! Please choose an option:\n"
            "1. Find the ticker of a specific stock\n"
            "2. Get the historical prices of a ticker\n"
            "3. Add specific ticker to portfolio\n"
            "4. Show me my portfolio\n"
            "Type 'exit' to quit.\n"
        ).strip().lower()
        
        if userInput == "1":
            stock_name = input("Enter the name of the stock:\n").strip()
            ticker = return_ticker(stock_name)
            print(f"The ticker for {stock_name} is: {ticker}")
        
        elif userInput == "2":
            if ticker:
                decision = input("Would you like to use the last retrieved ticker? (y/n):\n").strip().lower()
                if decision == "y":
                    time_frame = input("Enter the time frame (e.g., 1d, 1mo, 1y):\n").strip()
                    data = history_of_spec_stock(ticker, time_frame)
                    print(data)
                else:
                    new_ticker = input("Enter the ticker symbol:\n").strip()
                    time_frame = input("Enter the time frame (e.g., 1d, 1mo, 1y):\n").strip()
                    data = history_of_spec_stock(new_ticker, time_frame)
                    print(data)
            else:
                print("No ticker has been retrieved yet. Please choose option 1 first.")
                
        elif userInput == "3":
            if ticker is None:
                print("No ticker has been retrieved yet. Please choose option 1 first.")
            else:
                add_to_portfolio(my_portfolio, ticker)
                print(f"Added {ticker} to your portfolio\n")

        elif userInput == "4":
            show_portfolio(my_portfolio)
            
        elif userInput == "exit":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
