# Legacy

This directory contains the _WFF_ parser `proposition_parser.py`, as well as the original relaxed parser developed during the extra classes. These are mostly useless and are only kept for archival purposes.

## Vocabulary

To make it easier to input proposition formulas, the following conventions will be used:

- A-Z : Propositional variables
- n : Negation
- a : Conjunction
- o : Disjunction
- i : Implication
- e : Equivalence
- (,) : Paranthesis

## Input / Output

Input and output is assumed to be done through the console, unless otherwise specified.

# Scripts

## `proposition_parser.py`

After introducing the proposition using the vocabulary described above, a menu will appear with multiple options.
For the examples bellow, I will be using the propositional formula `(((AaB)o(CaB))i(AeB))`

### 1. Display tree

Prints the Abstract Syntax Tree of the proposition, along with the identified atoms. Example:

```
i
-o
--a
---A
---B
--a
---C
---B
-e
--A
--B
The atoms are: {'B', 'A', 'C'}
```

### 2. Compute value for an interpretation

Asks the user to input values (`0` or `1`) for all the identified atoms, computes the truth value of the proposition along with the tree of values. Examples:

```
Computing value under interpretation: {'B': True, 'A': False, 'C': True}
The value is: False
The computation is shown below:
i: False
-o: True
--a: False
---A: False
---B: True
--a: True
---C: True
---B: True
-e: False
--A: False
--B: True
```

### 3. Generate truth table

Generates the truth table of the propositional formula and outputs it as `truth_table.csv` in the `res/` folder. Example converted to markdown table:

| A     | B     | C     | (AaB) | (CaB) | ((AaB)o(CaB)) | (AeB) | (((AaB)o(CaB))i(AeB)) |
| ----- | ----- | ----- | ----- | ----- | ------------- | ----- | --------------------- |
| False | False | False | False | False | False         | True  | True                  |
| False | False | True  | False | False | False         | True  | True                  |
| False | True  | False | False | False | False         | False | True                  |
| False | True  | True  | False | True  | True          | False | False                 |
| True  | False | False | False | False | False         | False | True                  |
| True  | False | True  | False | False | False         | False | True                  |
| True  | True  | False | True  | False | True          | True  | True                  |
| True  | True  | True  | True  | True  | True          | True  | True                  |
