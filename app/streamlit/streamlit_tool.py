"""
Streamlit visualization tool
"""
from typing import Dict, Any, Tuple
from app.tools.base import Tool
from app.schemas.streamlit_schema import streamlit_visualization_schema
from app.functions.streamlit_functions import launch_streamlit_visualization

# move this to a functional approach

class StreamlitVisualizationTool(Tool):
    """
    Tool for launching Streamlit visualizations
    """
    @property
    def name(self) -> str:
        return streamlit_visualization_schema["name"]
    
    @property
    def schema(self) -> Dict[str, Any]:
        return streamlit_visualization_schema
    
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, str]:
        """
        Launch a Streamlit visualization app as a subprocess
        
        Args:
            tool_input: Dictionary containing:
                - service_name: Name of the service to use
                - file_path: Path to the data file (optional)
                - chart_title: Title for the chart (optional)
                
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - result message
        """
        # Extract parameters
        service_name = tool_input.get("service_name")
        file_path = tool_input.get("file_path", "btc_data.csv")
        chart_title = tool_input.get("chart_title", "Bitcoin Data Visualization")
        
        # Call the function
        result = launch_streamlit_visualization(
            service_name=service_name, 
            file_path=file_path, 
            chart_title=chart_title
        )
        
        if result["status"] == 0:
            return 0, result["message"]
        else:
            return 1, result.get("error", "Unknown error")
    
    def format_output(self, result: str) -> str:
        return result