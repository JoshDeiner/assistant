from app.clients.api_client import ApiClient

# http_service.py
# move later
import requests

# bitcoin_price_client.py
from typing import Tuple, Dict, Optional, Any
import requests
from app.clients.api_client import ApiClient
from app.services.http_service import RequestsHTTPService


class BitcoinPriceClient(ApiClient):
    """
    Client to fetch Bitcoin price data from CoinGecko.

    Attributes:
        http: An HTTP service used to perform GET requests.
    """
    def __init__(
        self,
        currency: str = "usd",
        http_service: Optional[RequestsHTTPService] = None,
    ) -> None:
        # Initialize parent with query params
        super().__init__({"ids": "bitcoin", "vs_currencies": currency.lower()})
        # Inject or default to RequestsHTTPService
        self.http = RequestsHTTPService()

    @property
    def BASE_URL(self) -> str:
        return "https://api.coingecko.com/api/v3/simple/price"

    def parse_response(self, raw: Dict) -> Dict:
        """
        Normalize and extract the Bitcoin price from CoinGecko's JSON.
        """
        return {"bitcoin_price": raw.get("bitcoin", {}).get("usd")}

    def fetch(self) -> Tuple[int, Dict]:
        """
        Fetch the current Bitcoin price.

        Returns:
            A tuple of (status_code, data_or_error):
              - status_code == 0: success, data contains parsed response
              - status_code == 1: failure, data contains error message
        """
        try:
            response = self.http.get(
                self.BASE_URL,
                params=self.params,
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            return 0, self.parse_response(data)
        except requests.RequestException as e:
            return 1, {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return 1, {"error": f"Unexpected error: {str(e)}"}



def main():
    client = BitcoinPriceClient()
    status, result = client.fetch()
    if status == 0:
        print(f"Current BTC price: {result['bitcoin_price']}")
    else:
        print(f"Error fetching price: {result['error']}")


if __name__ == "__main__":
    main()
