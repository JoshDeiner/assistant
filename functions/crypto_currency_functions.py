from  clients.factory_clients import ApiClientFactory
import os, sys


def bitcoin_price_tool(currency: str = "usd") -> dict:
    """
    Fetches the current price of Bitcoin.

    Args:
        currency (str): The fiat currency to compare against (default is 'usd').

    Returns:
        dict: A dictionary containing the Bitcoin price or an error message.
    """
    try:
        client = ApiClientFactory.get_client("bitcoin", currency=currency)
        return client.fetch()
    except Exception as e:
        return {"error": str(e)}
    


# result = bitcoin_price_tool(currency="usd")
# print(result)  # Example: {'bitcoin_price': 68000}