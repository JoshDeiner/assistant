import os

def load_doc(base_path):
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

def llm_classify_with_schema(prompt: str, client, tool_schemas: list, model) -> dict:
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
            model=model,
            messages=[{"role": "user", "content": classification_prompt}],
            max_tokens=1000,
        )
    except Exception as e:
        print("classification error", e)
        return {"tool_name": None, "confidence": 0.0}

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

