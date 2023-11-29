from typing import List

import pytest

from mathy_core import TOKEN_TYPES, Token, Tokenizer


def test_tokenizer_tokenize() -> None:
    text = "4x + 2x^3 * 7!"
    tokenizer = Tokenizer()
    tokens: List[Token] = tokenizer.tokenize(text)

    for token in tokens:
        print(token)
        assert token.type <= TOKEN_TYPES.EOF
        assert token.value is not None


def test_tokenizer_errors() -> None:
    text = "4x + 2x^3 * 7\\"
    tokenizer = Tokenizer()

    with pytest.raises(ValueError):
        tokenizer.tokenize(text)


def test_tokenizer_manual_verification() -> None:
    """Simplest conceptual example verifying the tokenizer maps to
    expectations."""

    manual_tokens: List[Token] = [
        Token("4", TOKEN_TYPES.Constant),
        Token("x", TOKEN_TYPES.Variable),
        Token("+", TOKEN_TYPES.Plus),
        Token("2", TOKEN_TYPES.Constant),
        Token("", TOKEN_TYPES.EOF),
    ]
    auto_tokens: List[Token] = Tokenizer().tokenize("4x + 2")

    for i, token in enumerate(manual_tokens):
        assert auto_tokens[i].value == token.value
        assert auto_tokens[i].type == token.type


def test_tokenizer_identify_functions() -> None:
    """The tokenizer can deal with known function expressions"""
    tokens: List[Token] = Tokenizer().tokenize("sgn(-3)")
    assert tokens[0].type == TOKEN_TYPES.Function
    assert tokens[0].value == "sgn"


def test_tokenizer_ignore_padding() -> None:
    """When specified, the tokenizer will return tokens for padding characters
    to allow exact reproduction of the input string from its tokens."""
    text = "4x + 2y^7 - 6"
    # exclude_padding is True by default
    no_padding: List[Token] = Tokenizer().tokenize(text)
    # When including padding, spaces are preserved
    padding: List[Token] = Tokenizer(exclude_padding=False).tokenize(text)
    assert len(padding) == len(no_padding) + 4
