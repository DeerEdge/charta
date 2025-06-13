import streamlit as st
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from bokeh.embed import file_html
from bokeh.resources import CDN
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from cerebras.cloud.sdk import Cerebras


st.set_page_config(page_title="transfer",)
st.title("Options View")
st.markdown("View Option Prices")