import streamlit as st
from services.base_service import BaseService

class StreamlitClient:
    def __init__(self, service=None):
        """
        Initialize with a service instance.
        
        Args:
            service: Any service that implements the execute method
        """
        self.service = service
    
    def run(self):
        """Run the Streamlit application by delegating to the service's execute method."""
        if not self.service:
            st.error("No service provided to StreamlitClient")
            return
            
        # Call the service's execute method
        # We assume all services implement the execute method
        self.service.execute()