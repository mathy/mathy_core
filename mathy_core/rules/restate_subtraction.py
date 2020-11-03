from typing import Optional

from ..expressions import (
    AddExpression,
    ConstantExpression,
    MathExpression,
    MultiplyExpression,
    NegateExpression,
    PowerExpression,
    SubtractExpression,
    VariableExpression,
)
from ..rule import BaseRule, ExpressionChangeRule


class RestateSubtractionRule(BaseRule):
    """Convert subtract operators to plus negative to allow commuting"""

    OP_SUBTRACTION = "subtraction"
    OP_ADD_NEG_CONST = "add_neg_const"
    OP_ADD_NEG_CONST_VAR = "add_neg_const_var"
    OP_ADD_NEG_CONST_VAR_EXP = "add_neg_const_var_exp"

    @property
    def name(self) -> str:
        return "Restate Subtraction"

    @property
    def code(self) -> str:
        return "RS"

    def get_type(self, node: MathExpression) -> Optional[str]:
        """Determine the configuration of the tree for this transformation.

        Support two types of tree configurations:
         - Subtraction is a subtract to be restate as a plus negation
         - PlusNegative is a plus negative const to be restated as subtraction
        """
        is_sub = isinstance(node, SubtractExpression)
        is_parent_add = isinstance(node.parent, AddExpression)
        # 4x - 2x
        if is_sub and (node.parent is None or is_parent_add):
            return RestateSubtractionRule.OP_SUBTRACTION
        # The other cases are addition and negative/negation
        is_add = isinstance(node, AddExpression)
        if not is_add:
            return None

        # + -2 = Const
        if node.right and isinstance(node.right, ConstantExpression):
            assert node.right.value is not None
            if node.right.value < 0.0:
                return RestateSubtractionRule.OP_ADD_NEG_CONST
            return None

        # + -2x = Mult(Const, Var)
        if (
            node.right
            and isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, ConstantExpression)
            and isinstance(node.right.right, VariableExpression)
        ):
            assert node.right.left.value is not None
            if node.right.left.value < 0.0:
                return RestateSubtractionRule.OP_ADD_NEG_CONST_VAR
            return None

        # + -2x^3 = Mult(Const, Exp(Var, Const))
        if (
            isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, ConstantExpression)
            and isinstance(node.right.right, PowerExpression)
        ):
            assert node.right.left.value is not None
            if node.right.left.value < 0.0:
                return RestateSubtractionRule.OP_ADD_NEG_CONST_VAR_EXP
            return None

        return None

    def can_apply_to(self, node: MathExpression) -> bool:
        tree_type = self.get_type(node)
        return tree_type is not None

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node)
        tree_type = self.get_type(node)
        assert tree_type is not None, "call can_apply_to before applying a rule"
        change.save_parent()  # connect result to node.parent
        result: MathExpression

        # Simple case of subtract to plus negate
        if tree_type == RestateSubtractionRule.OP_SUBTRACTION:
            result = AddExpression(node.left, NegateExpression(node.right))
        else:
            # Plus negative to subtract cases
            assert node.left is not None and node.right is not None
            result = SubtractExpression(node.left, node.right.clone())
            if tree_type == RestateSubtractionRule.OP_ADD_NEG_CONST:
                assert (
                    result.right is not None
                    and isinstance(result.right, ConstantExpression)
                    and result.right.value is not None
                )
                result.right.value = -result.right.value
            elif tree_type == RestateSubtractionRule.OP_ADD_NEG_CONST_VAR:
                assert (
                    result.right is not None
                    and isinstance(result.right.left, ConstantExpression)
                    and result.right.left.value is not None
                )
                result.right.left.value = -result.right.left.value
            elif tree_type == RestateSubtractionRule.OP_ADD_NEG_CONST_VAR_EXP:
                assert (
                    result.right is not None
                    and isinstance(result.right.left, ConstantExpression)
                    and result.right.left.value is not None
                )
                result.right.left.value = -result.right.left.value
        result.set_changed()  # mark this node as changed for visualization
        return change.done(result)
