import pandas as pd
import yfinance as yf
import mplfinance as mpf

# Fetch data
symbol = "AAPL"
start_date = "2022-01-01"
end_date = "2022-12-31"
stock_data = yf.download(symbol, start=start_date, end=end_date)

# Ensure correct index format
stock_data.index = pd.to_datetime(stock_data.index)

# Ensure correct data types
for col in ['Open', 'High', 'Low', 'Close']:
    stock_data[col] = stock_data[col].astype(float)

# Check for NaN values and drop them if necessary
stock_data.dropna(inplace=True)

# Plotting with mplfinance
mpf.plot(stock_data, type='candle', style='yahoo', title=f'{symbol} Stock Price')
