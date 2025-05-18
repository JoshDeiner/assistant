"""
Schema definitions for Streamlit-related tools
"""

streamlit_visualization_schema = {
    "name": "streamlit_visualization",
    "description": (
        """Launches a Streamlit visualization dashboard based on the specified service.
        The tool runs Streamlit as a subprocess and returns a URL where the visualization
        can be accessed. Returns a tuple (status_code, result), where status_code is 0 for 
        success and 1 for failure."""
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "service_name": {
                "type": "string",
                "description": "Type of visualization service to use",
                "enum": ["bitcoin_chart"],
                "default": "bitcoin_chart"
            },
            "file_path": {
                "type": "string",
                "description": "Path to the data file to visualize",
                "default": "btc_data.csv"
            },
            "chart_title": {
                "type": "string",
                "description": "Title to display on the chart",
                "default": "Data Visualization"
            }
        },
        "required": ["service_name", "file_path"]
    }
}