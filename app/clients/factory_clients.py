from app.clients.crypto_currency_clients import BitcoinPriceClient
from app.clients.yfinance_client import YFinanceClient
from app.clients.api_client import ApiClient

class ApiClientFactory:
    _clients = {
        "bitcoin": BitcoinPriceClient,
        "yfinance": YFinanceClient,
    }

    @staticmethod
    def get_client(name: str, **kwargs) -> ApiClient:
        client_class = ApiClientFactory._clients.get(name.lower())
        if not client_class:
            raise ValueError(f"API client '{name}' is not registered.")
        return client_class(**kwargs)
    