from app.clients.api_client import ApiClient

class BitcoinPriceClient(ApiClient):
    def __init__(self, currency: str = "usd"):
        # Initialize API parameters dynamically based on currency input
        super().__init__({"ids": "bitcoin", "vs_currencies": currency.lower()})

    @property
    def BASE_URL(self) -> str:
        return "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    def fetch(self) -> tuple[int, dict]:
        import requests
        try:
            response = requests.get(self.BASE_URL, params=self.params, timeout=5)
            response.raise_for_status()
            return 0, self.parse_response(response.json())  # Success status
        except requests.RequestException as e:
            return 1, {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return 1, {"error": f"Unexpected error: {str(e)}"}

    def parse_response(self, data: dict) -> dict:
        currency = self.params.get("vs_currencies", "usd").lower()
        price = data.get("bitcoin", {}).get(currency)
        return {"bitcoin_price": price}
    

