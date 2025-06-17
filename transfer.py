import streamlit as st
import requests

from key import API_KEY

st.set_page_config(page_title="Options View")
st.title("Options Data Viewer")

ticker = st.selectbox("Choose a ticker", ["AAPL", "SPY", "TSLA", "GOOG", "NVDA"])
url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey={API_KEY}'
r = requests.get(url)
data = r.json()

print(data)

try:
    st.subheader("Recent Options Data")
    st.write(data)
except Exception as e:
    st.error(f"Failed to fetch contracts: {e}")
