"""
Tool factory implementing the Factory pattern
"""
from typing import Dict, Type, List
from .base import Tool

class ToolFactory:
    """
    Factory class for tool management.
    Follows the Open/Closed Principle by allowing new tools to be added without modifying existing code.
    """
    _tools: Dict[str, Tool] = {}
    
    @classmethod
    def register_tool(cls, tool_instance: Tool) -> None:
        """
        Register a tool instance with the factory
        
        Args:
            tool_instance: An instance of a Tool subclass
        """
        cls._tools[tool_instance.name] = tool_instance
    
    @classmethod
    def get_tool(cls, tool_name: str) -> Tool:
        """
        Get a tool instance by name
        
        Args:
            tool_name: The name of the tool to retrieve
            
        Returns:
            The tool instance
            
        Raises:
            ValueError: If the tool name is not registered
        """
        tool = cls._tools.get(tool_name)
        if not tool:
            raise ValueError(f"Unknown tool: {tool_name}")
        return tool
    
    @classmethod
    def get_all_schemas(cls) -> List[Dict]:
        """
        Get all registered tool schemas
        
        Returns:
            List of tool schemas
        """
        return [tool.schema for tool in cls._tools.values()]