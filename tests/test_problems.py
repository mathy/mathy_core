import random
from typing import List, Optional

from mathy_core import MathExpression
from mathy_core.parser import ExpressionParser
from mathy_core.problems import (
    gen_simplify_multiple_terms,
    rand_number,
    use_pretty_numbers,
)
from mathy_core.util import TermEx, get_term_ex, get_terms


def test_number_generation() -> None:
    random.seed(1337)

    # When using pretty number generation, all values
    # are in range 1-12 and are always integers
    use_pretty_numbers(True)
    pretty_numbers = [rand_number() for _ in range(256)]
    outside_range_floats = [f for f in pretty_numbers if f < 1 or f > 12]
    pretty_floats = [f for f in pretty_numbers if isinstance(f, float)]
    assert len(outside_range_floats) == 0
    assert len(pretty_floats) == 0

    # When not using pretty numbers, values can be floats and large integers
    use_pretty_numbers(False)
    rand_numbers = [rand_number() for _ in range(256)]
    large_ints = [f for f in rand_numbers if isinstance(f, int) and f > 12]
    rand_floats = [f for f in rand_numbers if isinstance(f, float)]
    assert len(large_ints) > 0
    assert len(rand_floats) > 0


def test_problems_variable_sharing_like_terms() -> None:
    """Verify that the polynomial generation functions return matches that include
    shared variables with different exponents, e.g. "4x + x^3 + 2x + 1.3x^3"
    """
    parser = ExpressionParser()
    problem, _ = gen_simplify_multiple_terms(
        3, share_var_probability=1.0, noise_probability=0.0, op="+"
    )
    expression: MathExpression = parser.parse(problem)
    term_nodes: List[MathExpression] = get_terms(expression)
    found_var: Optional[str] = None
    found_exp: bool = False
    for term_node in term_nodes:
        ex: Optional[TermEx] = get_term_ex(term_node)
        assert ex is not None, f"invalid expression {term_node}"
        if found_var is None:
            found_var = ex.variable
        assert found_var == ex.variable, "expected only one variable"
        if ex.exponent is not None:
            found_exp = True

    # Assert there are terms with and without exponents for this var
    assert found_var is not None
    assert found_exp is True


def test_problems_variable_sharing_unlike_terms() -> None:
    """Verify that the polynomial generation functions return matches that include
    shared variables for terms that are not like, e.g. "4x + x^3 + 2x"
    """
    parser = ExpressionParser()
    problem, _ = gen_simplify_multiple_terms(
        2, share_var_probability=1.0, noise_probability=0.0, op="+"
    )
    expression: MathExpression = parser.parse(problem)
    term_nodes: List[MathExpression] = get_terms(expression)
    found_var: Optional[str] = None
    found_exp: bool = False
    for term_node in term_nodes:
        ex: Optional[TermEx] = get_term_ex(term_node)
        assert ex is not None, f"invalid expression {term_node}"
        if found_var is None:
            found_var = ex.variable
        assert found_var == ex.variable, "expected only one variable"
        if ex.exponent is not None:
            found_exp = True

    # Assert there are terms with and without exponents for this var
    assert found_var is not None
    assert found_exp is True


def test_problems_noise_grouping_terms() -> None:
    """Verify that the polynomial generation functions return matches that include
    non-standard grouping of terms, in order to force the agents to commute different
    tree configurations, rather than relying on say always commuting the 3rd node.

    Standard grouping is: "4x + x^3 + 2x + 7y"
    Grouped first two terms: "(4x + x^3) + 2x + 7y"
    Grouped second and third terms: "4x + (x^3 + 2x) + 7y"
    """
    for _ in range(100):
        problem, _ = gen_simplify_multiple_terms(6, grouping_noise_probability=1.0)
        assert "(" in problem and ")" in problem
