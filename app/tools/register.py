"""
Tool registration module
"""
from .factory import ToolFactory
from .crypto_tools import DownloadBtcDataTool, CryptoPriceTool
from .shell_tools import CommandExecTool
from .code_tools import CalcTool, CodeWriteTool
from app.streamlit.streamlit_tool import StreamlitVisualizationTool

def register_all_tools():
    """
    Register all available tools with the ToolFactory
    """
    ToolFactory.register_tool(DownloadBtcDataTool())
    ToolFactory.register_tool(CryptoPriceTool())
    ToolFactory.register_tool(CommandExecTool())
    ToolFactory.register_tool(CalcTool())
    ToolFactory.register_tool(CodeWriteTool())
    ToolFactory.register_tool(StreamlitVisualizationTool())
    
    return ToolFactory.get_all_schemas()