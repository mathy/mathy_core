import pytest

from mathy_core.parser import (
    ExpressionParser,
    InvalidExpression,
    InvalidSyntax,
    TrailingTokens,
    UnexpectedBehavior,
)


def test_parser_to_string() -> None:
    parser = ExpressionParser()
    expects = [
        {
            "input": "(-2.257893300159429e+16h^2 * v) * j^4",
            "output": "(-2.257893300159429e + 16h^2 * v) * j^4",
        },
        {"input": "1f + 98i + 3f + 14t", "output": "1f + 98i + 3f + 14t"},
        {"input": "4x * p^(1 + 3) * 12x^2", "output": "4x * p^(1 + 3) * 12x^2"},
        {"input": "(5 * 3) * (32 / 7)", "output": "(5 * 3) * 32 / 7"},
        {"input": "7 - 5 * 3 * (2^7)", "output": "7 - 5 * 3 * 2^7"},
        {"input": "(8x^2 * 9b) * 7", "output": "(8x^2 * 9b) * 7"},
        {"input": "(8 * 9b) * 7", "output": "(8 * 9b) * 7"},
        {"input": "7 - (5 * 3) * (32 / 7)", "output": "7 - (5 * 3) * 32 / 7"},
        {"input": "7 - (5 - 3) * (32 - 7)", "output": "7 - (5 - 3) * (32 - 7)"},
        {"input": "(7 - (5 * 3)) * (32 - 7)", "output": "(7 - 5 * 3) * (32 - 7)"},
    ]
    # Test to make sure parens are preserved in output when they are meaningful
    for expect in expects:
        expression = parser.parse(expect["input"])
        out_str = str(expression)
        assert out_str == expect["output"]


def test_parser_factorials() -> None:
    """should parse factorials"""
    parser = ExpressionParser()
    expression = parser.parse("5!")
    # 5! = 5 * 4 * 3 * 2 * 1 = 120
    assert expression.evaluate() == 120


def test_parser_operator_precedence() -> None:
    expects: list[dict[str, float | int | str]] = [
        {"input": "9 / 8 * 9", "output": 10.125},
        {"input": "4 + 9 / 8 * 9", "output": 14.125},
    ]
    for expect in expects:
        parser = ExpressionParser()
        expression = parser.parse(str(expect["input"]))
        assert expression.evaluate() == expect["output"]


def test_parser_mult_exp_precedence() -> None:
    """should respect order of operations with factor parsing"""
    parser = ExpressionParser()
    expression = parser.parse("4x^2")
    val = expression.evaluate({"x": 2})
    # 4x^2 should evaluate to 16 with x=2
    assert val == 16

    expression = parser.parse("7 * 10 * 6x * 3x + 5x")
    assert expression is not None


def test_parser_exceptions() -> None:
    parser = ExpressionParser()
    expectations = [
        ["1=5+-", InvalidSyntax, "parse_unary not expected"],
        ["x+4^-", InvalidSyntax, "parse_unary not expected"],
        ["4^4/.", ValueError, "parse_unary coerce_to_number"],
        ["4*/", InvalidSyntax, "parse_mult not expected"],
        ["4+3+3     3", TrailingTokens, "_parse trailing tokens check"],
        ["4^+", InvalidSyntax, "parse_exponent check unary"],
        ["4+", UnexpectedBehavior, "parse_add not expected and not right"],
        ["", InvalidExpression, "_parse initial next check"],
        ["4=+", UnexpectedBehavior, "parse_equal not expected"],
        ["+!", InvalidSyntax, "parse_equal first check"],
        ["=+", InvalidSyntax, "parse_equal first check"],
    ]
    for in_str, out_err, meta in expectations:
        with pytest.raises(out_err):
            parser.parse(in_str)
        assert meta != "", "add note about which parser fn throws for this case"
