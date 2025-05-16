from api_client import ApiClient

class BitcoinPriceClient(ApiClient):
    def __init__(self, currency: str = "usd"):
        # Initialize API parameters dynamically based on currency input
        super().__init__({"ids": "bitcoin", "vs_currencies": currency.lower()})

    @property
    def BASE_URL(self) -> str:
        return "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    def parse_response(self, data: dict) -> dict:
        currency = self.params.get("vs_currencies", "usd").lower()
        price = data.get("bitcoin", {}).get(currency)
        return {"bitcoin_price": price}