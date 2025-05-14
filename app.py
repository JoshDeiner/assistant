# Import document loading functions and tool schema

from dotenv import load_dotenv
from anthropic import Anthropic
from schema import calc_tool
import re
import os

from colorama import Fore, Style, init


load_dotenv()
client = Anthropic()

MODEL =os.getenv("MODEL", "model")

# Initialize colorama for Windows compatibility
init(autoreset=True)  # Resets color after each print


def extract_blocks(response_text):
    blocks = {}
    reasoning_match = re.search(
        r"<reasoning>(.*?)</reasoning>", response_text, re.DOTALL
    )
    answer_match = re.search(r"<answer>(.*?)</answer>", response_text, re.DOTALL)

    blocks["reasoning"] = reasoning_match.group(1).strip() if reasoning_match else None
    blocks["answer"] = answer_match.group(1).strip() if answer_match else None

    return blocks


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
            model=MODEL,
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
            model=MODEL,
            system=current_prompt,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
    else:
        print("using tools for init response")

        response = client.messages.create(
            model=MODEL,
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


if __name__ == "__main__":
    chat_loop()
