stock_data_tool_schema = {
    "name": "stock_data_tool",
    "description": (
        "Fetches historical price data for a specified stock ticker using Yahoo Finance. "
        "Returns a tuple (status_code, result_dict), where status_code is 0 for success and 1 for failure. "
        "If successful, result_dict contains the data path. If failed, it contains an error message."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol (e.g., 'VOO', 'VTI', 'AAPL').",
                "default": "VOO"
            },
            "period": {
                "type": "string",
                "description": "The time period to fetch data for (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max').",
                "default": "10y"
            },
            "interval": {
                "type": "string",
                "description": "The interval between data points (e.g., '1d', '1wk', '1mo').",
                "default": "1d"
            },
            "csv_file_path": {
                "type": "string",
                "description": "Local filesystem path for the output CSV",
                "default": "app/stock_data.csv"
            }
        },
        "required": ["ticker"]
    }
}