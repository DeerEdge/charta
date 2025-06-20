import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os


def insert_data(supabase, id, json_data={}):
    (
        supabase.table("ALPHAVANTAGE_OPTIONS_HISTORICAL_DATA")
        .insert({"id": id, "data": json_data})
        .execute()
    )
    print("Inserted into table")

