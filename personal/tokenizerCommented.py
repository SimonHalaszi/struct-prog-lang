
# Import the regular expressions module (like <regex> in C++)
import re


# List of token patterns: each is a [regex, tag] pair
# The tag is a string describing the type of token (like an enum or string in C++)
patterns = [
    [r"print", "print"],  # the keyword 'print'
    [r"\d*\.\d+|\d+\.\d*|\d+", "number"],  # integer or float numbers
    [r"[a-zA-Z_][a-zA-Z0-9_]*", "identifier"],  # variable names (identifiers)
    [r"\+", "+"],  # plus
    [r"\-", "-"],  # minus
    [r"\*", "*"],  # multiply
    [r"\/", "/"],  # divide
    [r"\(", "("],  # left parenthesis
    [r"\)", ")"],  # right parenthesis
    [r"\s+", "whitespace"],  # whitespace (spaces, tabs, etc.)
    [r".", "error"]  # any other character is an error
]


# Compile all regex patterns for faster matching
for pattern in patterns:
    pattern[0] = re.compile(pattern[0])


# Tokenize a string into a list of tokens (like a lexer in C++)
def tokenize(characters):
    tokens = []  # List to store the tokens (like a vector of structs)
    position = 0  # Current position in the input string
    while position < len(characters):
        # Try each pattern in order
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break  # Found a match, stop checking other patterns
        assert match  # Should always match something (even if error)
        # If the tag is 'error', raise an exception
        if tag == "error":
            raise Exception("Syntax error")
        # Create a token as a Python dictionary (like a struct)
        token = {
            "tag": tag,  # The type of token (e.g., 'number', '+', etc.)
            "position": position,  # Where the token starts in the input
            "value": match.group(0)  # The actual text matched
        }
        # If the token is a number, convert its value to int or float
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
        # Ignore whitespace tokens (don't add them to the list)
        if token["tag"] != "whitespace":
            tokens.append(token)
        # Move position to the end of the matched text
        position = match.end()
    # Add an end-of-stream marker (like EOF)
    tokens.append({
        "tag": None,
        "value": None,
        "position": position
    })
    return tokens


# Test: single-character tokens
def test_simple_token():
    print("test simple token")
    examples = "+-*/()"
    for example in examples:
        t = tokenize(example)[0]
        assert t["tag"] == example
        assert t["position"] == 0
        assert t["value"] == example


# Test: integer and float numbers
def test_number_token():
    print("test number tokens")
    for s in ["1", "11"]:
        t = tokenize(s)
        assert len(t) == 2  # token + end marker
        assert t[0]["tag"] == "number"
        assert t[0]["value"] == int(s)
    for s in ["1.1", "11.11", "11.", ".11"]:
        t = tokenize(s)
        assert len(t) == 2
        assert t[0]["tag"] == "number"
        assert t[0]["value"] == float(s)



# Test: multiple tokens in a row
def test_multiple_tokens():
    print("test multiple tokens")
    tokens = tokenize("1+2")
    assert tokens == [
        {'tag': 'number', 'position': 0, 'value': 1},
        {'tag': '+', 'position': 1, 'value': '+'},
        {'tag': 'number', 'position': 2, 'value': 2},
        {'tag': None, 'value': None, 'position': 3}
    ]


# Test: whitespace is ignored
def test_whitespace():
    print("test whitespace...")
    tokens = tokenize("1 + 2")
    assert tokens == [
        {'tag': 'number', 'position': 0, 'value': 1},
        {'tag': '+', 'position': 2, 'value': '+'},
        {'tag': 'number', 'position': 4, 'value': 2},
        {'tag': None, 'value': None, 'position': 5}
    ]


# Test: keyword tokens (like 'print')
def test_keywords():
    print("test keywords...")
    for keyword in [
        "print",
    ]:
        t = tokenize(keyword)
        assert len(t) == 2
        assert t[0]["tag"] == keyword, f"expected {keyword}, got {t[0]}"
        # (Note: in this implementation, 'value' is present, but in some lexers it might not be)


# Test: variable names (identifiers)
def test_identifier_tokens():
    print("test identifier tokens...")
    for s in ["x", "y", "z", "alpha", "beta", "gamma"]:
        t = tokenize(s)
        assert len(t) == 2
        assert t[0]["tag"] == "identifier"
        assert t[0]["value"] == s




# Test: error handling for invalid characters
def test_error():
    print("test error")
    try:
        t = tokenize("$1+2")
        assert False, "Should have raised an error for an invalid character."
    except Exception as e:
        assert "Syntax error" in str(e), f"Unexpected exception: {e}"


# If this file is run directly, run all tests
if __name__ == "__main__":
    test_simple_token()
    test_number_token()
    test_multiple_tokens()
    test_whitespace()
    test_keywords()
    test_identifier_tokens()
    test_error()