from keys import *
from supabase import create_client, Client

nyse_tickers_path = "tasks/nyse_tickers.txt"
nasdaq_tickers_path = "tasks/nasdaq_tickers.txt"
historical_data_table = "ALPHAVANTAGE_OPTIONS_HISTORICAL_DATA"
url: str = SUPABASE_URL
key: str = SUPABASE_SERVICE_ROLE_KEY
supabase: Client = create_client(url, key)