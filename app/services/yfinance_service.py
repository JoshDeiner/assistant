import os
from typing import Dict, Tuple
import yfinance as yf
import pandas as pd
from os.path import isfile, dirname, isdir
from os import makedirs

from .base_service import BaseService
from ..clients.yfinance_client import YFinanceClient

class YFinanceService(BaseService):
    """
    Service for fetching and working with stock data from Yahoo Finance.
    """
    
    def __init__(self, **kwargs):
        self.client = kwargs.get('client')
        if not self.client:
            # Create default client if none provided
            ticker = kwargs.get('ticker', 'VOO')
            period = kwargs.get('period')
            interval = kwargs.get('interval')
            csv_file_path = kwargs.get('csv_file_path')
            self.client = YFinanceClient(
                ticker=ticker,
                period=period,
                interval=interval,
                csv_file_path=csv_file_path
            )
        
    def execute(self, *args, **kwargs):
        """Main execution logic for the service."""
        # Get the operation type from kwargs
        operation = kwargs.get('operation', 'fetch_ticker_data')
        
        if operation == 'fetch_ticker_data':
            return self.fetch_ticker_data()
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def fetch_ticker_data(self) -> Tuple[int, Dict]:
        """
        Fetch data for the specified ticker using the YFinance client.
        
        Returns:
            (0, {"data": csv_file_path}) on success
            (1, {"error": "..."}) on failure
        """
        return self.client.fetch()