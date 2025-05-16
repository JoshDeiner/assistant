import os

def print_calc(num1: int, num2: int, operator: str):
    
    if operator == "addition":
        return num1 + num2
    elif operator == "subtraction":
        return num1 - num2
    elif operator == "multiplication" or operator == "multiply" or operator == "*":
        return num1 * num2
    elif operator == "division":
        if num2 == 0:
            return "Error: Division by zero!"
        else:
            return num1 / num2
    else:
        return "Error: Invalid operator!"




def extract_code_block_from_string(input_text, output_file, language_marker="python", mode="overwrite"):
    print("input text", input_text)
    inside_block = False
    extracted_lines = []

    PRELOAD_PATH = os.getenv("PRELOAD_PATH", "NONE")

    # Secure and restrict file path to the special directory
    safe_base_path = os.path.abspath(PRELOAD_PATH)
    target_file_name = os.path.basename(output_file)
    safe_output_path = os.path.abspath(os.path.join(safe_base_path, target_file_name))

    # Ensure file stays within the allowed directory
    if not safe_output_path.startswith(safe_base_path):
        raise ValueError(f"❌ Attempt to write outside the allowed directory: {safe_output_path}")

    # Extract code block
    for line in input_text.splitlines():
        stripped_line = line.strip()
        if stripped_line == f"```{language_marker}":
            inside_block = True
            continue
        if stripped_line.startswith("```") and inside_block:
            inside_block = False
            continue
        if stripped_line.startswith("</") and inside_block:
            inside_block = False
            continue
        if inside_block:
            extracted_lines.append(line)

    if not extracted_lines and input_text.strip():
        print("⚠️ No code block markers found, falling back to raw input.")
        extracted_code = input_text.strip()
    else:
        extracted_code = "\n".join(extracted_lines).strip()

    # Ensure directory exists
    os.makedirs(safe_base_path, exist_ok=True)

    # ✅ Handle File Writing Modes
    if mode == "append":
        with open(safe_output_path, "a") as f:
            f.write("\n" + extracted_code + "\n")
    elif mode == "merge":
        try:
            with open(safe_output_path, "r") as f:
                existing_content = f.read()
            if extracted_code not in existing_content:
                with open(safe_output_path, "a") as f:
                    f.write("\n" + extracted_code + "\n")
        except FileNotFoundError:
            with open(safe_output_path, "w") as f:
                f.write(extracted_code + "\n")
    else:  # overwrite
        with open(safe_output_path, "w") as f:
            f.write(extracted_code + "\n")

    print(f"✅ Code written to {safe_output_path} with mode '{mode}'")
    return 0