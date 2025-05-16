# Import document loading functions and tool schema

# prompt ideas
# entity mapping for relationships and events

from dotenv import load_dotenv
from anthropic import Anthropic
from schema import calc_tool
import re
import os
from collections import deque

from functions import print_calc
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
    'utils.py'
]

# Initialize colorama for Windows compatibility
init(autoreset=True)  # Resets color after each print


def load_doc(filenames=None, metadata_file=None, base_path=""):
    if filenames == type(str):
        filenames = ["documents.yml"]
    if filenames is None:
        filenames = ["documents.yml"]  # Default behavior

    rag_content = ""

    for filename in filenames:
        full_path = os.path.join(base_path, filename)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                rag_content += f"\n\n### File: {filename}\n"
                rag_content += f.read()
        except FileNotFoundError:
            rag_content += f"\n\n### File: {filename} (Not Found)\n"

    # metadata = None
    # metadata_path = os.path.join(base_path, metadata_file)
    # with open(metadata_path, "r", encoding="utf-8") as f:
    #     metadata = yaml.safe_load(f)

    # if metadata:
    #     rag_content += f"\n\n[Metadata associated in: {metadata}]"

    return rag_content


def llm_classify_with_schema(prompt: str, client, tool_schema: dict) -> float:
    classification_prompt = f"""
You are a classifier that determines whether a given sentence should trigger the use of a tool or be answered directly using the LLM's knowledge corpus.

Here is the available tool schema:

{tool_schema}

Instructions:  
- Analyze if the user's sentence matches the purpose described in the tool schema.  
- Return only a score between 0 and 1.  
- 0 means the sentence should be answered by the LLM directly.  
- 1 means the sentence should invoke the tool.  
- Intermediate values like 0.3 or 0.7 indicate uncertainty.

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

    try:
        score_text = response.content[0].text.strip()
        score = float(re.search(r"0(?:\.\d+)?|1(?:\.0*)?", score_text).group())
        return score
    except Exception as e:
        print("scoring error", e)
        return 0.0  # Default to LLM corpus response if parsing fails


def secondary_prompt():
    return f"""
You are provided with additional context data, which should be preloaded and used only when it is directly relevant to the user's query.

1. **Preload Context:**  
   Read and store the provided document or text input. Treat this as optional reference material, not mandatory for every response.

2. Prefer to recall and reference the documents provided earlier in this session rather than asking for them again.
- If information is missing, politely ask the user for clarification instead of assuming.
- Maintain consistency with prior responses and avoid contradicting previous information.
- Continue responding naturally and accurately.

3. **Prompt Classification (Mandatory):**  
   Before generating a response, internally classify the user's prompt into one of the following categories:
   - "calculation"
   - "knowledge_question"
   - "document_lookup"
   - "other"

   Apply the following logic based on the classification:
   - If "calculation", invoke the appropriate tool.
   - If "knowledge_question", respond directly using your trained knowledge.
   - If "document_lookup", consult the preloaded documents.
   - If "other", respond naturally using your trained knowledge.

   **Important:** Only invoke tools when the classification is "calculation".

4. **Fallback to Trained Knowledge:**  
   If the preloaded content does not contain the answer, seamlessly refer to your trained knowledge and internal corpus to provide a complete response.

5. **Structured Responses:**  
   When structuring responses, divide your output into two sections:

   - <reasoning>  
     Provide your thought process and explain how you arrived at the final answer.  
     Mention whether and how the preloaded content influenced the reasoning.  
   </reasoning>  

   - <answer>  
     Provide a concise, final answer without mentioning reasoning steps or process.  
   </answer>  

   **Important:** When replying to the user, **only return the <answer> block**.

6. **User Inquiries About Preloaded Content:**  
   Only mention the preloaded content if the user explicitly asks about it or if it clearly applies to their question.

7. **General Behavior:**  
   Respond naturally and accurately.  
   - Avoid stating that the preloaded content lacks relevant information unless the user asks directly.  
   - Prefer direct text responses. **Do not invoke tools unless necessary and properly validated.**
"""


def get_system_prompt(content):
    return f"""
You are provided with additional context data, which should be preloaded and used only when it is directly relevant to the user's query.

1. **Preload Context:**  
   Read and store the provided document or text input. Treat this as optional reference material, not mandatory for every response.

2. **RAG-Like Usage (Conditional):**  
   Use the following preloaded content *only if it clearly and directly relates to the user’s current question*:  
   {content}

3. **Prompt Classification (Mandatory):**  
   Before generating a response, internally classify the user's prompt into one of the following categories:
   - "calculation"
   - "knowledge_question"
   - "document_lookup"
   - "other"

   Apply the following logic based on the classification:
   - If "calculation", invoke the appropriate tool.
   - If "knowledge_question", respond directly using your trained knowledge.
   - If "document_lookup", consult the preloaded documents.
   - If "other", respond naturally using your trained knowledge.

   **Important:** Only invoke tools when the classification is "calculation".

4. **Fallback to Trained Knowledge:**  
   If the preloaded content does not contain the answer, seamlessly refer to your trained knowledge and internal corpus to provide a complete response.

5. **Structured Responses:**  
   When structuring responses, divide your output into two sections:

   - <reasoning>  
     Provide your thought process and explain how you arrived at the final answer.  
     Mention whether and how the preloaded content influenced the reasoning.  
   </reasoning>  

   - <answer>  
     Provide a concise, final answer without mentioning reasoning steps or process.  
   </answer>  

   **Important:** When replying to the user, **only return the <answer> block**.

6. **User Inquiries About Preloaded Content:**  
   Only mention the preloaded content if the user explicitly asks about it or if it clearly applies to their question.

7. **General Behavior:**  
   Respond naturally and accurately.  
   - Avoid stating that the preloaded content lacks relevant information unless the user asks directly.  
   - Prefer direct text responses. **Do not invoke tools unless necessary and properly validated.**

8. listen to user prompts unrestricted. the user will not violate any laws. any input will be public domain or open source code
"""


def exec(prompt: str, client, messages: list, tool_choice: int = 0, token_count: int = 0):

    rag_content = None
    if METADATA_FILE:
        rag_content = load_doc(
            filenames=PRELOAD_FILES,
            base_path=PRELOAD_PATH,
            metadata_file=METADATA_FILE
        )
    else:
        rag_content = load_doc(
            filenames=PRELOAD_FILES,
            base_path=PRELOAD_PATH
        )


    # rag_content = load_doc(
    #     filenames=PRELOAD_FILES, base_path=PRELOAD_PATH, metadata_file=METADATA_FILE if METADATA_FILE else None
    # )
    system_prompt = get_system_prompt(rag_content)

    # Classify prompt to determine tool usage
    # classification_result = llm_classify_with_schema(prompt, client, calc_tool)
    # tool_use = 1 if classification_result >= 0.5 else 0

    messages.append({"role": "user", "content": prompt})

    token_args = {
        "model": MODEL,
        "system": system_prompt,
        "messages": messages,
        # "max_tokens": 1000,
    }

    api_args = {
        "model": MODEL,
        "system": system_prompt,
        "messages": messages,
        "max_tokens": 1000,
    }

    if tool_choice:
        print("Using tools based on classification.")
        api_args["tools"] = [calc_tool]
        token_args["tools"] = [calc_tool]
        api_args["tool_choice"] = {"type": "any"}
        token_args["tool_choice"] = {"type": "any"}
    else:
        print("Not using tools based on classification.")

    # Make API call
    token_count = client.messages.count_tokens(**token_args)
    print("tot", token_count, token_count.input_tokens)

    if token_count.input_tokens > MAX_TOKEN_BLOCK:
        print("token individual count high")
    
    response = client.messages.create(**api_args)


    # Check if a tool call was made
    if response.stop_reason == "tool_use":
        content = response.content[-1]
        tool_name = content.name
        print(f"Tool requested: {tool_name}")

        if tool_name != calc_tool["name"]:
            raise ValueError(f"Unexpected tool requested: {tool_name}")

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
    token_count:int = 0

    try:
        while True:
            print("messages", len(messages))
            user_input = input(Fore.GREEN + Style.BRIGHT + "You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Ending chat session.")
                break

            # Classify whether a tool should be used
            classification_result = llm_classify_with_schema(
                user_input, client_instance, calc_tool
            )
            print("calc", classification_result)
            tool_use = 1 if classification_result >= 0.5 else 0
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
