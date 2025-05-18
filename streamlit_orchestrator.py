import sys
from pathlib import Path

import streamlit as st
from services.service_factory import ServiceFactory
from streamlit_client import StreamlitClient


class StreamlitOrchestrator:
    """
    Streamlit orchestrator class that uses dependency injection to orchestrate
    the creation of services and streamlit client execution.
    """
    
    def __init__(self, service_factory=None, streamlit_client=None):
        """
        Initialize the Streamlit orchestrator with dependencies.
        
        Args:
            service_factory: Factory for creating services (defaults to ServiceFactory)
            client_class: Client class to instantiate (defaults to StreamlitClient)
        """
        self.service_factory = service_factory or ServiceFactory()
        self.streamlit_client = streamlit_client or StreamlitClient
        
    def run(self, service_name: str, **service_params):
        """
        Main application entry point that orchestrates the service creation
        and client execution process.
        
        Args:
            service_name: Name of the service to create (must be registered in ServiceFactory)
            **service_params: Parameters to pass to the service constructor
        """
        st.set_page_config(
            page_title=service_params.get("chart_title", "Data Visualization"),
            page_icon="📊",
            layout="wide"
        )
        
        # Create the service dynamically using the injected service factory
        try:
            service = self.service_factory.create_service(service_name, **service_params)
            client = self.streamlit_client(service)
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
    orchestrator = StreamlitOrchestrator()
    config = orchestrator.get_default_config()
    
    # This could be modified to accept command line arguments or LLM function calls
    orchestrator.run(**config)