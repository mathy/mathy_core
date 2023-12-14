## Motivation

We first need an intermediate representation to parse math text into tree structures that encode the Order of Operations of the input. Specifically, we want to build a list of text characters corresponding to relevant `tokens` for a math expression. That is what the tokenizer does.

The tokenization process treats the input string as an array of characters, iterating over them to produce a list of tokens with `type`/`value` properties. While building the collection, the tokenizer also optionally discards extra whitespace characters.

## Visual Example

For example, consider the input text `8 - (2 + 4)` and its token representation.

`tokens:8 - (2 + 4)`

- The top row contains the token value.
- The bottom row includes the integer type of the token represented by the value.

## Code Example

Simple tokenization only requires a few lines of code:

```Python

{!./snippets/cas/tokenizer_tokenize.py!}

```

## Conceptual Example

To better understand the tokenizer, let's build a tokens array manually then compare it to the tokenizer outputs:

```Python
{!./snippets/cas/tokenizer_manual.py!}
```

# API

```python

import mathy_core.tokenizer
```




## TOKEN_TYPES

```python

TOKEN_TYPES(self, args, kwargs)

```



### CloseParen

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Constant

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Divide

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### EOF

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Equal

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Exponent

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Factorial

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Function

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Invalid

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Minus

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Multiply

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### OpenParen

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Pad

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Plus

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

### Variable

int([x]) -> integer

int(x, base=10) -> integer



Convert a number or string to an integer, or return 0 if no arguments

are given.  If x is a number, return x.__int__().  For floating point

numbers, this truncates towards zero.



If x is not a number or if base is given, then x must be a string,

bytes, or bytearray instance representing an integer literal in the

given base.  The literal can be preceded by '+' or '-' and be surrounded

by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.

Base 0 means to interpret the base from the string as an integer literal.

>>> int('0b100', base=0)

4

## Tokenizer

```python

Tokenizer(self, exclude_padding: bool = True)

```

The Tokenizer produces a list of tokens from an input string.

### eat_token

```python

Tokenizer.eat_token(

    self, 

    context: mathy_core.tokenizer.TokenContext, 

    typeFn: Callable[[str], bool], 

) -> str

```

Eat all of the tokens of a given type from the front of the stream

until a different type is hit, and return the text.

### identify_alphas

```python

Tokenizer.identify_alphas(

    self, 

    context: mathy_core.tokenizer.TokenContext, 

) -> int

```

Identify and tokenize functions and variables.

### identify_constants

```python

Tokenizer.identify_constants(

    self, 

    context: mathy_core.tokenizer.TokenContext, 

) -> int

```

Identify and tokenize a constant number.

### identify_operators

```python

Tokenizer.identify_operators(

    self, 

    context: mathy_core.tokenizer.TokenContext, 

) -> bool

```

Identify and tokenize operators.

### is_alpha

```python

Tokenizer.is_alpha(self, c: str) -> bool

```

Is this character a letter

### is_number

```python

Tokenizer.is_number(self, c: str) -> bool

```

Is this character a number

### tokenize

```python

Tokenizer.tokenize(self, buffer: str) -> List[mathy_core.tokenizer.Token]

```

Return an array of `Token`s from a given string input.

This throws an exception if an unknown token type is found in the input.
