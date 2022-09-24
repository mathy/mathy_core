from typing import Callable, Dict, List, Optional, Type

from .expressions import FunctionExpression, SgnExpression
from .types import NumberType


# Define the known types of tokens for the Tokenizer.
class TOKEN_TYPES:
    Constant: int = 1 << 0
    Variable: int = 1 << 1
    Plus: int = 1 << 2
    Minus: int = 1 << 3
    Multiply: int = 1 << 4
    Divide: int = 1 << 5
    Exponent: int = 1 << 6
    Factorial: int = 1 << 7
    OpenParen: int = 1 << 8
    CloseParen: int = 1 << 9
    Function: int = 1 << 10
    Equal: int = 1 << 11
    Pad: int = 1 << 12
    EOF: int = 1 << 13
    Invalid: int = 1 << 14


class Token:
    value: str
    type: int

    def __init__(self, value: str, type: int):
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return f'(type={self.type}, value="{self.value}")'


class TokenContext:
    tokens: List[Token]
    index: int
    buffer: str
    chunk: str

    def __init__(
        self,
        *,
        tokens: Optional[List[Token]] = None,
        index: int = 0,
        buffer: str = "",
        chunk: str = "",
    ):
        self.tokens = tokens if tokens is not None else []
        self.index = index
        self.buffer = buffer
        self.chunk = chunk


class Tokenizer:
    """The Tokenizer produces a list of tokens from an input string."""

    exclude_padding: bool
    functions: Dict[str, Type[FunctionExpression]]

    def __init__(self, exclude_padding: bool = True):
        self.exclude_padding = exclude_padding
        self.functions = {"sgn": SgnExpression}

    def is_alpha(self, c: str) -> bool:
        """Is this character a letter"""
        return ("a" <= c and c <= "z") or ("A" <= c and c <= "Z")

    def is_number(self, c: str) -> bool:
        """Is this character a number"""
        return "." == c or ("0" <= c and c <= "9")

    def eat_token(self, context: TokenContext, typeFn: Callable[[str], bool]) -> str:
        """Eat all of the tokens of a given type from the front of the stream
        until a different type is hit, and return the text."""
        res = ""
        for ch in list(context.chunk):
            if not typeFn(ch):
                return res
            res = res + str(ch)

        return res

    def tokenize(self, buffer: str) -> List[Token]:
        """Return an array of `Token`s from a given string input.
        This throws an exception if an unknown token type is found in the input."""
        context = TokenContext(buffer=buffer, chunk=str(buffer))
        while context.chunk and (
            self.identify_constants(context)
            or self.identify_alphas(context)
            or self.identify_operators(context)
        ):
            context.chunk = context.buffer[context.index :]  # noqa

        context.tokens.append(Token("", TOKEN_TYPES.EOF))
        return context.tokens

    def identify_operators(self, context: TokenContext) -> bool:
        """Identify and tokenize operators."""
        ch = context.chunk[0]
        if ch == " " or ch == "\t" or ch == "\r" or ch == "\n":
            # NOTE: originally introduced this to include padding for token prediction
            if self.exclude_padding is False:
                context.tokens.append(Token(ch, TOKEN_TYPES.Pad))
        elif ch == "+":
            context.tokens.append(Token("+", TOKEN_TYPES.Plus))
        elif ch == "-" or ch == "–":
            context.tokens.append(Token("-", TOKEN_TYPES.Minus))
        elif ch == "*":
            context.tokens.append(Token("*", TOKEN_TYPES.Multiply))
        elif ch == "/":
            context.tokens.append(Token("/", TOKEN_TYPES.Divide))
        elif ch == "^":
            context.tokens.append(Token("^", TOKEN_TYPES.Exponent))
        elif ch == "!":
            context.tokens.append(Token("!", TOKEN_TYPES.Factorial))
        elif ch == "(" or ch == "[":
            context.tokens.append(Token("(", TOKEN_TYPES.OpenParen))
        elif ch == ")" or ch == "]":
            context.tokens.append(Token(")", TOKEN_TYPES.CloseParen))
        elif ch == "=":
            context.tokens.append(Token("=", TOKEN_TYPES.Equal))
        else:
            raise ValueError(f'Invalid token "{ch}" in expression: {context.buffer}')
        context.index = context.index + 1
        return True

    def identify_alphas(self, context: TokenContext) -> int:
        """Identify and tokenize functions and variables."""
        if not self.is_alpha(context.chunk[0]):
            return False

        variable = self.eat_token(context, self.is_alpha)
        if variable in self.functions:
            context.tokens.append(Token(variable, TOKEN_TYPES.Function))
        else:
            # Each letter is its own variable
            for c in variable:
                context.tokens.append(Token(c, TOKEN_TYPES.Variable))

        context.index += len(variable)
        return len(variable)

    def identify_constants(self, context: TokenContext) -> int:
        """Identify and tokenize a constant number."""
        if not self.is_number(context.chunk[0]):
            return 0

        val = self.eat_token(context, self.is_number)
        context.tokens.append(Token(val, TOKEN_TYPES.Constant))
        context.index += len(val)
        return len(val)


def coerce_to_number(value: str) -> NumberType:
    return float(value) if "e" in value or "." in value else int(value)


__all__ = ("TOKEN_TYPES", "Token", "TokenContext", "Tokenizer", "coerce_to_number")
