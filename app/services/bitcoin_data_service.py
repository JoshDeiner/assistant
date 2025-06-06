import yfinance as yf
import streamlit as st
import pandas as pd
from pandas import Timestamp
from pandas import to_datetime
from typing import Dict
from typing import Tuple

from os import makedirs
from os.path import isfile
from os.path import dirname
from os.path import isdir

from .base_service import BaseService

class BitcoinDataService(BaseService):
    """
    Service for fetching and persisting Bitcoin historical data.
    """
    
    def __init__(self, **kwargs):
        # Initialize with any needed parameters
        pass
        
    def execute(self, *args, **kwargs):
        """Main execution logic for the service."""
        # Get the operation type from kwargs
        operation = kwargs.get('operation', 'fetch_weekly_start')
        
        if operation == 'fetch_weekly_start':
            csv_file_path = kwargs.get('csv_file_path')
            start_date = kwargs.get('start_date', "2013-01-01")
            return self.fetch_weekly_start(csv_file_path, start_date)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
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
            
            # Create a DataFrame with a 'Date' column for compatibility
            result_df = weekly_start.reset_index()
            result_df.columns = ['Date', 'Close']

            # 5) Write to CSV
            result_df.to_csv(csv_file_path, index=False)

            return 0, {"csv_file_path": csv_file_path}

        except Exception as e:
            return 1, {"error": str(e)}