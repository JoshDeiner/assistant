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
