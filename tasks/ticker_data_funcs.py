import io
import os

"""
    Gets all tickers on an exchange
    Input: file path
    Output: set() of tickets
"""
def get_tickers(filepath):
    all_tickers = set()
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                all_tickers.add(line.strip().upper())
    return all_tickers
