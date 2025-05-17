"""
Shell command execution tools
"""
from typing import Dict, Any, Tuple
from .base import Tool
from app.functions.shell_functions import run_command_secure
from app.schemas.shell_schema import command_exec_tool

class CommandExecTool(Tool):
    """
    Tool for executing shell commands securely
    """
    @property
    def name(self) -> str:
        return command_exec_tool["name"]
    
    @property
    def schema(self) -> Dict[str, Any]:
        return command_exec_tool
    
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, str]:
        """
        Execute a shell command securely
        
        Args:
            tool_input: Dictionary containing:
                - input_command: The command to execute
                - working_dir: The working directory for command execution
                
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - command output or error message
        """
        try:
            input_cmd = tool_input.get('input_command', '')
            sink = tool_input.get('working_dir', '')
            
            cmd_output = run_command_secure(input_cmd, sink)
            status = cmd_output.get('status', 1)
            output = cmd_output.get('output', '')
            
            return status, output
        except Exception as e:
            return 1, str(e)
    
    def format_output(self, result: str) -> str:
        return result