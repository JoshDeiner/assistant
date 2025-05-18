import sys
from pathlib import Path

import streamlit as st
from app.services.service_factory import ServiceFactory
from app.streamlit_client import StreamlitClient


class StreamlitApp:
    """
    Streamlit application class that uses the Service Factory pattern
    to dynamically create and inject services.
    """
    
    def __init__(self):
        """Initialize the Streamlit application."""
        pass
        
    def run(self, service_name: str, **service_params):
        """
        Main application entry point that uses the ServiceFactory to create 
        and inject the appropriate service into the StreamlitClient.
        
        Args:
            service_name: Name of the service to create (must be registered in ServiceFactory)
            **service_params: Parameters to pass to the service constructor
        """
        st.set_page_config(
            page_title=service_params.get("chart_title", "Data Visualization"),
            page_icon="📊",
            layout="wide"
        )
        
        # Create the service dynamically using the ServiceFactory
        try:
            service = ServiceFactory.create_service(service_name, **service_params)
            client = StreamlitClient(service)
            client.run()
        except ValueError as e:
            st.error(f"Error: {str(e)}")
            st.info("Available services: bitcoin_chart, bitcoin_data")
    
    def get_default_config(self):
        """
        Returns the default configuration for the application.
        This can be extended to load from environment variables, config files, etc.
        
        Returns:
            dict: Default configuration parameters
        """
        return {
            "service_name": "bitcoin_chart",
            "file_path": "btc_data.csv",
            "chart_title": "BTC Weekly Overview"
        }


if __name__ == "__main__":
    # Create and run the application with default configuration
    app = StreamlitApp()
    config = app.get_default_config()
    
    # This could be modified to accept command line arguments or LLM function calls
    app.run(**config)