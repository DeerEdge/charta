import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os


from keys import *
from supabase import create_client, Client

# AlphaVantage Usage limited to 25 hits a day, maybe cache once every 30 mins???

url: str = os.environ.get(SUPABASE_URL)
key: str = os.environ.get(SUPABASE_KEY)
supabase: Client = create_client(url, key)

st.set_page_config(page_title="Options View")
st.title("Options Data Viewer")

ticker = st.selectbox("Choose a ticker", ["AAPL", "SPY", "TSLA", "GOOG", "NVDA"])
url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={ticker}&apikey={ALPHAVANTAGE_KEY}'
r = requests.get(url)
data = r.json()

print(data)

st.subheader("Recent Options Data")
st.write(data)

df = pd.DataFrame(data['data'])
df = df[df["type"] == "call"]
df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
df["mark"] = pd.to_numeric(df["mark"], errors="coerce")
df = df.dropna(subset=["strike", "mark"])

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

