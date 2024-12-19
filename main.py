# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import html, dcc, Output, Input, Dash
import dash_bootstrap_components as dbc

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
        return html.Div([
            html.H3('Welcome to the Home Tab'),
            html.P('This is where you can find an overview of our application.')
        ])
    elif tab == 'learn':
        return html.Div([
            html.H3('Learn Tab'),
            html.P('Here you can find resources and tutorials to help you learn more.')
        ])
    elif tab == 'trade':
        return html.Div([
            html.H3('Trade Tab'),
            html.P('This section is dedicated to trading features and tools.')
        ])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
