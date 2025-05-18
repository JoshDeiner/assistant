import os
from typing import Tuple, Dict, Optional
import yfinance as yf
from api_client import ApiClient
from dotenv import load_dotenv


class YFinanceClient(ApiClient):
    """
    Client to fetch stock data from Yahoo Finance.

    Attributes:
        ticker: The stock ticker symbol to fetch data for.
        period: The time period to fetch data for.
        interval: The interval between data points.
        csv_file_path: Path to save the CSV data.
    """
    def __init__(
        self,
        ticker: str = "VOO",
        period: str = None,
        interval: str = None,
        csv_file_path: str = None,
    ) -> None:
        # Initialize parent with empty params (not used for yfinance)
        super().__init__({})
        self.ticker = ticker
        # Get values from environment or use defaults
        self.period = period or os.getenv("PERIOD", "10y")
        self.interval = interval or os.getenv("INTERVAL_GRAPH", "1wk")
        self.csv_file_path = csv_file_path or f"./data/{ticker.lower()}_data.csv"

    @property
    def BASE_URL(self) -> str:
        # This is a placeholder since we're not making HTTP requests directly
        return "https://finance.yahoo.com"

    def parse_response(self, raw: Dict) -> Dict:
        """
        Not used in this client as yfinance handles the data directly.
        """
        return raw

    def fetch(self) -> Tuple[int, Dict]:
        """
        Fetch historical data for the specified ticker.

        Returns:
            A tuple of (status_code, data_or_error):
              - status_code == 0: success, data contains path to CSV file
              - status_code == 1: failure, data contains error message
        """
        # Check if CSV file already exists
        if os.path.isfile(self.csv_file_path):
            return 0, {"data": self.csv_file_path}

        try:
            # Create a Ticker object
            ticker_obj = yf.Ticker(self.ticker)
            
            # Get historical data
            data = ticker_obj.history(
                period=self.period,
                interval=self.interval
            )
            
            # Save to CSV
            data.to_csv(self.csv_file_path)
            
            return 0, {"data": self.csv_file_path}
        except Exception as e:
            return 1, {"error": f"Error fetching stock data: {str(e)}"}

def main():
    client = YFinanceClient(ticker="VOO")
    status, result = client.fetch()
    if status == 0:
        print(f"Data saved to: {result['data']}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    load_dotenv()
    main()
