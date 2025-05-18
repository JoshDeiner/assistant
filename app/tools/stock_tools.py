"""
Stock market related tools
"""
from typing import Dict, Any, Tuple
from app.tools.base import Tool
from app.functions.yfinance_functions import stock_data_function
from app.schemas.yfinance_schema import stock_data_tool_schema
from app.errors import ApiError

class StockDataTool(Tool):
    """
    Tool for downloading stock price data
    """
    @property
    def name(self) -> str:
        return stock_data_tool_schema["name"]
    
    @property
    def schema(self) -> Dict[str, Any]:
        return stock_data_tool_schema
    
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, str]:
        """
        Download stock price data
        
        Args:
            tool_input: Dictionary containing:
                - ticker: Stock symbol
                - period: Optional time period
                - interval: Optional data interval
                - csv_file_path: Optional path to save the CSV
                
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - result message or error message
        """
        try:
            ticker = tool_input.get("ticker", "VOO")
            period = tool_input.get("period")
            interval = tool_input.get("interval")
            csv_file_path = tool_input.get("csv_file_path")
            
            status, result = stock_data_function(
                ticker=ticker,
                period=period,
                interval=interval,
                csv_file_path=csv_file_path
            )
            
            if status == 1:
                return 1, f"Problem fetching data: {result.get('error', 'Unknown error')}"
                
            data_path = result.get("data")
            return 0, f"Successfully downloaded {ticker} data to {data_path}"
        except ApiError as e:
            return 1, f"API Error: {e}"
        except Exception as e:
            return 1, str(e)
    
    def format_output(self, result: str) -> str:
        return result