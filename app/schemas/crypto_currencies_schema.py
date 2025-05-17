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


download_btc_data_tool = {
    "name": "download_btc_data",
    "description": (
        "Downloads or returns a CSV of Bitcoin weekly-start prices. "
        "If `csv_file_path` already exists, returns it immediately; "
        "otherwise fetches daily BTC-USD history since `start_date`, "
        "resamples to weekly starts (Mondays), saves to CSV, and returns the path."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "csv_file_path": {
                "type": "string",
                "description": "Path for the CSV (default: app/dummyapp/btc_weekly_start.csv)"
            },
            "start_date": {
                "type": "string",
                "format": "date",
                "description": "History start date (YYYY-MM-DD; default 2013-01-01)"
            },
        },
        "required": []
    }
}
