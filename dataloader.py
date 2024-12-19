import yfinance as yf
dat = yf.Ticker("MSFT")

def get_ticker_history(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history()
    print(data)