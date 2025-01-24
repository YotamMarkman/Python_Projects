import yfinance as yf



def history_of_spec_stock(name_of_stock : str, time_period : str):
    ticker = yf.Ticker(name_of_stock)
    data = ticker.history(period=time_period)
    return data


print(history_of_spec_stock("AAPL", "1mo"))