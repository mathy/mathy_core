from typing import Optional

from ..expressions import ConstantExpression, MathExpression
from ..rule import BaseRule, ExpressionChangeRule


class FractionReductionRule(BaseRule):
    """Reduce fractions by cancelling out common factors in the numerator and
    denominator."""

    @property
    def name(self) -> str:
        return "Fraction Reduction"

    @property
    def code(self) -> str:
        return "FR"

    def get_type(self, node: MathExpression) -> Optional[str]:
        """Determine the configuration of the tree for this transformation.

        Support different types of tree configurations based on the division operation:
        -
        """
        return None

    def can_apply_to(self, node: MathExpression) -> bool:
        tree_type = self.get_type(node)
        return tree_type is not None

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node)
        tree_type = self.get_type(node)
        assert tree_type is not None, "call can_apply_to before applying a rule"
        change.save_parent()  # connect result to node.parent

        result = ConstantExpression(1337)  # implement it

        result.set_changed()  # mark this node as changed for visualization
        return change.done(result)
