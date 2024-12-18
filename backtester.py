import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Stock Price Candlestick Chart"),

    dcc.Dropdown(
        id='stock-symbol',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
        ],
        value='AAPL'
    ),

    dcc.Graph(id='stock-graph')
])


@app.callback(
    Output('stock-graph', 'figure'),
    Input('stock-symbol', 'value')
)
def update_graph(selected_symbol):
    # Fetch stock data
    df = yf.download(selected_symbol, period='1mo')

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    # Update layout
    fig.update_layout(title=f'{selected_symbol} Stock Price')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)