import streamlit as st
from services.bitcoin_chart_service import BitcoinChartService
from streamlit_client import StreamlitClient
import sys
from pathlib import Path

# Add the project root directory to sys.path

def main(file_path: str, chart_title: str):
    st.set_page_config(
        page_title=chart_title,
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize chart service
    # does it make sense to add 
    # chart_service = BitcoinChartService()

    # Pre-configure the service with some defaults
    # probably need a factory method to decide which service to call
    chart_service = BitcoinChartService(file_path, chart_title)
    client = StreamlitClient(chart_service)
    client.run()

if __name__ == "__main__":
    # service = 
    # decides which variables to pass in by llm metadata
    main(
        file_path="btc_data.csv",
        chart_title="BTC Weekly Overview"

        )