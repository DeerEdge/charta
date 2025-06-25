import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os


def insert_data(supabase, ticker, table, json_data):
    (
        supabase.table(table)
        .insert({"ticker": ticker, "data": json_data})
        .execute()
    )

    print("Inserted into table at ticker: ", ticker)

def fetch_data(supabase, ticker, table):
    response = (
        supabase.table(table)
        .select('*')
        .eq("ticker", ticker)
        .limit(1)
        .execute()
    )

    print(response)
    return response.data

