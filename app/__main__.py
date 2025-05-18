# Import document loading functions and tool schema
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from collections import deque
from colorama import Fore, Style, init

from app.tools.register import register_all_tools
from app.prompts import get_system_prompt
from app.utils.main import llm_classify_with_schema
from app.message_handler import MessageHandler

# Initialize colorama for Windows compatibility
init(autoreset=True)  # Resets color after each print

# Load environment variables
load_dotenv()
client = Anthropic()

# Configuration settings
MODEL = os.getenv("MODEL", "model")
MAX_CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", 200_000))
MAX_TOKEN_BLOCK = int(os.getenv("MAX_TOKEN_BLOCK", 8000))
LOCAL_PATH = os.getenv("PRELOAD_PATH", "NONE")
PRELOAD_PATH = os.path.abspath(LOCAL_PATH)
METADATA_FILE = ""

# Preload file list
#PRELOAD_FILES = [
#    'app.py',
#    'config.py',
#    'routes.py',
#    'utils.py',
#    'update.md',
#    'request.md',
#    'todo.md',
#    'metadata.yml'
#]

def chat_loop():
    """
    Main chat loop for the application
    """
    # Register all tools
    tool_schemas = register_all_tools()
    
    # Initialize client and message history
    client_instance = Anthropic()
    messages = deque(maxlen=50)
    token_count = 0
    
    # Create message handler
    message_handler = MessageHandler(
        client=client_instance,
        model=MODEL,
        preload_path=PRELOAD_PATH,
        metadata_file=METADATA_FILE
    )

    try:
        while True:
            print("messages", len(messages))
            user_input = input(Fore.GREEN + Style.BRIGHT + "You: ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Ending chat session.")
                break

            # Classify whether a tool should be used
            classification_result = llm_classify_with_schema(
                prompt=user_input,
                client=client_instance,
                model=MODEL,
                tool_schemas=tool_schemas
            )
            
            # Determine if we should use tools based on classification confidence
            classification_confidence = classification_result['confidence']
            print("calc", classification_confidence, classification_result)
            print("classification_result", classification_result['tool_name'])
            
            use_tools = False
            if classification_result['tool_name'] != 'None':
                use_tools = classification_confidence >= 0.5
            print(use_tools, "tool")

            # Get system prompt
            rag_content = message_handler._load_rag_content()
            system_prompt = get_system_prompt(rag_content, PRELOAD_PATH)
            
            # Process the message
            assistant_response, messages, token_count = message_handler.process_message(
                prompt=user_input,
                messages=list(messages),
                system_prompt=system_prompt,
                use_tools=use_tools
            )

            # Check token limit
            token_limit = MAX_CONTEXT_WINDOW * 0.25
            if token_count.input_tokens >= token_limit:
                print("token size at 25%")

            # Display assistant response
            print(Fore.CYAN + Style.BRIGHT + f"Assistant: {assistant_response}\n")
            
    except KeyboardInterrupt:
        print("\nChat session ended by user.")

if __name__ == "__main__":
    chat_loop()
