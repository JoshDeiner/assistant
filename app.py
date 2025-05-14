# Import document loading functions and tool schema

from dotenv import load_dotenv
from anthropic import Anthropic
from schema import calc_tool
import re

from enum import Enum

from colorama import Fore, Style, init


load_dotenv()
client = Anthropic()


# Initialize colorama for Windows compatibility
init(autoreset=True)  # Resets color after each print

# print(Fore.RED + "This text is red.")
# print(Back.YELLOW + "This background is yellow.")
# print(Style.BRIGHT + "This text is bright.")
# print(Style.DIM + "This text is dim.")
# print(Style.RESET_ALL + "Back to normal.")

# print(Fore.GREEN + Style.BRIGHT + "Bright green text!")
# print(Fore.CYAN + Back.BLACK + "Cyan text on black background.")

class LLMResponseType(Enum):
    DEFAULT = 0
    TOOL = 1

def extract_blocks(response_text):
    blocks = {}
    reasoning_match = re.search(
        r"<reasoning>(.*?)</reasoning>", response_text, re.DOTALL
    )
    answer_match = re.search(r"<answer>(.*?)</answer>", response_text, re.DOTALL)

    blocks["reasoning"] = reasoning_match.group(1).strip() if reasoning_match else None
    blocks["answer"] = answer_match.group(1).strip() if answer_match else None

    return blocks


# # Define the document loading tool
# calc_tool = {
#     "name": "print-calculate-tool",
#     "description": "Performs a basic arithmetic operation on two numbers.",
#     "input_schema": {
#         "type": "object",
#         "properties": {
#             "num1": {
#                 "type": "number",
#                 "description": "The first number for the calculation.",
#             },
#             "operator": {
#                 "type": "string",
#                 "description": "The operation to perform (addition, multiplication, substraction, division).",
#             },
#             "num2": {
#                 "type": "number",
#                 "description": "The second number for the calculation.",
#             },
#         },
#         "required": ["num1", "operator", "num2"],
#     },
# }


def print_calc(num1: int, num2: int, operator: str):
    if operator == "addition":
        return num1 + num2
    elif operator == "subtraction":
        return num1 - num2
    elif operator == "multiplication":
        return num1 * num2
    elif operator == "division":
        if num2 == 0:
            return "Error: Division by zero!"
        else:
            return num1 / num2
    else:
        return "Error: Invalid operator!"


def load_doc(filename: str = "documents.yml"):
    rag_content = ""
    with open(filename, "r") as f:
        rag_content = f.read()

    return rag_content


# def exec(prompt: str, client, tool_use: int = 0):
#     rag_content = load_doc("documents.yml")

#     system_prompt = f"""
# You are provided with additional context data, which should be preloaded and used only when it is directly relevant to the user's query.

# 1. **Preload Context:**  
#    Read and store the provided document or text input. Treat this as optional reference material, not mandatory for every response.

# 2. **RAG-Like Usage (Conditional):**  
#    Use the following preloaded content *only if it clearly and directly relates to the user’s current question*:  
#    {rag_content}

# 3. **Prompt Classification (Mandatory):**  
#    Before generating a response, internally classify the user's prompt into one of the following categories:
#    - "calculation"
#    - "knowledge_question"
#    - "document_lookup"
#    - "other"

#    Apply the following logic based on the classification:
#    - If "calculation", invoke the appropriate tool.
#    - If "knowledge_question", respond directly using your trained knowledge.
#    - If "document_lookup", consult the preloaded documents.
#    - If "other", respond naturally using your trained knowledge.

#    **Important:** Only invoke tools when the classification is "calculation".

# 4. **Fallback to Trained Knowledge:**  
#    If the preloaded content does not contain the answer, seamlessly refer to your trained knowledge and internal corpus to provide a complete response.

# 5. **Structured Responses:**  
#    When structuring responses, divide your output into two sections:

#    - <reasoning>  
#      Provide your thought process and explain how you arrived at the final answer.  
#      Mention whether and how the preloaded content influenced the reasoning.  
#    </reasoning>  

#    - <answer>  
#      Provide a concise, final answer without mentioning reasoning steps or process.  
#    </answer>  

#    **Important:** When replying to the user, **only return the <answer> block**.

# 6. **User Inquiries About Preloaded Content:**  
#    Only mention the preloaded content if the user explicitly asks about it or if it clearly applies to their question.

# 7. **General Behavior:**  
#    Respond naturally and accurately.  
#    - Avoid stating that the preloaded content lacks relevant information unless the user asks directly.  
#    - Prefer direct text responses. **Do not invoke tools unless necessary and properly validated.**
# """


#     # initial response to model
#     # initiates the model session
#     # user response
#     # just text
#     response = None
#     messages = [{"role": "user", "content": prompt}]

#     if tool_use == 0:
#         print("not using tools")
#         response = client.messages.create(
#             model="claude-3-haiku-20240307",
#             system=system_prompt,
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=400,
#         )
#     else:
#         print("using tools for init response")

#         response = client.messages.create(
#             model="claude-3-haiku-20240307",
#             system=system_prompt,
#             tool_choice={'type': 'any',},
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=400,
#             tools=[calc_tool],
#         )



#     # create while loop based on some condition
#     # update messages based on each api encounter
#     # probably print out answer




#     if not response.content:
#         raise ValueError("error")
    

#     # get response back from init

#     # update messages for assistant object
#     # call api

#     # get response back create user message block


#     # parse/create assistant response. and send back


#     print()
#     print("rrrr", response, response.role, response.content[-1])
#     try:

#         while True:
#             print("messages array", messages)
#             # messages.append({
#             #     "role": response.role,
#             #     "content": response.content[-1]
#             # })

#             # response = None
            
#             print()
#             if response.stop_reason == "tool_use":
#                 print("using tool")
#                 content = response.content[-1]
#                 print("content", content, content.name)
#                 if content.name == "print-calculate-tool":
#                     print("using calculator tool")

#                     tool_input = content.input
#                     response = print_calc(**tool_input)

#                     messages.append({
#                         "role": response.role,
#                         "content": response
#                     })

#                     client.messages.create(
#                         model="claude-3-haiku-20240307",
#                         system=system_prompt,
#                         tool_choice={'type': 'any',},
#                         messages=messages,
#                         max_tokens=400,
#                         tools=[calc_tool],
#                     )


#                     print(Fore.RED + "res", response)
                

#                 print("hi")
#             else:
#                 print("else block")
#                 message_block = response.content[-1]
#                 response = message_block.text

#                 print("message", message_block)

#                 messages.append({
#                     "role": response.role,
#                     "content": message_block
#                 })

#                 client.messages.create(
#                     model="claude-3-haiku-20240307",
#                     system=system_prompt,
#                     messages=messages,
#                     max_tokens=400,
#                 )

#                 print(Fore.RED + "Text", Fore.RED + response)
#     except KeyboardInterrupt as K:
#         print("interupt from chatbot", K)
#     except Exception as e:
#         print("chatbox exception", e)


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

    print("hi")
    response = None
    try:

        response = Anthropic().messages.create(
            model="claude-3-haiku-20240307",
            messages=[{"role": "user", "content": classification_prompt}],
            max_tokens=10
        )
    except Exception as e:
        print("ugh", e)

    try:
        score_text = response.content[0].text.strip()
        score = float(re.search(r"0(?:\.\d+)?|1(?:\.0*)?", score_text).group())
        return score
    except Exception:
        return 0.0  # Default to LLM corpus response if parsing fails



# def client():
#     client = Anthropic()
#     # create a while loop that continually prompts user 
#     # while true execute input sequence. enable a graceful exit

#     try:
#         while True:
#             # print(Fore.GREEN + Style.BRIGHT + "Bright green text!")
#             prompt = input(Fore.GREEN + Style.BRIGHT + "what is your question?: ")
#             classification_result = llm_classify_with_schema(prompt, client, calc_tool)
#             exec(prompt, client, classification_result)
#     except KeyboardInterrupt as KI:
#         raise ValueError("keyboard interuptt") 
#     except Exception as e:
#         print("exception wrapper", e)




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
"""

def exec(prompt: str, client, messages: list, tool_use: int = 0):
    rag_content = load_doc("documents.yml")
    system_prompt = get_system_prompt(rag_content)

    current_prompt = system_prompt if not messages else secondary_prompt() 

    messages.append({"role": "user", "content": prompt})

    

    if tool_use == 0:
        print("not using tools")
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            system=current_prompt,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
    else:
        print("using tools for init response")

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            system=current_prompt,
            tool_choice={'type': 'any',},
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            tools=[calc_tool],
        )


    message_block = response.content[-1]
    assistant_response = message_block.text
    messages.append({"role": "assistant", "content": assistant_response})

    return assistant_response, messages



def chat_loop():
    client_instance = Anthropic()
    messages = []

    try:
        while True:
            print("messages", len(messages))
            user_input = input(Fore.GREEN + Style.BRIGHT + "You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Ending chat session.")
                break

            # Classify whether a tool should be used
            classification_result = llm_classify_with_schema(user_input, client_instance, calc_tool)
            tool_use = 1 if classification_result >= 0.5 else 0

            assistant_response, messages = exec(user_input, client_instance, messages, tool_use)

            print(Fore.CYAN + Style.BRIGHT + f"Assistant: {assistant_response}\n")
    except KeyboardInterrupt:
        print("\nChat session ended by user.")

chat_loop()
