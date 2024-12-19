import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import html, dcc, Output, Input, Dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dataloader import *
from dash import dash_table
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = dbc.Container([
    dcc.Graph(id="graph")
])

tab_style = {
    'backgroundColor': '#1f2539',
    'color': '#ffffff',
    'paddingLeft': '40px',  # Added left padding
    'paddingRight': '40px',  # Added right padding
    'paddingTop': '10px',
    'paddingBottom': '10px',
    'border': 'none',
    'fontSize': '20px'
}

selected_style = {
    'backgroundColor': '#1f2539',
    'color': '#7296f7',
    'paddingLeft': '40px',  # Added left padding
    'paddingRight': '40px',  # Added right padding
    'paddingTop': '10px',
    'paddingBottom': '10px',
    'border': 'none',
    'fontSize': '20px'
}

app.layout = html.Div([
    # Header container
    html.Div(style={'backgroundColor': '#1f2539', 'color': '#1f2539', 'padding': '20px'}, children=[
        html.Div(style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'}, children=[
            html.H1("Charta", style={'margin': '0', 'color': '#ffffff', 'paddingLeft': '15px'}),
            dcc.Tabs(id='tabs', value='home',
                     style={'backgroundColor': '#1f2539', 'color': '#7296f7', 'marginLeft': 'auto'}, children=[
                    dcc.Tab(label='Home', value='home', style=tab_style, selected_style=selected_style),
                    dcc.Tab(label='Learn', value='learn', style=tab_style, selected_style=selected_style),
                    dcc.Tab(label='Trade', value='trade', style=tab_style, selected_style=selected_style),
                ])
        ])
    ]),

    # Content container
    html.Div(id='tabs-content', style={'margin-top': '20px', 'padding': '20px'})
])


# Define the callback to update content based on selected tab
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'home':
        df = get_ticker_history("AAPL", "1y") # Period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

        return html.Div([
            html.H3('Trade Tab'),
            html.P('This section is dedicated to trading features and tools.'),

            html.Div([
                dcc.Input(id="symbol_field", type="text", placeholder="Enter Symbol"),
                html.Div(id="ticker_label", style={'display': 'inline-block', 'margin-left': '10px'})
            ], style={'margin-bottom': '20px'}),

            html.Div(id="num_rows_label"),
            html.Div(id="table_container")  # DataTable
        ])

    elif tab == 'learn':
        return html.Div([
            html.H3('Learn Tab'),
            html.P('Here you can find resources and tutorials to help you learn more.')
        ])
    elif tab == 'trade':
        return html.Div([
            html.H3('Trade Tab'),
            html.P('This section is dedicated to trading features and tools.'),
            html.P(get_ticker_history("GOOG"))
        ])

@app.callback(
    Output("ticker_label", "children"),
    Input("symbol_field", "value")
)
def update_ticker_label(value):
    if value and value.strip():
        try:
            yf.Ticker(value.strip()).info  # This will raise an exception if the ticker is invalid
            return f"Valid ticker: {value.upper()}"
        except:
            return "Invalid ticker"
    return ""

@app.callback(
    Output("table_container", "children"),
    Input("symbol_field", "value")
)
def update_price_table(value):
    if value and value.strip():
        try:
            df = get_ticker_history(value.strip(), "1y")
            print(df.shape)
            if df.shape[0] == 0:
                raise ValueError
            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={
                    'backgroundColor': '#1f2539',
                    'color': 'white',
                    'textAlign': 'left'
                },
                style_header={
                    'backgroundColor': '#35394c',
                    'fontWeight': 'bold'
                }
            )
            return table
        except:
            return html.Div("No data available for this ticker")
    return None

@app.callback(
    Output("num_rows_label", "children"),
    Input("symbol_field", "value")
)
def update_num_rows_label(value):
    if value and value.strip():
        try:
            df = get_ticker_history(value.strip(), "1y")
            if df.shape[0] == 0:
                raise ValueError
            return html.Div("Number of Rows:" + str(df.shape[0]))
        except:
            pass
    return None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
