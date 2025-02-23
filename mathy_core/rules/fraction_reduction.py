from typing import Optional

from ..expressions import DivideExpression, MathExpression
from ..rule import BaseRule, ExpressionChangeRule
from ..util import (
    FractionReductionResult,
    factor_fraction_terms_ex,
    get_term_ex,
    make_term_fractional,
)


class FractionReductionRule(BaseRule):
    """Reduce fractions by cancelling out common factors in the numerator and
    denominator."""

    @property
    def name(self) -> str:
        return "Fraction Reduction"

    @property
    def code(self) -> str:
        return "FR"

    def get_reduction_term(
        self, node: MathExpression
    ) -> Optional[FractionReductionResult]:
        is_division = isinstance(node, DivideExpression)
        if not is_division:
            return None
        left_term = get_term_ex(node.left)
        right_term = get_term_ex(node.right)
        if left_term is None or right_term is None:
            return None
        f = factor_fraction_terms_ex(left_term, right_term)
        if not f:
            return None
        return f

    def can_apply_to(self, node: MathExpression) -> bool:
        reduced_fraction_result = self.get_reduction_term(node)
        return reduced_fraction_result is not None

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node)
        reduced_fraction_result = self.get_reduction_term(node)
        assert (
            reduced_fraction_result is not None
        ), "call can_apply_to before applying a rule"

        change.save_parent()  # connect result to node.parent
        result = make_term_fractional(
            numerator=reduced_fraction_result.numerator,
            denominator=reduced_fraction_result.denominator,
            variable=reduced_fraction_result.reduced_variable,
            exponent=reduced_fraction_result.reduced_exponent,
        )
        result.set_changed()  # mark this node as changed for visualization
        return change.done(result)
