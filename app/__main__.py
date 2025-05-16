# Import document loading functions and tool schema

# prompt ideas
# entity mapping for relationships and events

from dotenv import load_dotenv
from anthropic import Anthropic
from app.schemas.schema import calc_tool
from app.schemas.schema import code_write_tool
from app.schemas.schema import code_write_tool
from app.schemas.index import tools
from app.schemas.crypto_currencies_schema import crypto_price_tool_schema
from app.errors import ApiError, CryptoPriceError

from app.schemas.shell_schema import command_exec_tool
import os
from collections import deque

from app.functions.functions import print_calc
from app.functions.functions import extract_code_block_from_string
from app.functions.crypto_currency_functions import bitcoin_price_tool

from app.functions.shell_functions import run_command_secure

from colorama import Fore, Style, init

from app.prompts import get_system_prompt
from app.utils.main import load_doc
from app.utils.main import llm_classify_with_schema
load_dotenv()
client = Anthropic()

MODEL = os.getenv("MODEL", "model")
MAX_CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", 200_000))
MAX_TOKEN_BLOCK = int(os.getenv("MAX_TOKEN_BLOCK", 8000))

PRELOAD_PATH = os.getenv("PRELOAD_PATH", "NONE")

# PRELOAD_FILES = ["chapter_one.yml"]
# METADATA_FILE = "metadata.yml"
METADATA_FILE = ""

PRELOAD_FILES=[
    'app.py',
    'config.py',
    'routes.py',
    'utils.py',
    ## more
    'update.md',
    'request.md',
    'todo.md',
    'metadata.yml'
]


# Initialize colorama for Windows compatibility
init(autoreset=True)  # Resets color after each print

def exec(prompt: str, client, messages: list, tool_choice: int = 0, token_count: int = 0):

    rag_content = None
    if METADATA_FILE:
        rag_content = load_doc(
            base_path=PRELOAD_PATH,
            metadata_file=METADATA_FILE
        )
    else:
        rag_content = load_doc(
            base_path=PRELOAD_PATH
        )


    system_prompt = get_system_prompt(rag_content, PRELOAD_PATH)

    messages.append({"role": "user", "content": prompt})

    args = {
        "model": MODEL,
        "system": system_prompt,
        "messages": messages,
    }

    api_args = {
        **args,
        "max_tokens": 1000,
        "tools": tools,
        "tool_choice": {"type": "any"}
    }

    token_count = client.messages.count_tokens(**args)
    print("tot", token_count, token_count.input_tokens)

    response = None

    if tool_choice:
        response = client.messages.create(**api_args)
    else:
        args["max_tokens"] = 1000
        response = client.messages.create(**args)

        print("Not using tools based on classification.")

    print("respon", response)


    if token_count.input_tokens > MAX_TOKEN_BLOCK:
        print("token individual count high")

    print("response", response)
    # Check if a tool call was made
    if response.stop_reason == "tool_use" and tool_choice == 1:
        content = response.content[-1]
        tool_name = content.name
        print(f"Tool requested: {tool_name}")

        tool_result = None

        if tool_name == crypto_price_tool_schema["name"]:
            tool_input = content.input
            tool_result = None
            current_message = messages[-1]

            try:
                # call tool
                # Call tool only once
                status, cmd_result = bitcoin_price_tool(currency="usd")
                print("st", status, cmd_result)

                if status == 1:
                    raise ValueError("problem with api request")

                statement = f"Bitcoin current price: {cmd_result.get('bitcoin_price')}"
                print("statement", statement)
                current_message["content"] += f"\n\n[Tool Output]:\n{statement}"
                tool_result = statement
            except CryptoPriceError as e:
                print(f"❌ Crypto Error: {e}")
            except ApiError as e:
                print(f"❌ General API Error: {e}")
            except Exception as e:
                print(f"error: {e}")
                return 1 

        if tool_name == command_exec_tool["name"]:
            tool_input = content.input
            input_cmd = tool_input['input_command']
            sink = tool_input['working_dir']

            tool_result = None
            current_message = messages[-1]
            print("curr", current_message)
            # current_message['output'] = None

            try:
                cmd_output = run_command_secure(input_cmd, sink)
                print("cmd", cmd_output, cmd_output['status'])
                tool_result = cmd_output.get("output")
                current_message["content"] += f"\n\n[Tool Output]:\n{tool_result}"
                
            except Exception as e:
                tool_result = 1
                print(e, "exception")
                # current_message['output'] = e

        if tool_name == code_write_tool["name"]:
            print("Tool Invoked:", tool_name)
            tool_input = content.input
            input_text = tool_input.get('raw_text', '')
            output_file = tool_input.get('output_file', 'app.temp.py')  # Default fallback
            language_marker = tool_input.get('language_marker', 'python')
            mode = tool_input.get('mode', 'overwrite')  # New parameter to control file behavior

            
            try:

                print("Input Text:", input_text)
                print(f"Writing to: {output_file} | Mode: {mode}")

                # Call the function with dynamic parameters
                extract_code_block_from_string(
                    input_text=input_text,
                    output_file=output_file,
                    language_marker=language_marker,
                    mode=mode
                )

                tool_result = 0  # Success
            except Exception as e:
                tool_result = 1  # Failure
                print(f"Tool error for code writing, return code: {tool_result}, error: {e}")


        if tool_name == calc_tool["name"]:
            # Run the correct tool
            tool_input = content.input
            tool_result = print_calc(**tool_input)

        # Add tool result as assistant response
        assistant_response = f"Tool Result: {tool_result}"
    else:
        # Standard text-based response
        message_block = response.content[-1]
        assistant_response = message_block.text

    messages.append({"role": "assistant", "content": assistant_response})

    return assistant_response, messages, token_count



def chat_loop():
    client_instance = Anthropic()
    messages = deque(maxlen=50)
    token_count: int = 0

    try:
        while True:
            print("messages", len(messages))
            user_input = input(Fore.GREEN + Style.BRIGHT + "You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Ending chat session.")
                break

            # Classify whether a tool should be used
            classification_result = llm_classify_with_schema(
                user_input, client_instance, MODEL, tools
            )
            classification_confidence = classification_result['confidence']
            print("calc", classification_confidence, classification_result)
            print("classification_result", classification_result['tool_name'])
            tool_use = None
            if classification_result['tool_name'] == 'None':
                tool_use = 0
            else:
                tool_use = 1 if classification_confidence >= 0.5 else 0
            print(tool_use, "tool")

            # assistant_response, messages = exec(user_input, client_instance, messages, tool_use)
            assistant_response, messages, token_count = exec(
                user_input, client_instance, messages, tool_use
            )

            token_limit = MAX_CONTEXT_WINDOW * 0.25
            if token_count.input_tokens >= token_limit:
                print("token size at 25%")

            print(Fore.CYAN + Style.BRIGHT + f"Assistant: {assistant_response}\n")
    except KeyboardInterrupt:
        print("\nChat session ended by user.")



if __name__ == "__main__":
    chat_loop()
