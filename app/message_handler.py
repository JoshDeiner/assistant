"""
Message handling module for the application
"""
from typing import Dict, List, Tuple, Any
from anthropic import Anthropic
from app.tools.factory import ToolFactory
from app.utils.main import load_doc

class MessageHandler:
    """
    Handles processing of messages between the user and the assistant
    Follows the Single Responsibility Principle by separating message handling from tool execution
    """
    def __init__(
        self, 
        client: Anthropic, 
        model: str,
        preload_path: str = "NONE",
        metadata_file: str = "",
        max_tokens: int = 1000
    ):
        """
        Initialize the message handler
        
        Args:
            client: Anthropic client instance
            model: Model name to use
            preload_path: Path to preload documents from
            metadata_file: Metadata file name
            max_tokens: Maximum tokens for response
        """
        self.client = client
        self.model = model
        self.preload_path = preload_path
        self.metadata_file = metadata_file
        self.max_tokens = max_tokens
        
    def _load_rag_content(self) -> str:
        """
        Load RAG content from files
        
        Returns:
            RAG content as string
        """
        if self.metadata_file:
            return load_doc(
                base_path=self.preload_path,
                metadata_file=self.metadata_file
            )
        return load_doc(
            base_path=self.preload_path
        )
    
    def _handle_tool_response(
        self, 
        content: Any, 
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Handle tool execution and response
        
        Args:
            content: Tool content from response
            messages: List of message history
            
        Returns:
            Formatted tool result
        """
        tool_name = content.name
        tool_input = content.input
        print(f"Tool requested: {tool_name}")
        
        try:
            tool = ToolFactory.get_tool(tool_name)
            status, result = tool.execute(tool_input)
            
            if status != 0:
                raise ValueError(f"Tool execution failed: {result}")
                
            formatted_result = tool.format_output(result)
            
            # Update the last message with tool output
            current_message = messages[-1]
            current_message["content"] += f"\n\n[Tool Output]:\n{formatted_result}"
            
            return f"Tool Result: {formatted_result}"
        except Exception as e:
            print(f"Error executing tool {tool_name}: {e}")
            return f"Tool Error: {str(e)}"
    
    def process_message(
        self, 
        prompt: str, 
        messages: List[Dict[str, str]], 
        system_prompt: str,
        use_tools: bool = False
    ) -> Tuple[str, List[Dict[str, str]], Dict[str, int]]:
        """
        Process a message from the user
        
        Args:
            prompt: User input prompt
            messages: Message history
            system_prompt: System prompt
            use_tools: Whether to enable tool use
            
        Returns:
            Tuple containing:
                - Assistant's response
                - Updated message history
                - Token count information
        """
        # Add user message to history
        messages.append({"role": "user", "content": prompt})
        
        # Prepare API arguments
        args = {
            "model": self.model,
            "system": system_prompt,
            "messages": messages,
        }
        
        # Count tokens for tracking
        token_count = self.client.messages.count_tokens(**args)
        print("token count", token_count, token_count.input_tokens)
        
        # Prepare API call with tools if requested
        if use_tools:
            api_args = {
                **args,
                "max_tokens": self.max_tokens,
                "tools": ToolFactory.get_all_schemas(),
                "tool_choice": {"type": "any"}
            }
            response = self.client.messages.create(**api_args)
        else:
            args["max_tokens"] = self.max_tokens
            response = self.client.messages.create(**args)
            print("Not using tools based on classification.")
        
        print("res", response)
        
        # Process response based on type
        if response.stop_reason == "tool_use" and use_tools:
            content = response.content[-1]
            assistant_response = self._handle_tool_response(content, messages)
        else:
            # Standard text-based response
            message_block = response.content[-1]
            assistant_response = message_block.text
        
        # Add assistant response to history
        messages.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response, messages, token_count