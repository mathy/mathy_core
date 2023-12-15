```python

import mathy_core.parser
```
Mathy parses [token arrays](./tokenizer) into inspectable, transformable, visualizable symbolic trees.

## Motivation

A Token array verifies that text maps to some known symbols, not that they are a correct ordering that produces a valid mathematical expression. The mathy Parser class converts tokens into a tree while also validating that the tree follows the expected Order of Operations.

## Examples

To help better understand what the parser does, consider a few examples of expressions and their visualized trees:

| Text                  | Tree                        |
| --------------------- | --------------------------- |
| `4x`                  | `mathy:4x`                  |
| `4x / 2y^7`           | `mathy:4x/2y^7`             |
| `4x + (1/3)y + 7x`    | `mathy:4x+ (1/3)y + 7x`     |
| `4x + 1/3y + 7x`      | `mathy:4x+ 1/3y + 7x`       |
| `(28 + 1j)(17j + 2y)` | `mathy:(28 + 1j)(17j + 2y)` |


## API


## ExpressionParser
```python
ExpressionParser(self) -> None
```
Parser for converting text into binary trees. Trees encode the order of
operations for an input, and allow evaluating it to detemrine the expression
value.

### Grammar Rules

Symbols:
```
( )    == Non-terminal
{ }*   == 0 or more occurrences
{ }+   == 1 or more occurrences
{ }?   == 0 or 1 occurrences
[ ]    == Mandatory (1 must occur)
|      == logical OR
" "    == Terminal symbol (literal)
```

Non-terminals defined/parsed by Tokenizer:
```
(Constant) = anything that can be parsed by `float(in)`
(Variable) = any string containing only letters (a-z and A-Z)
```

Rules:
```
(Function)     = [ functionName ] "(" (AddExp) ")"
(Factor)       = { (Variable) | (Function) | "(" (AddExp) ")" }+ { { "^" }? (UnaryExp) }?
(FactorPrefix) = [ (Constant) { (Factor) }? | (Factor) ]
(UnaryExp)     = { "-" }? (FactorPrefix)
(ExpExp)       = (UnaryExp) { { "^" }? (UnaryExp) }?
(MultExp)      = (ExpExp) { { "*" | "/" }? (ExpExp) }*
(AddExp)       = (MultExp) { { "+" | "-" }? (MultExp) }*
(EqualExp)     = (AddExp) { { "=" }? (AddExp) }*
(start)        = (EqualExp)
```

### check
```python
ExpressionParser.check(
    self, 
    tokens: mathy_core.parser.TokenSet, 
    do_assert: bool = False, 
) -> bool
```
Check if the `self.current_token` is a member of a set Token types

Args:
    - `tokens` The set of Token types to check against

`Returns` True if the `current_token`'s type is in the set else False
### eat
```python
ExpressionParser.eat(self, type: int) -> bool
```
Assign the next token in the queue to current_token if its type
matches that of the specified parameter. If the type does not match,
raise a syntax exception.

Args:
    - `type` The type that your syntax expects @current_token to be

### next
```python
ExpressionParser.next(self) -> bool
```
Assign the next token in the queue to `self.current_token`.

Return True if there are still more tokens in the queue, or False if there
are no more tokens to look at.
### parse
```python
ExpressionParser.parse(
    self, 
    input_text: str, 
) -> mathy_core.expressions.MathExpression
```
Parse a string representation of an expression into a tree
that can be later evaluated.

Returns : The evaluatable expression tree.

## TokenSet
```python
TokenSet(self, source: int)
```
TokenSet objects are bitmask combinations for checking to see
if a token is part of a valid set.
### add
```python
TokenSet.add(self, addTokens: int) -> 'TokenSet'
```
Add tokens to self set and return a TokenSet representing
their combination of flags.  Value can be an integer or an instance
of `TokenSet`
### contains
```python
TokenSet.contains(self, type: int) -> bool
```
Returns true if the given type is part of this set
