from app.clients.factory_clients import ApiClientFactory

if __name__ == "__main__":
    api_client = ApiClientFactory()
    btc_client = api_client.get_client("bitcoin", currency="usd")
    response = btc_client.fetch()
    print("res", response.get("bitcoin_price"))

    print("response", response)