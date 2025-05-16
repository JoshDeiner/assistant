crypto_price_tool_schema = {
    "name": "crypto_price_tool",
    "description": (
        "Fetches the current price of Bitcoin in the specified national currency using a live external API. "
        "Returns a tuple (status_code, result_dict), where status_code is 0 for success and 1 for failure. "
        "If successful, result_dict contains the Bitcoin price. If failed, it contains an error message."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "currency": {
                "type": "string",
                "description": "The national (fiat) currency to convert the Bitcoin price into (e.g., 'usd', 'eur', 'gbp').",
                "default": "usd"
            }
        },
        "required": ["currency"]
    }
}