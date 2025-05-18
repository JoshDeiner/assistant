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

from app.services.base_service import BaseService

class BitcoinDataService(BaseService):
    """
    Service for fetching and persisting Bitcoin historical data.
    """
    
    def __init__(self, default_file_path="btc_data.csv", default_start_date="2013-01-01"):
        self.default_file_path = default_file_path
        self.default_start_date = default_start_date

    def execute(self, file_path=None, start_date=None):
        """
        Main execution logic for the service.
        Fetches Bitcoin data and displays it in Streamlit.
        """
        file_path = file_path or self.default_file_path
        start_date = start_date or self.default_start_date
        
        st.title("Bitcoin Data Service")
        st.write("## Fetch and Display Bitcoin Historical Data")
        
        # Control panel
        file_path = st.sidebar.text_input("CSV File Path", file_path)
        start_date = st.sidebar.text_input("Start Date (YYYY-MM-DD)", start_date)
        
        if st.sidebar.button("Fetch Bitcoin Data"):
            with st.spinner("Fetching Bitcoin data..."):
                status, result = self.fetch_weekly_start(file_path, start_date)
                
                if status == 0:
                    st.success(f"Data successfully saved to {result['csv_file_path']}")
                    # Display the data
                    try:
                        df = pd.read_csv(result['csv_file_path'])
                        df['Date'] = pd.to_datetime(df['Date'])
                        st.write("### Bitcoin Weekly Data")
                        st.dataframe(df)
                        st.line_chart(df.set_index('Date'))
                    except Exception as e:
                        st.error(f"Error displaying data: {e}")
                else:
                    st.error(f"Error fetching data: {result['error']}")
    
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