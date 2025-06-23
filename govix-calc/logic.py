import re

# Allow digits, operators, decimal, parentheses, percent, sign
SAFE_EXPR = re.compile(r"^[0-9+\-*/().%±]*$")

def safe_eval(expr: str) -> str:
    """Validate and evaluate expression, return result or 'Error'."""
    if not SAFE_EXPR.match(expr):
        return 'Error'
    try:
        result = eval(expr, {'__builtins__': None}, {})
        return str(result)
    except:
        return 'Error'

def toggle_sign(expr: str) -> str:
    return expr[1:] if expr.startswith('-') else ('-' + expr if expr else expr)

def calc_percent(expr: str) -> str:
    try:
        return str(float(expr) / 100)
    except:
        return 'Error'
