import os
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

# check if csv file for this exists. if it does just return status code and csv file ie 1, {data: content}

# Create a Ticker object for VOO
voo = yf.Ticker("VOO")

period = os.getenv("PERIOD", "10y")  # Default to 10 years if not set
interval = os.getenv("INTERVAL_GRAPH", "1d")  # Default to daily if not set

# Get last 10 years of historical data (daily)
voo_data = voo.history(period=period, interval=interval)

voo_data.to_csv("voo_weekly_data.csv")

