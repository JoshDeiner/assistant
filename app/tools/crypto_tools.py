"""
Cryptocurrency-related tools
"""
from typing import Dict, Any, Tuple
from .base import Tool
from app.functions.crypto_currency_functions import download_btc_data, bitcoin_price_function
from app.schemas.crypto_currencies_schema import crypto_price_tool_schema, download_btc_data_tool
from app.errors import ApiError, CryptoPriceError

class DownloadBtcDataTool(Tool):
    """
    Tool for downloading Bitcoin price data
    """
    @property
    def name(self) -> str:
        return download_btc_data_tool["name"]
    
    @property
    def schema(self) -> Dict[str, Any]:
        return download_btc_data_tool
    
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, str]:
        """
        Download Bitcoin price data
        
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - result message
        """
        try:
            status, result = download_btc_data()
            if status == 1:
                return 1, "Problem with API request"
            return 0, "Successfully downloaded CSV file"
        except Exception as e:
            return 1, str(e)
    
    def format_output(self, result: str) -> str:
        return result

class CryptoPriceTool(Tool):
    """
    Tool for getting cryptocurrency prices
    """
    @property
    def name(self) -> str:
        return crypto_price_tool_schema["name"]
    
    @property
    def schema(self) -> Dict[str, Any]:
        return crypto_price_tool_schema
    
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, str]:
        """
        Get current Bitcoin price
        
        Args:
            tool_input: Dictionary containing:
                - currency (optional): Currency to show price in, defaults to "usd"
                
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - result message or error message
        """
        try:
            currency = tool_input.get("currency", "usd")
            status, cmd_result = bitcoin_price_function(currency=currency)
            
            if status == 1:
                return 1, "Problem with API request"
                
            price = cmd_result.get("bitcoin_price")
            return 0, f"Bitcoin current price: {price}"
        except CryptoPriceError as e:
            return 1, f"Crypto Error: {e}"
        except ApiError as e:
            return 1, f"General API Error: {e}"
        except Exception as e:
            return 1, str(e)
    
    def format_output(self, result: str) -> str:
        return result