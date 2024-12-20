import yfinance as yf

def get_ticker_history(symbol, period):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period)
    print("Data from get_ticker_history:")
    print(data)
    print(data.columns)
    return data
