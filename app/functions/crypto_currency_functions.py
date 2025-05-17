import os
import sys
import subprocess
import yfinance as yf
import pandas as pd
from typing import Tuple, Dict

# Add the parent directory to sys.path to allow absolute imports
from app.clients.factory_clients import ApiClientFactory

from typing import Any, Dict
from app.services.bitcoin_data_service import BitcoinDataService

def bitcoin_price_function(currency: str = "usd") -> tuple[int, dict]:
    """
    Fetches the current price of Bitcoin.

    Args:
        currency (str): The fiat currency to compare against (default is 'usd').

    Returns:
        Tuple: (status_code, result_dict)
        - status_code: 0 for success, 1 for error
        - result_dict: Contains either the result or an error message
    """
    client = ApiClientFactory.get_client("bitcoin", currency=currency)
    return client.fetch()  # Status and result directly returned



def download_btc_data(**kwargs: Any) -> Dict:
    """
    LLM tool adapter for BitcoinDataService.fetch_weekly_start.
    Accepts:
      - csv_file_path: str
      - start_date: str (YYYY-MM-DD)
    Returns:
      {
        "status": int,            # 0 = success, 1 = error
        "csv_file_path": str,     # if status == 0
        "error": str              # if status == 1
      }
    """
    csv_file_path = kwargs.get("csv_file_path", "app/dummyapp/btc_weekly_start.csv")
    start_date    = kwargs.get("start_date", "2013-01-01")

    status, result = BitcoinDataService.fetch_weekly_start(
        csv_file_path=csv_file_path,
        start_date=start_date
    )

    # merge into a single dict
    return {"status": status, **result}
