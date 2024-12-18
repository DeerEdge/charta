import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.graph_objs as go
import datetime

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = html.Div([
    html.H1("Live Stock Price Dashboard", style={'text-align': 'center'}),

    # Dropdown for selecting stock symbol
    dcc.Dropdown(
        id='stock-symbol',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
            {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
        ],
        value='AAPL',  # Default value
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),

    # Graph for displaying stock prices
    dcc.Graph(id='live-stock-graph'),

    # Interval component for updating the graph every minute
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # Update every 60 seconds
        n_intervals=0
    )
])


@app.callback(
    Output('live-stock-graph', 'figure'),
    Input('stock-symbol', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_graph(selected_symbol, n):
    # Get current date and time for fetching data
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=1)  # Fetch last day's data

    # Fetch stock data using yfinance
    df = yf.download(selected_symbol, start=start_date, end=end_date, interval='1m')

    if df.empty:
        return go.Figure()  # Return an empty figure if no data is available

    # Create a candlestick chart using Plotly
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    # Update layout of the figure
    fig.update_layout(
        title=f'Live {selected_symbol} Stock Price',
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
