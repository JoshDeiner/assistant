"""
Code writing and calculation tools
"""
from typing import Dict, Any, Tuple
from .base import Tool
from app.schemas.schema import calc_tool, code_write_tool
from app.functions.functions import print_calc, extract_code_block_from_string

class CalcTool(Tool):
    """
    Tool for performing calculations
    """
    @property
    def name(self) -> str:
        return calc_tool["name"]
    
    @property
    def schema(self) -> Dict[str, Any]:
        return calc_tool
    
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, Any]:
        """
        Perform calculations
        
        Args:
            tool_input: Dictionary of calculation parameters
                
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - calculation result or error message
        """
        try:
            result = print_calc(**tool_input)
            return 0, result
        except Exception as e:
            return 1, str(e)
    
    def format_output(self, result: Any) -> str:
        return str(result)

class CodeWriteTool(Tool):
    """
    Tool for writing code to files
    """
    @property
    def name(self) -> str:
        return code_write_tool["name"]
    
    @property
    def schema(self) -> Dict[str, Any]:
        return code_write_tool
    
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, str]:
        """
        Write code to a file
        
        Args:
            tool_input: Dictionary containing:
                - raw_text: The text/code to write
                - output_file: The file to write to (default: 'app.temp.py')
                - language_marker: The language marker (default: 'python')
                - mode: File write mode (default: 'overwrite')
                
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - result message or error message
        """
        try:
            input_text = tool_input.get('raw_text', '')
            output_file = tool_input.get('output_file', 'app.temp.py')
            language_marker = tool_input.get('language_marker', 'python')
            mode = tool_input.get('mode', 'overwrite')
            
            extract_code_block_from_string(
                input_text=input_text,
                output_file=output_file,
                language_marker=language_marker,
                mode=mode
            )
            
            return 0, f"Successfully wrote code to {output_file}"
        except Exception as e:
            return 1, str(e)
    
    def format_output(self, result: str) -> str:
        return result