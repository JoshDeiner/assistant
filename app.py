# Import document loading functions and tool schema

# prompt ideas
# entity mapping for relationships and events

from dotenv import load_dotenv
from anthropic import Anthropic
from schemas.schema import calc_tool, code_write_tool, tools
from schemas.shell_schema import command_exec_tool
import re
import os
from collections import deque

from functions.functions import print_calc, extract_code_block_from_string
from functions.shell_functions import run_command_secure

from colorama import Fore, Style, init

load_dotenv()
client = Anthropic()

MODEL = os.getenv("MODEL", "model")
MAX_CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", 200_000))
MAX_TOKEN_BLOCK = int(os.getenv("MAX_TOKEN_BLOCK", 8000))

# PRELOAD_PATH = "/workspaces/codespaces-jupyter/documents/book"
PRELOAD_PATH = "/workspaces/codespaces-jupyter/dummyapp"

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
def load_doc(base_path=PRELOAD_PATH):
    rag_content = ""
    try:
        for filename in os.listdir(base_path):
            full_path = os.path.join(base_path, filename)
            if os.path.isfile(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    rag_content += f"\n\n### File: {filename}\n"
                    rag_content += f.read()
    except FileNotFoundError:
        print(f"❌ Directory {base_path} not found.")

    return rag_content


def llm_classify_with_schema(prompt: str, client, tool_schemas: list) -> dict:
    """
    Classifies whether a prompt should invoke one of the available tools.
    Returns a dictionary with the selected tool name (or None) and the confidence score.
    """

    # Build the tool schema section dynamically
    tool_schema_text = "\n\n".join(
        [f"- Tool Name: {tool['name']}\n  Description: {tool['description']}" for tool in tool_schemas]
    )

    classification_prompt = f"""
You are a classifier that determines whether a given sentence should trigger the use of one of the available tools 
or be answered directly using the LLM's knowledge corpus.

Available Tools:
{tool_schema_text}

Instructions:
- Analyze if the user's sentence matches the purpose of any of the tools above.
- If it matches, return the tool name and a confidence score between 0 and 1.
- If no tool matches, return "None" and a confidence score indicating your certainty.

Return your response strictly in this JSON format:

{{ 
  "tool_name": "<tool_name_or_None>", 
  "confidence": <confidence_score_between_0_and_1> 
}}

Classify the following sentence:

"{prompt}"
"""

    response = None
    try:
        response = client.messages.create(
            model=MODEL,
            messages=[{"role": "user", "content": classification_prompt}],
            max_tokens=1000,
        )
    except Exception as e:
        print("classification error", e)
        return {"tool_name": None, "confidence": 0.0}

    print("response fuck", response)
    try:
        import json
        response_text = response.content[0].text.strip()
        result = json.loads(response_text)
        print("result", result)
        return {
            "tool_name": result.get("tool_name", None),
            "confidence": float(result.get("confidence", 0.0))
        }
    except Exception as e:
        print("scoring error", e)
        return {"tool_name": None, "confidence": 0.0}


def get_system_prompt(content):
    return f"""
You are a smart automation assistant with access to specialized tools. Your role is to respond accurately and efficiently, using tools when appropriate.

You are a smart automation assistant with access to specialized tools. Your role is to respond accurately and efficiently, using tools when appropriate.

1. All file operations MUST occur only within the allowed directory: `{PRELOAD_PATH}`.
2. You can create, update, and read files within this directory freely. Do not attempt to use files outside this path.

3. Prompt Classification (Mandatory):  
   - "calculation" → Invoke the calculation tool.  
   - "code_generation" → Use `extract_code_block_from_string` to generate or modify code files.  
   - "command_execution" → Use `run_command_secure` to safely execute allowed shell commands and python within approved directories.  
   - "knowledge_question" → Respond directly using your trained knowledge.  
   - "document_lookup" → Consult preloaded documents.  
   - "other" → Respond naturally using your trained knowledge.

**Important:** Always return only the <answer> block to the user.

5. **Fallback to Trained Knowledge:**  
   If the preloaded content does not contain the answer, seamlessly refer to your trained knowledge.

6. **Structured Responses:**  
   When structuring responses, divide responses into:

   - <reasoning>  
     Explain your thought process and any tool invocation decisions.  
   </reasoning>

   - <answer>  
     Provide the final answer or result. If a tool was used, summarize the result here.  
   </answer>

   **Important:** **Always return only the <answer> block to the user.**

7. **General Behavior Guidelines:**  
   - Respond naturally and accurately.  
   - Invoke tools when a task involves code generation or file modification.  
   - Do not assume preloaded content is always relevant unless clearly applicable.  
   - Follow open knowledge and public domain guidelines. Assume all user inputs are open-source or legally safe.

8. **Unrestricted User Prompts:**  
   Listen to user prompts without restrictions. Assume the user will not violate any laws, and that all input is public domain or open-source content.
"""



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


    system_prompt = get_system_prompt(rag_content)

    # Classify prompt to determine tool usage
    # classification_result = llm_classify_with_schema(prompt, client, calc_tool)
    # tool_use = 1 if classification_result >= 0.5 else 0

    messages.append({"role": "user", "content": prompt})

    args = {
        "model": MODEL,
        "system": system_prompt,
        "messages": messages,
    }

    api_args = {
        **args,
        "max_tokens": 1000,
        "tools": [
            calc_tool,
            code_write_tool,
            command_exec_tool
            ],
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
        print("c", content)

        if tool_name == command_exec_tool["name"]:
            tool_input = content.input
            input_cmd = tool_input['input_command']
            sink = tool_input['working_dir']

            tool_result = None
            current_message = messages[-1]
            current_content = current_message.get('content')
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
                user_input, client_instance, [calc_tool, code_write_tool, command_exec_tool]
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
