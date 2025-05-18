import streamlit as st
from services.bitcoin_chart_service import BitcoinChartService

class StreamlitClient:
    def __init__(self, service=None):
        """Initialize with a chart service or create a default one."""
        self.service = service
    
    def run(self):
        """Run the Streamlit application."""
        
        # Simply call the chart service's execute method
        self.service.execute(file_path="btc_data.csv", chart_title="Bitcoin Data Analysis")