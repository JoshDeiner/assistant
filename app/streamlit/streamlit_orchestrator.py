import sys
from pathlib import Path
import argparse

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from app.services.service_factory import ServiceFactory
from app.streamlit.streamlit_client import StreamlitClient


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
        
        # Adjust file_path to use data directory if it's a relative path
        if "file_path" in service_params and not Path(service_params["file_path"]).is_absolute():
            # Check if path starts with 'data/'
            if not service_params["file_path"].startswith("data/"):
                # Construct path using project root /data directory
                project_root = Path(__file__).resolve().parent.parent.parent
                service_params["file_path"] = str(project_root / "data" / service_params["file_path"])
        
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
        This should ONLY be used for testing purposes.
        
        Returns:
            dict: Default configuration parameters
        """
        # Construct absolute path to data file in data directory
        project_root = Path(__file__).resolve().parent.parent.parent
        return {
            "service_name": "bitcoin_chart",
            "file_path": str(project_root / "data" / "bitcoin_data.csv"),
            "chart_title": "Bitcoin Data Visualization"
        }


def parse_args():
    """Parse command line arguments passed to the script."""
    parser = argparse.ArgumentParser(description="Streamlit visualization application")
    parser.add_argument("--service_name", default="bitcoin_chart", help="Service name to use")
    parser.add_argument("--file_path", default="bitcoin_data.csv", help="Path to data file")
    parser.add_argument("--chart_title", default="Data Visualization", help="Chart title")
    
    # Parse known args to handle Streamlit's own arguments
    args, _ = parser.parse_known_args()
    return args


if __name__ == "__main__":
    orchestrator = StreamlitOrchestrator()
    
    # Parse command line arguments
    args = parse_args()
    
    # Use parsed arguments instead of default config
    orchestrator.run(
        service_name=args.service_name,
        file_path=args.file_path,
        chart_title=args.chart_title
    )
