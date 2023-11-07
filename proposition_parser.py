vocab = "ABCDEFGHIJKLMNOPQRSTUVWXYZnaoie()"
operations = "naoie"

import os
import csv

class Node:
    def __init__(self, data):
        self.mid = ""
        self.left = ""
        self.right = ""
        self.atoms = set()
        self.truth = "UNCOMPUTED"

        #print("[Node init] Data:", data)

        # If node contains a complex formula
        if len(data) > 1:
            data = data[1:-1]
            # find the dominant operation
            dominant_operation = findDominantOperation(data)
            if dominant_operation == -1:
                self.mid = "ERROR"
            else:
                self.mid = data[dominant_operation]
                self.left = Node(data[:dominant_operation])
                for atom in self.left.atoms:
                    self.atoms.add(atom)
                self.right = Node(data[dominant_operation+1:])
                for atom in self.right.atoms:
                    self.atoms.add(atom)
        elif len(data) == 1:
            self.mid = data
            self.atoms.add(data)

def banner():
    print("""
The vocabulary of propositional logic
will be written as follows:
A-Z : Propositional variables
n   : Negation
a   : Conjunction
o   : Disjunction
i   : Implication
e   : Equivalence
(,) : Paranthesis

Please input your formula:""")

def menu():
    print("""
What do you want to do?
1 : Display tree
2 : Compute value for an interpretation
3 : Generate truth table
4 : Exit
>""", end="")

def validateVocabulary(text): 
    valid = True
    for char in text:
        if char not in vocab:
            valid = False
            break
    return valid

# deprecated
def findSequenceLength(text):
    #text_p = ""
    p = 0
    i = 0
    for char in text:
        if char == "(":
            p += 1
        elif char == ")":
            p -= 1
        #text_p += str(p)
        if p == 0:
            return i
        i += 1
    # print("[findSequenceLength] text_p:", text_p)

def findDominantOperation(text):
    text_depth = ""
    d = 0
    # compute the depth of the text at any char
    for char in text:
        if char == "(":
            d += 1
        elif char == ")":
            d -= 1
        text_depth += str(d)
    # find the operator at depth 0
    for i in range(len(text)):
        if text[i] in operations and text_depth[i] == "0":
            return i
    return -1

def printTree(node: Node, depth, mode):
    if mode == "value":
        print("-" * depth + node.mid)
    elif mode == "truth":
        print("-" * depth + node.mid + ": " + node.truth)
    if node.left:
        printTree(node.left, depth+1, mode)
    if node.right:
        printTree(node.right, depth+1, mode)

def printFlat(node: Node):
    atom = True
    if node.left or node.right:
        atom = False
    text = ""
    if not atom:
        text += "("
    if node.left:
        text += printFlat(node.left)
    text += node.mid
    if node.right:
        text += printFlat(node.right)
    if not atom:
        text += ")"
    return text

def getInterpretation(atoms: set):
    inter = dict()
    for atom in atoms:
        value = input(f"Introduce value for {atom}:")
        inter[atom] = bool(int(value))
    return inter

def getAllInterpretations(atoms: set):
    atoms = list(atoms)
    atoms.sort()
    l = len(atoms)
    possible_values = []
    interpretations = []
    for i in range(2**(l)):
        values = bin(i)[2:].rjust(l, "0")
        possible_values.append(values)
    
    for i in range(len(possible_values)):
        interpretation = dict()
        for j in range(len(atoms)):
            interpretation[atoms[j]] = bool(int(possible_values[i][j]))
        interpretations.append(interpretation)

    return(interpretations)  

def computeValue(node: Node, inter: dict, row: list):
    value = "ERROR"
    atom = False
    if node.mid in node.atoms:
        value = inter[node.mid]
        atom = True
    
    elif node.mid == "n":
        value = not computeValue(node.right, inter, row)
    
    elif node.mid == "a":
        left = computeValue(node.left, inter, row)
        right = computeValue(node.right,inter, row)
        value = left and right
    
    elif node.mid == "o":
        left = computeValue(node.left, inter, row)
        right = computeValue(node.right,inter, row)
        value = left or right 
    
    elif node.mid == "i":
        left = computeValue(node.left, inter, row)
        right = computeValue(node.right, inter, row)
        if left == False:
            value = True
        else:
            value = right
    
    elif node.mid == "e":
        value = computeValue(node.left, inter, row) == computeValue(node.right, inter, row)
    
    if not atom:
        segment = printFlat(node)
        row.append((segment, value))

    node.truth = str(value)
    return value
        
def computeUnderInterpretation(root: Node):
    # Get the interpretation
    inter = getInterpretation(root.atoms)
    print("Computing value under interpretation:",inter)

    # Compute the value under that interpretatin
    row = []
    value = computeValue(root, inter, row)
    print("The value is:", value)

    # Print proof
    print("The computation is shown below:")
    printTree(root, 0, "truth")

def computeAll(root: Node):
    interpretations = getAllInterpretations(root.atoms)
    header_printed = False
    rows = []
    for interpretation in interpretations:
        row = [(x, interpretation[x]) for x in interpretation]
        truth = computeValue(root, interpretation, row)
        #print(row)
        if not header_printed:
            header_row = [x[0] for x in row]
            rows.append(header_row)
            header_printed = True
        value_row = [x[1] for x in row]
        rows.append(value_row)
        #print("Value under interpretation", interpretation, "is", truth)
    if not os.path.exists("res"):
        os.makedirs("res")
    with open('res/truth_table.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print("Truth table printed to truth_table.csv")

def main():
    # Show banner (Vocab rules)
    banner()
    text = input()

    # Initial validation
    if validateVocabulary(text) == False:
        print("Invalid symbol used.")
        return
    
    # Form the abstract syntax tree
    # The Node class is self forming starting from a wff
    root = Node(text)

    while True:
        menu()
        choice = input().strip()
        if choice == "1":
            printTree(root, 0, "value")
            print("The atoms are:", root.atoms)
        elif choice == "2":
            computeUnderInterpretation(root)
        elif choice == "3":
            computeAll(root)
        elif choice == "4":
            break;
        else:
            print("Invalid choice.")

    print("Goodbye!")


if __name__ == "__main__":
    main()
