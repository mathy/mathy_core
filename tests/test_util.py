from mathy_core.parser import ExpressionParser
from mathy_core.util import (
    TermEx,
    get_sub_terms,
    get_term_ex,
    get_terms,
    has_like_terms,
    is_preferred_term_form,
    terms_are_like,
)


def test_util_get_sub_terms():
    expectations = [
        ["-f", 1],
        ["70656 * (x^2 * z^6)", 2],
        ["4x^2 * z^6 * y", 3],
        ["2x^2", 1],
        ["x^2", 1],
        ["2", 1],
    ]
    invalid_expectations = [
        # can't have more than one term
        ["4 + 4", False]
    ]
    parser = ExpressionParser()
    for text, output in expectations + invalid_expectations:
        exp = parser.parse(text)
        sub_terms = get_sub_terms(exp)
        if output is False:
            assert text == text and sub_terms == output
        else:
            assert isinstance(sub_terms, list)
            assert text == text and len(sub_terms) == output


def test_util_get_term_ex():
    examples = [
        ["-y", TermEx(-1, "y", None)],
        ["-x^3", TermEx(-1, "x", 3)],
        ["-2x^3", TermEx(-2, "x", 3)],
        ["4x^2", TermEx(4, "x", 2)],
        ["4x", TermEx(4, "x", None)],
        ["x", TermEx(None, "x", None)],
        # TODO: non-natural term forms? If this is supported we can drop the other
        #       get_term impl maybe?
        # ["x * 2", TermEx(2, "x", None)],
    ]
    parser = ExpressionParser()
    for input, expected in examples:
        expr = parser.parse(input)
        assert input == input and get_term_ex(expr) == expected


def test_util_is_preferred_term_form():
    examples = [
        ["b * (44b^2)", False],
        ["z * (1274z^2)", False],
        ["4x * z", True],
        ["z * 4x", True],
        ["2x * x", False],
        ["29y", True],
        ["z", True],
        ["z * 10", False],
        ["4x^2", True],
    ]
    parser = ExpressionParser()
    for input, expected in examples:
        expr = parser.parse(input)
        assert input == input and is_preferred_term_form(expr) == expected


def test_util_has_like_terms():
    examples = [
        ["14 + 6y + 7x + x * (3y)", False],
        ["b * (44b^2)", False],
        ["z * (1274z^2)", False],
        ["100y * x + 2", False],
    ]
    parser = ExpressionParser()
    for input, expected in examples:
        expr = parser.parse(input)
        assert input == input and has_like_terms(expr) == expected


def test_util_terms_are_like():
    parser = ExpressionParser()
    expr = parser.parse("10 + (7x + 6x)")
    terms = get_terms(expr)
    assert len(terms) == 3
    assert not terms_are_like(terms[0], terms[1])
    assert terms_are_like(terms[1], terms[2])

    expr = parser.parse("10 + 7x + 6")
    terms = get_terms(expr)
    assert len(terms) == 3
    assert not terms_are_like(terms[0], terms[1])
    assert terms_are_like(terms[0], terms[2])

    expr = parser.parse("6x + 6 * 5")
    terms = get_terms(expr)
    assert len(terms) == 2
    assert not terms_are_like(terms[0], terms[1])

    expr = parser.parse("360y^1")
    terms = get_terms(expr)
    assert len(terms) == 1

    expr = parser.parse("4z")
    terms = get_terms(expr)
    assert len(terms) == 1
