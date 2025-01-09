import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf


def get_stock_data(symbol, period):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df
    except:
        return pd.DataFrame()


def update_chart(symbol, period):
    df = get_stock_data(symbol, period)
    if df.empty:
        return "No data available for this ticker"

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])
    fig.update_layout(
        title=f"{symbol.upper()} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )
    return fig

def update_table(symbol, period):
    df = get_stock_data(symbol, period)
    if df.empty:
        return "No data available for this ticker"
    return df

# View
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# Charta")
    with gr.Tab("Home"):
        with gr.Row():
            with gr.Column(scale=2):
                symbol_input = gr.Textbox(label="Enter Symbol")
                period_input = gr.Radio(
                    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"],
                    label="Select Period",
                    value="max"
                )
                chart_output = gr.Plot()
                table_output = gr.DataFrame()
            with gr.Column(scale=1):
                strategy_input = gr.Textbox(
                    label="Enter your trading strategy code here",
                    lines=20
                )

        symbol_input.change(update_chart, inputs=[symbol_input, period_input], outputs=chart_output)
        period_input.change(update_chart, inputs=[symbol_input, period_input], outputs=chart_output)
        symbol_input.change(update_table, inputs=[symbol_input, period_input], outputs=table_output)
        period_input.change(update_table, inputs=[symbol_input, period_input], outputs=table_output)

    with gr.Tab("Learn"):
        gr.Markdown("## Learn Tab")
        gr.Markdown("Here you can find resources and tutorials to help you learn more.")

    with gr.Tab("Trade"):
        gr.Markdown("## Trade Tab")
        gr.Markdown("This section is dedicated to trading features and tools.")

demo.launch()
