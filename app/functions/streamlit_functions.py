"""
Functions for Streamlit visualizations
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, Tuple

def launch_streamlit_visualization(
    service_name: str,
    file_path: str = "bitcoin_data.csv", 
    chart_title: str = "Data Visualization") -> Dict[str, Any]:
    """
    Launch a Streamlit visualization with specified parameters.
    
    Args:
        service_name: Name of the service to use (bitcoin_chart, bitcoin_data)
        file_path: Path to data file
        chart_title: Title for the chart
        
    Returns:
        Dict containing status and result information
    """
    try:
        # Get path to the streamlit orchestrator script
        script_path = Path(__file__).resolve().parent.parent / "streamlit" / "streamlit_orchestrator.py"
        
        # Prepare command line arguments
        args = [
            f"--service_name={service_name}",
            f"--file_path={file_path}",
            f"--chart_title={chart_title}"
        ]
        
        # Build the command to run streamlit
        cmd = f"streamlit run {script_path} -- {' '.join(args)}"
        
        # Launch streamlit as a subprocess
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # Get initial output to check for errors
            stdout, stderr = process.communicate(timeout=3)
            
            if process.returncode is not None and process.returncode != 0:
                return {"status": 1, "error": f"Failed to start Streamlit: {stderr}"}
            
            # Extract the URL from stdout if available
            url = "http://localhost:8501"  # Default Streamlit URL
            for line in stdout.split('\n'):
                if "External URL:" in line:
                    url = line.split("External URL:")[1].strip()
                    break
            
            return {"status": 0, "message": f"Streamlit visualization launched at: {url}"}
        except subprocess.TimeoutExpired:
            # This is expected since streamlit keeps running
            return {"status": 0, "message": "Streamlit visualization started at http://localhost:8501"}
            
    except Exception as e:
        return {"status": 1, "error": f"Error launching Streamlit visualization: {str(e)}"}