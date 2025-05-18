import os
from typing import Dict, Any, Tuple
from app.clients.factory_clients import ApiClientFactory

def stock_data_function(
    ticker: str = "VOO",
    period: str = None,
    interval: str = None,
    csv_file_path: str = None
) -> Tuple[int, Dict]:
    """
    Fetches historical stock data.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'VOO', 'VTI').
        period (str, optional): The time period to fetch data for (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max').
        interval (str, optional): The interval between data points (e.g., '1d', '1wk', '1mo').
        csv_file_path (str, optional): Path to save the CSV file.

    Returns:
        Tuple[int, Dict]: (status_code, result_dict)
        - status_code: 0 for success, 1 for error
        - result_dict: Contains either the result or an error message
    """
    client = ApiClientFactory.get_client(
        "yfinance", 
        ticker=ticker,
        period=period,
        interval=interval,
        csv_file_path=csv_file_path
    )
    return client.fetch()