"""
Parses a relaxed syntax logical expression using the Shunting Yard Algorithm by Dijkstra.

The rules of the algorithm are the following:

1. A variable: 
    - Print it to output
2. A open paranthesis: 
    - Push onto stack
3. A closed paranthesis:
    - Discard the symbol
    - Print and discard everything from the stack until meeting an open paranthesis
    - That open paranthesis also gets discarded
4. A connective, when the stack is empty or the last element is an open paranthesis
    - Push onto stack
5. A connective, when the last element of the stack is a connective with LOWER priority
    - Push onto stack
6. A connective, when the last element of the stack is a connective with HIGHER priority
    - Print and discard every element from the stack until that condition is no longer met
    - Push onto stack

After going over all of the symbols of the expression, consume the stack, printing everything to the output.

These steps leave you with the representation of the original expression in Reverse Polish Notation.
This can then easily be parsed into an actual AST.
"""

# Used to get CLI arguments and to exit
import sys

# Used for colored output support
from colorama import init as colorama_init
from colorama import Fore, Style

debug = True

# RPN global variables
stack = []
output = []

# general global variables
vocabulary_connectives = "¬∧∨⇒⇔"
variables = []
vocabulary_connectives_priority = {
    "¬": 40,
    "∧": 30,
    "∨": 30,
    "⇒": 20,
    "⇔": 10
}

def stripColorama(data:str):
    data = data.replace(Fore.GREEN, "")
    data = data.replace(Fore.BLUE, "")
    data = data.replace(Fore.RED, "")
    data = data.replace(Style.RESET_ALL, "")
    return data

def pal(data:str):
    print(data)
    with open("logs/parser.log", "a", encoding="utf-8") as o:
        o.write(stripColorama(data) + "\n")

def log(data, channel:int):
    """Custom log function

    Args:
        data (str): Message
        channel (int): 0 = HUMAN, 1 = DEBUG, 2 = ERROR
    """
    msg = ""
    if(channel == 0):
        pal(f"{Fore.BLUE}[HUMAN]{Style.RESET_ALL} {data}")
    elif(channel == 1):
        if debug:
            pal(f"{Fore.GREEN}[DEBUG]{Style.RESET_ALL} {data}")
    elif(channel == 2):
        pal(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {data}")

def getPriority(symbol: str):
    return vocabulary_connectives_priority[symbol]

def isValidVariable(symbol: str):
    return symbol.isalnum() and symbol[0].isalpha()

def interpretSymbol(symbol: str):
    global output
    global stack
    
    # if symbol is a variable
    if isValidVariable(symbol):
        output.append(symbol)
        if symbol not in variables:
            variables.append(symbol)
            log(f"Identified variable: '{symbol}'",1)
    # open paranthesis
    elif symbol == "(":
        stack.append("(")
    # closed paranthesis
    elif symbol == ")":
        while(stack[-1] != "("):
            output.append(stack.pop())
        stack.pop()
    # connective
    elif symbol in vocabulary_connectives:
        if len(stack) == 0 or stack[-1] == "(":
            stack.append(symbol)
        elif getPriority(symbol) > getPriority(stack[-1]):
            stack.append(symbol)
        elif getPriority(symbol) <= getPriority(stack[-1]):
            while(len(stack) != 0 and stack[-1] != "("
                  and getPriority(symbol) <= getPriority(stack[-1])):
                output.append(stack.pop())
            stack.append(symbol)
    # invalid symbol
    else:
        raise Exception("Invalid symbol", symbol)
       
def consumeStack():
    """Consumes what's left on the stack, moving it to the output.
    """
    global output
    global stack
    while(len(stack) != 0):
        output += stack.pop()

def splitExpression(expression: str):
    """Splits a string representing a propositional logic expression into its symbols.

    Args:
        expression (str): String to proccess

    Returns:
        list: List of symbols
    """
    symbols = []
    buff = ""
    for c in expression:
        if c in "()" or c in vocabulary_connectives:
            if buff != "":
                symbols.append(buff)
                buff = ""
            symbols.append(c)
        else:
            buff += c
    # empty out buffer
    if buff != "":
        symbols.append(buff)
        buff = ""
    log("Input symbols: " + str(symbols), 1)
    return symbols

def expressionToRpn(symbols: list):
    global output
    for symbol in symbols:
        try:
            interpretSymbol(symbol)
        except Exception as e:
            highlight = ""
            for symbol in symbols:
                if symbol == e.args[1]:
                    highlight += f"{Fore.RED}{symbol}{Style.RESET_ALL}"
                else:
                    highlight += symbol
            log(f"Invalid symbol '{e.args[1]}': {highlight}. Aborting.", 2)
            sys.exit(1)
    consumeStack()
    log("Reverse Polish Notation: " + str(output), 1)
    log(f"The identified variables are {variables}",1)
    return output

def main():
    # Read expression from file
    f = open("input.txt", "r", encoding="utf-8")
    expression = f.readline()
    # Strip newline if present
    if expression[-1] == "\n":
        expression = expression[:-1]
    log(f"Parsing expression: {expression}", 0)

    # Split the expression into its symbols
    symbols = splitExpression(expression)

    # Parse the symbols into Reverse Polish Notation
    rpn = expressionToRpn(symbols)

    # Parse the Abstract Syntax Tree from the RPN

    

if __name__ == "__main__":
    # enable color support
    colorama_init()

    # check for debug flag
    if "debug" in sys.argv:
        debug = True

    # check that initialize was run
    initialized = True
    try:
        with open("logs/parser.log") as l:
            if l.read() != "":
                initialized = False
    except Exception:
        initialized = False
    if not initialized:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Data folder not initialized or already in use. Please run {Fore.YELLOW}initialize.py{Style.RESET_ALL} first.")
        sys.exit(1)

    # check that input is present
    input_ok = True
    try:
        with open("input.txt") as l:
            if l.read() == "":
                input_ok = False
    except Exception:
        input_ok = False
    if not input_ok:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Input file is empty or doesn't exist. Please create {Fore.YELLOW}input.txt{Style.RESET_ALL} first.")
        sys.exit(1)

    main()
