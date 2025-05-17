import yfinance as yf
from pandas import Timestamp
from pandas import to_datetime
from typing import Dict
from typing import Tuple

from os import makedirs
from os.path import isfile
from os.path import dirname
from os.path import isdir
from os import getenv

class BitcoinDataService:
    """
    Service for fetching and persisting Bitcoin historical data.
    """

    @staticmethod
    def fetch_weekly_start(
        csv_file_path: str,
        start_date: str = "2013-01-01"
    ) -> Tuple[int, Dict]:
        """
        If the weekly-start CSV already exists, return it immediately.
        Otherwise download daily BTC-USD data from start_date to today,
        resample to weekly starts (Mondays), save the first 'Close' price
        of each week to CSV, and return the status tuple.

        Returns:
            (0, {"csv_file_path": path}) on success
            (1, {"error": "..."}) on failure
        """
        # 1) If the file already exists, skip download
        if isfile(csv_file_path):
            return 0, {"csv_file_path": csv_file_path}

        try:
            # 2) Ensure parent directory exists
            parent_dir = dirname(csv_file_path)
            if parent_dir and not isdir(parent_dir):
                makedirs(parent_dir, exist_ok=True)

            # 3) Download daily BTC-USD data
            btc = yf.download(
                "BTC-USD",
                start=start_date,
                end=Timestamp.today().strftime("%Y-%m-%d"),
                interval="1d",
                progress=False
            )
            btc.index = to_datetime(btc.index)

            # 4) Resample to weekly starts (Mondays) and take first 'Close' price
            weekly_start = btc["Close"].resample("W-MON").first()

            # 5) Write to CSV
            weekly_start.to_csv(csv_file_path, index=True, header=True)

            return 0, {"csv_file_path": csv_file_path}

        except Exception as e:
            return 1, {"error": str(e)}

