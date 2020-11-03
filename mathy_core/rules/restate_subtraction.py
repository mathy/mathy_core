from typing import Optional

from ..expressions import (
    AddExpression,
    ConstantExpression,
    MultiplyExpression,
    NegateExpression,
    PowerExpression,
    SubtractExpression,
    VariableExpression,
)
from ..rule import BaseRule


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

    def get_type(self, node) -> Optional[str]:
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
        if isinstance(node.right, ConstantExpression):
            if node.right.value < 0.0:
                return RestateSubtractionRule.OP_ADD_NEG_CONST
            return None

        # + -2x = Mult(Const, Var)
        if (
            isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, ConstantExpression)
            and isinstance(node.right.right, VariableExpression)
        ):
            if node.right.left.value < 0.0:
                return RestateSubtractionRule.OP_ADD_NEG_CONST_VAR
            return None

        # + -2x^3 = Mult(Const, Exp(Var, Const))
        if (
            isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, ConstantExpression)
            and isinstance(node.right.right, PowerExpression)
        ):
            if node.right.left.value < 0.0:
                return RestateSubtractionRule.OP_ADD_NEG_CONST_VAR_EXP
            return None

        return None

    def can_apply_to(self, node) -> bool:
        tree_type = self.get_type(node)
        return tree_type is not None

    def apply_to(self, node):
        change = super().apply_to(node)
        tree_type = self.get_type(node)
        assert tree_type is not None, "call can_apply_to before applying a rule"
        change.save_parent()  # connect result to node.parent

        # Simple case of subtract to plus negate
        if tree_type == RestateSubtractionRule.OP_SUBTRACTION:
            result = AddExpression(node.left, NegateExpression(node.right))
        else:
            # Plus negative to subtract cases
            result = SubtractExpression(node.left, node.right.clone())
            if tree_type == RestateSubtractionRule.OP_ADD_NEG_CONST:
                assert isinstance(result.right, ConstantExpression)
                result.right.value = -result.right.value
            elif tree_type == RestateSubtractionRule.OP_ADD_NEG_CONST_VAR:
                assert isinstance(result.right.left, ConstantExpression)
                result.right.left.value = -result.right.left.value
            elif tree_type == RestateSubtractionRule.OP_ADD_NEG_CONST_VAR_EXP:
                assert isinstance(result.right.left, ConstantExpression)
                result.right.left.value = -result.right.left.value
        result.set_changed()  # mark this node as changed for visualization
        return change.done(result)
