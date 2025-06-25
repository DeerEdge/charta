import io
import os

from tasks.db_funcs import *
from globs import *
from keys import *

"""
    Gets all tickers on an exchange
    Input: string filepath
    Output: set() all_tickers
"""
def get_tickers(filepath):
    all_tickers = set()
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                all_tickers.add(line.strip().upper())
    return all_tickers

"""
    Gets data for a given ticker, pulls cached data from db or populates if absent
    Inputs: supabase supabase
            string ticker
            string table
    Output: dict() data
"""
def get_ticker_data(supabase, ticker, table):
    data = fetch_data(supabase, ticker, table)
    if data == None:
        json_data = data_pull_alphavantage(ticker)
        fill_ticker_data(supabase, ticker, table, json_data)
    else:
        return data

def fill_ticker_data(supabase, ticker, table, json_data):
    try:
        insert_data(supabase, ticker, table, json_data)
    except Exception as e:
        st.error(f"Failed to fill data: {e}")

def data_pull_alphavantage(ticker, ALPHAVANTAGE_KEY=ALPHAVANTAGE_KEY):
    url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={ticker}&apikey={ALPHAVANTAGE_KEY}'
    r = requests.get(url)
    data = r.json()
