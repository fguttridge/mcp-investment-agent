# tools/calculator_tool.py
import math
import re

def calculate(expression: str) -> str:
    try:
        if not re.match(r'^[\d\s\.\+\-\*\/\(\),a-zA-Z]+$', expression):
            return "Error: Invalid characters in expression."

        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        return str(eval(expression, {"__builtins__": {}}, allowed))
    except Exception as e:
        return f"Error: {str(e)}"