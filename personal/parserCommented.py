
# Import the tokenize function from tokenizerCommented.py in the same directory
from personal.tokenizerCommented import tokenize


# parser.py -- implement parser for simple expressions
#
# Accept a string of tokens, return an AST (Abstract Syntax Tree) expressed as nested dictionaries (Python's version of a map or struct)


# Grammar rules (in EBNF-like notation):
#   factor = <number> | <identifier> | "(" expression ")"
#   term = factor { "*"|"/" factor }
#   expression = term { "+"|"-" term }
#   statement = <print> expression | expression


# Parse a 'factor' (number or parenthesized expression)
def parse_factor(tokens):
    """
    factor = <number> | "(" expression ")"
    tokens: a list of token dictionaries (like an array of structs in C++)
    Returns: (AST node, remaining tokens)
    """
    token = tokens[0]  # Get the first token
    if token["tag"] == "number":
        # If the token is a number, return an AST node representing the number
        return {
            "tag": "number",  # Node type
            "value": token["value"]  # The actual number value
        }, tokens[1:]  # Return the node and the rest of the tokens
    if token["tag"] == "(":
        # If the token is '(', parse the expression inside the parentheses
        ast, tokens = parse_expression(tokens[1:])  # Parse after '('
        assert tokens[0]["tag"] == ")"  # Ensure closing ')'
        return ast, tokens[1:]  # Return the AST and tokens after ')'
    # If not a number or '(', it's an error
    raise Exception(f"Unexpected token '{token['tag']}' at position {token['position']}.")


# Unit test for parse_factor
def test_parse_factor():
    """
    Test parsing numbers and parenthesized expressions
    """
    print("testing parse_factor()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        assert ast == {'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None  # End of input
    for s in ["(1)", "(22)"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        s_n = s.replace("(", "").replace(")", "")
        assert ast == {'tag': 'number', 'value': int(s_n)}
        assert tokens[0]['tag'] == None
    tokens = tokenize("(2+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}


# Parse a 'term' (handles multiplication and division)
def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    Handles left-to-right associativity for * and /
    """
    node, tokens = parse_factor(tokens)  # Parse the first factor
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]  # Operator: '*' or '/'
        right_node, tokens = parse_factor(tokens[1:])  # Parse the next factor
        # Build a new AST node for the operation
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens  # Return the AST and remaining tokens


# Unit test for parse_term
def test_parse_term():
    """
    Test parsing multiplication and division
    """
    print("testing parse_term()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_term(tokens)
        assert ast == {'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None
    tokens = tokenize("2*4")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}
    tokens = tokenize("2*4/6")
    ast, tokens = parse_term(tokens)
    assert ast == {'tag': '/', 'left': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 6}}


# Parse an 'expression' (handles addition and subtraction)
def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    Handles left-to-right associativity for + and -
    """
    node, tokens = parse_term(tokens)  # Parse the first term
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]  # Operator: '+' or '-'
        right_node, tokens = parse_term(tokens[1:])  # Parse the next term
        # Build a new AST node for the operation
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens  # Return the AST and remaining tokens


# Unit test for parse_expression
def test_parse_expression():
    """
    Test parsing addition and subtraction, including operator precedence
    """
    print("testing parse_expression()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_expression(tokens)
        assert ast == {'tag': 'number', 'value': int(s)}
        assert tokens[0]['tag'] == None
    tokens = tokenize("2*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}
    tokens = tokenize("1+2*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}}
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_expression(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}, 'right': {'tag': 'number', 'value': 4}}}


# Parse a 'statement' (either a print statement or an expression)
def parse_statement(tokens):
    """
    statement = <print> expression | expression
    Handles print statements and plain expressions
    """
    if tokens[0]["tag"] == "print":
        # If the first token is 'print', parse the following expression
        value_ast, tokens = parse_expression(tokens[1:])
        ast = {
            'tag': 'print',
            'value': value_ast
        }
    else:
        # Otherwise, just parse an expression
        ast, tokens = parse_expression(tokens)
    return ast, tokens


# Unit test for parse_statement
def test_parse_statement():
    """
    Test parsing statements (print and expressions)
    """
    print("testing parse_statement()")
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_statement(tokens)
    assert ast == {'tag': '+', 'left': {'tag': 'number', 'value': 1}, 'right': {'tag': '*', 'left': {'tag': '+', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 3}}, 'right': {'tag': 'number', 'value': 4}}}
    tokens = tokenize("print 2*4")
    ast, tokens = parse_statement(tokens)
    assert ast == {'tag': 'print', 'value': {'tag': '*', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}}



# Entry point: parse a list of tokens into an AST
def parse(tokens):
    ast, tokens = parse_statement(tokens)
    return ast


# If this file is run directly, run all tests
if __name__ == "__main__":
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse_statement()
    print("done.")
