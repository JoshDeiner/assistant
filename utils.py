def extract_blocks(response_text):
    blocks = {}
    reasoning_match = re.search(
        r"<reasoning>(.*?)</reasoning>", response_text, re.DOTALL
    )
    answer_match = re.search(r"<answer>(.*?)</answer>", response_text, re.DOTALL)

    blocks["reasoning"] = reasoning_match.group(1).strip() if reasoning_match else None
    blocks["answer"] = answer_match.group(1).strip() if answer_match else None

    return blocks
