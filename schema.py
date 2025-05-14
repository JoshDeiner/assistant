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