calc_tool = {
    "name": "print-calculate-tool",
    "description": "Performs a basic arithmetic operation on two numbers.",
    "input_schema": {
        "type": "object",
        "properties": {
            "num1": {
                "type": "number",
                "description": "The first number for the calculation.",
            },
            "operator": {
                "type": "string",
                "description": "The operation to perform (addition, multiplication, substraction, division).",
            },
            "num2": {
                "type": "number",
                "description": "The second number for the calculation.",
            },
        },
        "required": ["num1", "operator", "num2"],
    },
}
code_write_tool = {
    "name": "extract_code_block_from_string",
    "description": (
        "Extracts code blocks from LLM responses and writes them to a file. "
        "Use this tool to create new files or update existing ones."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "raw_text": {
                "type": "string",
                "description": "The raw LLM output text containing code blocks or raw code."
            },
            "output_file": {
                "type": "string",
                "description": "The path to the output file (e.g., 'app_updated.py')."
            },
            "language_marker": {
                "type": "string",
                "description": "Optional. Code block language marker. Defaults to 'python'.",
                "default": "python"
            },
            "mode": {
                "type": "string",
                "description": "How to handle existing files: 'overwrite', 'append', or 'merge'. Defaults to 'overwrite'.",
                "default": "overwrite"
            }
        },
        "required": ["raw_text", "output_file"]
    },
}



