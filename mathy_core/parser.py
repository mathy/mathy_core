from typing import Dict, List, Optional

from .expressions import (
    AddExpression,
    ConstantExpression,
    DivideExpression,
    EqualExpression,
    FactorialExpression,
    MathExpression,
    MultiplyExpression,
    NegateExpression,
    PowerExpression,
    SubtractExpression,
    VariableExpression,
)
from .tokenizer import TOKEN_TYPES, Token, Tokenizer, coerce_to_number
from .types import NumberType


class ParserException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


class InvalidExpression(ParserException):
    pass


class OutOfTokens(ParserException):
    pass


class InvalidSyntax(ParserException):
    pass


class UnexpectedBehavior(ParserException):
    pass


class TrailingTokens(ParserException):
    pass


class TokenSet:
    """TokenSet objects are bitmask combinations for checking to see
    if a token is part of a valid set."""

    tokens: int

    def __init__(self, source: int):
        self.tokens = source

    def add(self, addTokens: int) -> "TokenSet":
        """Add tokens to self set and return a TokenSet representing
        their combination of flags.  Value can be an integer or an instance
        of `TokenSet`"""
        return TokenSet(self.tokens | addTokens)

    def contains(self, type: int) -> bool:
        """Returns true if the given type is part of this set"""
        return (self.tokens & type) != 0


_FIRST_FUNCTION: TokenSet = TokenSet(TOKEN_TYPES.Function)
_FIRST_FACTOR: TokenSet = _FIRST_FUNCTION.add(
    TOKEN_TYPES.Variable | TOKEN_TYPES.OpenParen | TOKEN_TYPES.Factorial
)
_FIRST_FACTOR_PREFIX: TokenSet = _FIRST_FACTOR.add(TOKEN_TYPES.Constant)
_FIRST_UNARY: TokenSet = _FIRST_FACTOR_PREFIX.add(TOKEN_TYPES.Minus)
_FIRST_EXP: TokenSet = _FIRST_UNARY
_FIRST_MULT: TokenSet = _FIRST_UNARY
_FIRST_ADD: TokenSet = _FIRST_UNARY


# Precedence checks
_IS_ADD: TokenSet = TokenSet(TOKEN_TYPES.Plus | TOKEN_TYPES.Minus)
_IS_MULT: TokenSet = TokenSet(TOKEN_TYPES.Multiply | TOKEN_TYPES.Divide)
_IS_EXP: TokenSet = TokenSet(TOKEN_TYPES.Exponent)
_IS_EQUAL: TokenSet = TokenSet(TOKEN_TYPES.Equal)


class ExpressionParser:
    """Parser for converting text into binary trees. Trees encode the order of
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
    """  # noqa

    _parse_cache: Dict[str, MathExpression]
    _tokens_cache: Dict[str, List[Token]]
    _all_tokens: Optional[List[Token]]

    tokenizer: Tokenizer
    current_token: Token

    # Initialize the tokenizer.
    def __init__(self) -> None:
        self.tokenizer = Tokenizer()
        self.clear_cache()

    def clear_cache(self) -> None:
        self._tokens_cache = {}
        self._parse_cache = {}

    def tokenize(self, input_text: str) -> List[Token]:
        if input_text not in self._tokens_cache:
            self._tokens_cache[input_text] = self.tokenizer.tokenize(input_text)
        return self._tokens_cache[input_text][:]

    def parse(self, input_text: str) -> MathExpression:
        """Parse a string representation of an expression into a tree
        that can be later evaluated.

        Returns : The evaluatable expression tree.
        """
        if input_text in self._parse_cache:
            return self._parse_cache[input_text]
        self._parse_cache[input_text] = self._parse(self.tokenize(input_text))
        return self._parse_cache[input_text]

    def _parse(self, tokens: List[Token]) -> MathExpression:
        """Parse a given list of tokens into an expression tree"""
        self.tokens = tokens
        self._all_tokens = tokens[:]
        self.current_token = Token("", TOKEN_TYPES.Invalid)
        if not self.next():
            raise InvalidExpression("Cannot parse an empty function")

        expression: MathExpression = self.parse_equal()
        leftover = ""
        while self.current_token.type != TOKEN_TYPES.EOF:
            leftover = f"{leftover}{self.current_token.value}"
            self.next()

        if leftover != "":
            raise TrailingTokens("Trailing characters: {}".format(leftover))
        self._all_tokens = None
        return expression

    def parse_equal(self) -> MathExpression:
        self.check(_FIRST_ADD, True)

        exp = self.parse_add()
        while self.check(_IS_EQUAL):
            opType = self.current_token.type
            self.eat(opType)
            expected = self.check(_FIRST_ADD)
            right = None
            if expected:
                right = self.parse_add()

            if not expected or not right:
                raise UnexpectedBehavior(
                    "Expected an expression after = operator, got: {}".format(
                        self.current_token.value
                    )
                )
            exp = EqualExpression(exp, right)

        return exp

    def parse_add(self) -> MathExpression:
        self.check(_FIRST_MULT, True)

        exp = self.parse_mult()
        while self.check(_IS_ADD):
            opType = self.current_token.type
            opValue = self.current_token.value
            self.eat(opType)
            expected = self.check(_FIRST_MULT)
            right = None
            if expected:
                right = self.parse_mult()

            if not expected or not right:
                raise UnexpectedBehavior(
                    "Expected an expression after + or - operator, got: {}".format(
                        self.current_token.value
                    )
                )

            if opType == TOKEN_TYPES.Plus:
                exp = AddExpression(exp, right)
            elif opType == TOKEN_TYPES.Minus:
                exp = SubtractExpression(exp, right)
            else:  # pragma: nocover
                raise UnexpectedBehavior(
                    "Expected plus or minus, got: {}".format(opValue)
                )

        return exp

    def parse_mult(self) -> MathExpression:
        self.check(_FIRST_EXP, True)
        exp = self.parse_exponent()
        while self.check(_IS_MULT):
            opType = self.current_token.type
            opValue = self.current_token.value
            self.eat(opType)
            expected = self.check(_FIRST_EXP)
            right = None
            if expected:
                right = self.parse_mult()

            if not expected or right is None:
                assert self._all_tokens is not None
                input_str = "".join([str(f.value) for f in self._all_tokens])
                raise InvalidSyntax(
                    f"Expected an expression after * or / operator, got: {opValue}"
                    f"\nFull input: {input_str}"
                )

            if opType == TOKEN_TYPES.Multiply:
                exp = MultiplyExpression(exp, right)
            elif opType == TOKEN_TYPES.Divide:
                exp = DivideExpression(exp, right)
            else:  # pragma: nocover
                raise UnexpectedBehavior(
                    "Expected mult or divide, got: {}".format(opValue)
                )
        return exp

    def parse_exponent(self) -> MathExpression:
        self.check(_FIRST_UNARY, True)
        exp = self.parse_unary()
        if self.check(_IS_EXP):
            opType = self.current_token.type
            self.eat(opType)
            if not self.check(_FIRST_UNARY):
                raise InvalidSyntax("Expected an expression after ^ operator")

            right = self.parse_unary()
            if opType == TOKEN_TYPES.Exponent:
                exp = PowerExpression(exp, right)
            else:  # pragma: nocover
                raise UnexpectedBehavior("Expected exponent, got: {}".format(opType))
        return exp

    def parse_unary(self) -> MathExpression:
        value: NumberType = 0
        negate = False
        if self.current_token.type == TOKEN_TYPES.Minus:
            self.eat(TOKEN_TYPES.Minus)
            negate = True
        expected = self.check(_FIRST_FACTOR_PREFIX)
        exp: Optional[MathExpression] = None
        if expected:
            if self.current_token.type == TOKEN_TYPES.Constant:
                value = coerce_to_number(self.current_token.value)
                # Flip parse as float/int based on whether the value text
                if negate:
                    value = -value
                    negate = False

                exp = ConstantExpression(value)
                self.eat(TOKEN_TYPES.Constant)

            if self.check(_FIRST_FACTOR):
                if exp is None:
                    exp = self.parse_factors()
                elif self.current_token.type == TOKEN_TYPES.Factorial:
                    self.eat(TOKEN_TYPES.Factorial)
                    exp = FactorialExpression(exp)
                else:
                    exp = MultiplyExpression(exp, self.parse_factors())

        if not expected or exp is None:
            assert self._all_tokens is not None
            input_str = "".join([str(f.value) for f in self._all_tokens])
            raise InvalidSyntax(
                "Expected a function/variable/parenthesis after - or + \n"
                f"Received : {self.current_token.value}\n"
                f"Full Input : {input_str}\n"
            )
        if negate:
            return NegateExpression(exp)

        return exp

    def parse_factors(self) -> MathExpression:
        right = None
        found = True
        factors: List[MathExpression] = []
        while found:
            right = None
            opType = self.current_token.type
            if opType == TOKEN_TYPES.Variable:
                factors.append(VariableExpression(str(self.current_token.value)))
                self.eat(TOKEN_TYPES.Variable)
            elif opType == TOKEN_TYPES.Function:
                factors.append(self.parse_function())
            elif opType == TOKEN_TYPES.OpenParen:
                self.eat(TOKEN_TYPES.OpenParen)
                factors.append(self.parse_add())
                self.eat(TOKEN_TYPES.CloseParen)
            else:  # pragma: nocover
                raise UnexpectedBehavior(
                    "Unexpected token in Factor: {}".format(self.current_token.value)
                )

            found = self.check(_FIRST_FACTOR)

        if len(factors) == 0:
            raise InvalidExpression("No factors")

        exp: Optional[MathExpression] = None
        if self.check(_IS_EXP):
            opType = self.current_token.type
            self.eat(opType)
            if not self.check(_FIRST_UNARY):
                raise InvalidSyntax("Expected an expression after ^ operator")

            right = self.parse_unary()
            exp = PowerExpression(factors[-1], right)

        if len(factors) == 1:
            return exp or factors[0]

        while len(factors) > 0:
            if exp is None:
                exp = factors.pop(0)

            exp = MultiplyExpression(exp, factors.pop(0))

        assert exp is not None
        return exp

    def parse_function(self) -> MathExpression:
        opFn = str(self.current_token.value)
        self.eat(self.current_token.type)
        self.eat(TOKEN_TYPES.OpenParen)
        exp = self.parse_add()
        self.eat(TOKEN_TYPES.CloseParen)
        func = self.tokenizer.functions[opFn]
        if func is None:
            raise UnexpectedBehavior("Unknown Function type: {}".format(opFn))

        return func(exp)

    def next(self) -> bool:
        """Assign the next token in the queue to `self.current_token`.

        Return True if there are still more tokens in the queue, or False if there
        are no more tokens to look at."""

        if self.current_token.type == TOKEN_TYPES.EOF:
            raise OutOfTokens("Parsed beyond the end of the expression")

        self.current_token = self.tokens.pop(0)
        return self.current_token.type != TOKEN_TYPES.EOF

    def eat(self, type: int) -> bool:
        """Assign the next token in the queue to current_token if its type
        matches that of the specified parameter. If the type does not match,
        raise a syntax exception.

        Args:
            - `type` The type that your syntax expects @current_token to be
        """
        if self.current_token.type != type:
            raise InvalidSyntax("Missing: {}".format(type))

        return self.next()

    def check(self, tokens: TokenSet, do_assert: bool = False) -> bool:
        """Check if the `self.current_token` is a member of a set Token types

        Args:
            - `tokens` The set of Token types to check against

        `Returns` True if the `current_token`'s type is in the set else False"""

        result = tokens.contains(self.current_token.type)
        if do_assert is True and result is False:
            raise InvalidSyntax("Invalid expression")
        return result


__all__ = (
    "ParserException",
    "InvalidExpression",
    "OutOfTokens",
    "InvalidSyntax",
    "UnexpectedBehavior",
    "UnexpectedBehavior",
    "TrailingTokens",
    "TokenSet",
    "ExpressionParser",
)
