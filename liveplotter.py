from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import pandas_ta as ta
import requests

app = Dash(external_stylesheets=[dbc.themes.CYBORG])


def create_dropdown(options, id_value):
    return html.Div(
        [
            html.H4(" ".join(id_value.replace("-", " ").split(" ")[:-1]),
                    style={"padding": "0px 30px 0px 30px", "text-size": "15px"}),
            dcc.Dropdown(options, id=id_value, value=options[0])
        ], style={"padding": "0px 30px 0px 30px"}
    )


app.layout = html.Div([
    html.Div([
        create_dropdown(["btcusd", "ethusd", "xrpusd"], "coin-select"),
        create_dropdown(["60", "3600", "86400"], "timeframe-select"),
        create_dropdown(["20", "50", "100"], "num-bars-select"),
    ], style={"display": "flex", "margin": "auto", "width": "800px",
              "justify-content": "space-around"}),

    dcc.RangeSlider(0, 20, 1, value=[0, 20], id="range-slider",
                    marks={i: str(i) for i in range(21)}),

    dcc.Graph(id="candles"),
    dcc.Graph(id="indicator"),

    dcc.Interval(id="interval", interval=2000),
])


@app.callback(
    Output("candles", "figure"),
    Output("indicator", "figure"),
    Input("interval", "n_intervals"),
    Input("coin-select", "value"),
    Input("timeframe-select", "value"),
    Input("num-bars-select", "value"),
    Input("range-slider", "value"),
)
def update_figure(n_intervals, coin_pair, timeframe, num_bars, range_values):
    url = f"https://www.bitstamp.net/api/v2/ohlc/{coin_pair}/"

    params = {
        "step": timeframe,
        "limit": int(num_bars) + 14,
    }

    response = requests.get(url, params=params)
    data = response.json()["data"]["ohlc"]

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Calculate RSI and drop NaN values if necessary
    df['rsi'] = ta.rsi(df['close'].astype(float))

    # Filter based on range slider values
    df = df.iloc[range_values[0]:range_values[1]]

    # Create candlestick figure
    candles = go.Figure(data=[
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )
    ])

    candles.update_layout(xaxis_rangeslider_visible=False,
                          height=400, template="plotly_dark")

    # Create RSI indicator figure
    indicator = px.line(df, x='timestamp', y='rsi', height=300)

    return candles, indicator


if __name__ == '__main__':
    app.run_server(debug=True)
