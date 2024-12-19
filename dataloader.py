import yfinance as yf

def get_ticker_history(symbol, period):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period)
    print(type(data))
    print(data)
    return data