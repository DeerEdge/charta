import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

from tasks.db_funcs import *
from tasks.ticker_data_funcs import *
from globs import *

# AlphaVantage Usage limited to 25 hits a day, maybe cache once every 30 mins???
# Since there are 3000+ tickers, we pull historical data and store in db and refer to db data intraday
# Have to check across NYSE tickers

st.set_page_config(page_title="Options View")
st.title("Options Data Viewer")

all_nyse_tickers = get_tickers(nyse_tickers_path)
all_nasdaq_tickers = get_tickers(nasdaq_tickers_path)
all_tickers = all_nyse_tickers.union(all_nasdaq_tickers)

ticker = st.text_input("Enter a ticker symbol", value="AAPL").upper()

if st.button("Pull data"):
    print(get_ticker_data(supabase, ticker, historical_data_table))

if ticker in all_tickers:
    data = get_ticker_data(supabase, ticker, historical_data_table)

    st.subheader("Recent Options Data")
    st.write(data)

    df = pd.DataFrame(data['data'])
    df = df[df["type"] == "call"]
    df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
    df["mark"] = pd.to_numeric(df["mark"], errors="coerce")
    df = df.dropna(subset=["strike", "mark"])

    with st.expander("Strike v. Price"):
        fig, ax = plt.subplots()
        ax.plot(df["strike"], df["mark"], marker='o')
        ax.set_xlabel("Strike")
        ax.set_ylabel("Mark Price")
        ax.set_title(f"{ticker} Call Options: Strike vs Price")
        st.pyplot(fig)

    with st.expander("Show Greeks Charts"):
        # Convert Greek columns
        greeks = ["delta", "gamma", "theta", "vega", "rho"]
        for greek in greeks:
            df[greek] = pd.to_numeric(df[greek], errors="coerce")

        # Plot each Greek vs Strike
        for greek in greeks:
            fig, ax = plt.subplots()
            ax.plot(df["strike"], df[greek], marker='o')
            ax.set_xlabel("Strike")
            ax.set_ylabel(greek.title())
            ax.set_title(f"{ticker} Call Options: Strike vs {greek.title()}")
            ax.grid(True)
            st.pyplot(fig)


