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

stack = []
output = ""

vocabulary_variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
vocabulary_connectives = "¬∧∨⇒⇔"

vocabulary_connectives_priority = {
    "¬": 40,
    "∧": 30,
    "∨": 30,
    "⇒": 20,
    "⇔": 10
}

def getPriority(symbol: str):
    return vocabulary_connectives_priority[symbol]

def interpret_symbol(symbol: str):
    global output
    global stack
    
    # if symbol is a variable
    if symbol in vocabulary_variables:
        output += symbol
    # open paranthesis
    elif symbol == "(":
        stack.append("(")
    # closed paranthesis
    elif symbol == ")":
        while(stack[-1] != "("):
            output += stack.pop()
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
                output += stack.pop()
            stack.append(symbol)
    # invalid symbol
    else:
        raise Exception("Invalid symbol")

        
def consume_stack():
    global output
    global stack
    while(len(stack) != 0):
        output += stack.pop()

def debug_print(symbol: str):
    global output
    global stack
    print("Symbol:", symbol, "\tStack:", stack, "\tOuput:", output)

def main():
    global output

    f = open("input.txt", "r", encoding="utf-8")
    expression = f.readline()

    expression_valid = True

    for symbol in expression:
        try:
            interpret_symbol(symbol)  
        except Exception as e:
            print("An error has occured:",e)
            expression_valid = False
            break
        debug_print(symbol)
    
    if expression_valid:
        consume_stack()
        print("The final output is:", output)

if __name__ == "__main__":
    main()
