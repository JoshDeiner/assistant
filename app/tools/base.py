"""
Base Tool class definition for the application
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional

class Tool(ABC):
    """
    Abstract base class for all tools in the application.
    Follows the Single Responsibility Principle by having each tool handle only one specific operation.
    """
    @abstractmethod
    def execute(self, tool_input: Dict[str, Any]) -> Tuple[int, Any]:
        """
        Execute the tool with the given input.
        
        Args:
            tool_input: Dictionary containing the input parameters for the tool
            
        Returns:
            Tuple containing:
                - status code (0 for success, 1 for failure)
                - result data or error message
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Returns the unique name identifier for this tool
        """
        pass
    
    @property
    @abstractmethod
    def schema(self) -> Dict[str, Any]:
        """
        Returns the schema definition for this tool
        """
        pass
    
    def format_output(self, result: Any) -> str:
        """
        Format the output of the tool for display to the user.
        Can be overridden by subclasses to provide custom formatting.
        
        Args:
            result: The result data from execute()
            
        Returns:
            Formatted string representation of the result
        """
        return str(result)