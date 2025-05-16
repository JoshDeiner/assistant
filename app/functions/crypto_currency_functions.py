import os
import sys

# Add the parent directory to sys.path to allow absolute imports
from app.clients.factory_clients import ApiClientFactory


def bitcoin_price_tool(currency: str = "usd") -> tuple[int, dict]:
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
