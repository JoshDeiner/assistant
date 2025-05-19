import os
import sys
import subprocess
import yfinance as yf
import pandas as pd
from typing import Tuple, Dict
from dotenv import load_dotenv
# Add the parent directory to sys.path to allow absolute imports
from app.clients.factory_clients import ApiClientFactory
from app.services.service_factory import ServiceFactory

from typing import Any, Dict

def bitcoin_price_function(currency: str = "usd", client_factory=None) -> tuple[int, dict]:
    """
    Fetches the current price of Bitcoin.

    Args:
        currency (str): The fiat currency to compare against (default is 'usd').
        client_factory: Optional API client factory instance.

    Returns:
        Tuple: (status_code, result_dict)
        - status_code: 0 for success, 1 for error
        - result_dict: Contains either the result or an error message
    """
    # Use provided client factory or default to ApiClientFactory
    client_factory = client_factory or ApiClientFactory
    
    client = client_factory.get_client("bitcoin", currency=currency)
    return client.fetch()  # Status and result directly returned



def download_btc_data(service_factory=None, **kwargs: Any) -> Dict:
    """
    LLM tool adapter for BitcoinDataService.fetch_weekly_start.
    Accepts:
      - csv_file_path: str
      - start_date: str (YYYY-MM-DD)
      - service_factory: Optional service factory instance
    Returns:
      {
        "status": int,            # 0 = success, 1 = error
        "csv_file_path": str,     # if status == 0
        "error": str              # if status == 1
      }
    """
    # Use provided service factory or default to ServiceFactory
    service_factory = service_factory or ServiceFactory
    
    data_file = os.getenv("DATA", "1")
    other_app_path = os.path.abspath(data_file) 

    csv_file_path = kwargs.get("csv_file_path", "bitcoin_data.csv")
    full_csv_file_path = os.path.join(other_app_path, csv_file_path)

    if os.path.isfile(full_csv_file_path):
        # If the file already exists, we can skip downloading it again
        return {"status": 0, "csv_file_path": full_csv_file_path}

    # probably create a tuility that says current date minus ten years
    start_date    = kwargs.get("start_date", "2013-01-01")

    # Use the injected service factory to get the BitcoinDataService
    bitcoin_data_service = service_factory.create_service("bitcoin_data")
    status, result = bitcoin_data_service.execute(
        operation='fetch_weekly_start',
        csv_file_path=full_csv_file_path,
        start_date=start_date
    )

    # merge into a single dict
    return {"status": status, **result}



if __name__ == "__main__":
    # Example usage
    load_dotenv()  # Load environment variables from .env file if needed
    
    # Example using default client factory
    currency = "usd"
    status_code, result_dict = bitcoin_price_function(currency)
    print(f"Status Code: {status_code}")
    print(f"Result: {result_dict}")
    
    # Example with explicitly provided ApiClientFactory instance
    api_factory = ApiClientFactory()
    status_code, result_dict = bitcoin_price_function(currency, client_factory=api_factory)
    print(f"Status Code (with injected factory): {status_code}")
    print(f"Result (with injected factory): {result_dict}")

    # Example usage of download_btc_data with the default ServiceFactory
    result = download_btc_data(csv_file_path="bitcoin_data.csv", start_date="2013-01-01")
    print(result)
    
    # Example with explicitly provided ServiceFactory instance
    service_factory = ServiceFactory()
    result = download_btc_data(service_factory=service_factory, csv_file_path="bitcoin_data.csv")
    print(result)
