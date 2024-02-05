from typing import Optional

from ..expressions import (
    ConstantExpression,
    DivideExpression,
    MathExpression,
    MultiplyExpression,
    NegateExpression,
)
from ..rule import BaseRule, ExpressionChangeRule

_OP_DIVISION_EXPRESSION = "division-expression"
_OP_DIVISION_NEGATIVE_DENOMINATOR = "division-negative-denominator"


class MultiplicativeInverseRule(BaseRule):
    """Convert division operations to multiplication by the reciprocal."""

    @property
    def name(self) -> str:
        return "Multiplicative Inverse"

    @property
    def code(self) -> str:
        return "MI"

    def get_type(self, node: MathExpression) -> Optional[str]:
        """Determine the configuration of the tree for this transformation.

        Support different types of tree configurations based on the division operation:
        - DivisionExpression is a division to be restated as multiplication by reciprocal
        - DivisionNegativeDenominator is a division by a negative term
        """
        is_division = isinstance(node, DivideExpression)
        if not is_division:
            return None

        # Division where the denominator is negative (e.g., (2 + 3z) / -z)
        if isinstance(node.right, NegateExpression):
            return _OP_DIVISION_NEGATIVE_DENOMINATOR

        # If none of the above, it's a general division expression
        return _OP_DIVISION_EXPRESSION

    def can_apply_to(self, node: MathExpression) -> bool:
        tree_type = self.get_type(node)
        return tree_type is not None

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node)
        tree_type = self.get_type(node)
        assert tree_type is not None, "call can_apply_to before applying a rule"
        change.save_parent()  # connect result to node.parent

        # Handle the division based on the tree type
        if tree_type == _OP_DIVISION_EXPRESSION:
            result = MultiplyExpression(
                node.left.clone(),
                DivideExpression(ConstantExpression(1), node.right.clone()),
            )

        elif tree_type == _OP_DIVISION_NEGATIVE_DENOMINATOR:
            # For division by a negative denominator, negate the numerator and use the positive reciprocal
            result = MultiplyExpression(
                node.left.clone(),
                DivideExpression(
                    ConstantExpression(-1), node.right.get_child().clone()
                ),
            )

        else:
            raise NotImplementedError(
                "Unsupported tree configuration for MultiplicativeInverseRule"
            )

        result.set_changed()  # mark this node as changed for visualization
        return change.done(result)
