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
            {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
            {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
            {'label': 'Facebook (FB)', 'value': 'FB'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
        ],
        value='AAPL'
    ),

    dcc.Graph(id='stock-graph'),

    # Interval component to update every 10 seconds
    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(
    Output('stock-graph', 'figure'),
    Input('stock-symbol', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_graph(selected_symbol, n):
    # Fetch stock data
    df = yf.download(selected_symbol, period='1d', interval='1m')

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    # Get the latest closing price for annotation
    latest_price = df['Close'].iloc[-1]

    # Add annotation for the latest price
    fig.add_annotation(
        x=df.index[-1],  # Position at the last date
        y=latest_price,
        text=f'Current Price: ${latest_price:.2f}',
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        bgcolor='white',
        bordercolor='black',
        borderwidth=1,
        borderpad=4,
        font=dict(size=12)
    )

    # Update layout
    fig.update_layout(title=f'{selected_symbol} Stock Price',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      height=600,
                      width=1200)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
