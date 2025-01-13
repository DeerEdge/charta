import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from bokeh.embed import file_html
from bokeh.resources import CDN
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from cerebras.cloud.sdk import Cerebras

cerebras_client = Cerebras(api_key='key')

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

def show_table(symbol, period):
    df = update_table(symbol, period)
    return gr.DataFrame(visible=True), df


def run_backtest(df, strategy_code):
    try:
        # Compile the user-provided strategy code to check for syntax errors
        compile(strategy_code, '<string>', 'exec')

        # Execute the user-provided strategy code
        exec(strategy_code, globals())

        # Find the last defined class in the global namespace
        strategy_classes = [obj for obj in globals().values() if isinstance(obj, type) and issubclass(obj, Strategy)]
        if not strategy_classes:
            return "No valid Strategy class found in the code", None

        strategy_class = strategy_classes[-1]
        df.reset_index(inplace=True)

        bt = Backtest(df, strategy_class, cash=10000, commission=.002)
        stats = bt.run()

        # Generate the plot
        plot = bt.plot()

        # Convert stats to a DataFrame
        stats_df = pd.DataFrame({'Metric': stats.index, 'Value': stats.values})

        return stats_df, plot
    except SyntaxError as e:
        return f"Syntax error in strategy code: {e}", None
    except Exception as e:
        print("out")
        return str(e), None


def chat_with_ai(message, history):
    messages = [{"role": "system", "content": "You are a helpful assistant specializing in stock trading strategies."}]

    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})

    messages.append({"role": "user", "content": message})

    response = cerebras_client.chat.completions.create(
        model="llama3.1-70b",
        messages=[{"role": "user", "content": message}]
    )

    return [{"role": "assistant", "content": response.choices[0].message.content}]


# View
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# Charta")
    with gr.Tab("Home"):
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Row():
                    symbol_input = gr.Textbox(label="Enter Symbol", scale=7)
                    chart_button = gr.Button("Chart", scale=1)
                period_input = gr.Radio(
                    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"],
                    label="Select Period",
                    value="max"
                )
                chart_output = gr.Plot()
                show_table_button = gr.Button("Show historical data as table")
                table_output = gr.DataFrame(visible=False)
                backtest_button = gr.Button("Run Backtest")
                backtest_stats = gr.Dataframe(label="Backtest Statistics")
                backtest_plot = gr.Plot(label="Backtest Plot")
            with gr.Column(scale=1):
                strategy_input = gr.Code(
                    label="Strategy Code:",
                    language="python",
                    lines=30,
                    value=
                """
                from backtesting import Strategy
from backtesting.lib import crossover

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()
                """
                )

                chat_input = gr.Textbox(label="Chat with AI", placeholder="Ask about trading strategies...")
                chat_output = gr.Chatbot(label="AI Assistant", type="messages")
                clear_button = gr.Button("Clear Chat")

        chart_button.click(update_chart, inputs=[symbol_input, period_input], outputs=chart_output)
        period_input.change(update_chart, inputs=[symbol_input, period_input], outputs=chart_output)
        chart_button.click(update_table, inputs=[symbol_input, period_input], outputs=table_output)
        period_input.change(update_table, inputs=[symbol_input, period_input], outputs=table_output)
        chat_input.submit(chat_with_ai, inputs=[chat_input, chat_output], outputs=[chat_output])
        clear_button.click(lambda: None, None, chat_output, queue=False)


        def backtest_handler(symbol, period, strategy_code):
            df = get_stock_data(symbol, period)
            if df.empty:
                return "No data available for this ticker", None
            stats, plot = run_backtest(df, strategy_code)
            return stats, plot


        backtest_button.click(
            backtest_handler,
            inputs=[symbol_input, period_input, strategy_input],
            outputs=[backtest_stats, backtest_plot]
        )

    with gr.Tab("Learn"):
        gr.Markdown("## Learn Tab")
        gr.Markdown("Here you can find resources and tutorials to help you learn more.")

    with gr.Tab("Trade"):
        gr.Markdown("## Trade Tab")
        gr.Markdown("This section is dedicated to trading features and tools.")

demo.launch()
