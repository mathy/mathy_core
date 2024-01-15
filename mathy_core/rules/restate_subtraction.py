from typing import Optional, cast

from ..expressions import (
    AddExpression,
    ConstantExpression,
    EqualExpression,
    MathExpression,
    MultiplyExpression,
    NegateExpression,
    PowerExpression,
    SubtractExpression,
    VariableExpression,
)
from ..rule import BaseRule, ExpressionChangeRule

_OP_SUBTRACTION = "subtraction"
_OP_SUBTRACTION_TERM_WITH_CONST = "subtract-term-with-constant"
_OP_SUBTRACTION_NEGATIVE_CONST = "subtract-negative-constant"
_OP_SUBTRACTION_NEGATE_VARIABLE = "subtract-negative-variable"
_OP_ADD_NEG_CONST = "add_neg_const"
_OP_ADD_NEG_CONST_VAR = "add_neg_const_var"
_OP_ADD_NEG_CONST_VAR_EXP = "add_neg_const_var_exp"


class RestateSubtractionRule(BaseRule):
    """Convert subtract operators to plus negative to allow commuting"""

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
        is_parent_equal = isinstance(node.parent, EqualExpression)

        # Subtraction ops
        if is_sub and (node.parent is None or is_parent_equal or is_parent_add):
            if (
                isinstance(node.right, NegateExpression)
                and node.right.get_child() is not None
                and isinstance(node.right.get_child(), VariableExpression)
            ):
                # 4 - -x
                # 3 - -y + -u^2
                return _OP_SUBTRACTION_NEGATE_VARIABLE

            if (
                isinstance(node.right, ConstantExpression)
                and node.right.value is not None
                and node.right.value < 0.0
            ):
                # 4 - -1
                # 3 - -2 + -u^2
                return _OP_SUBTRACTION_NEGATIVE_CONST

            if (
                node.right is not None
                and isinstance(node.right.left, ConstantExpression)
                and node.right.left.value is not None
            ):
                # 4x - -1x
                # 3u^2 - -2t^4 + -u^2
                # 4 - 3x
                # 12 - -2x^2
                return _OP_SUBTRACTION_TERM_WITH_CONST

            # 4x - 2x
            return _OP_SUBTRACTION

        # The other cases are addition and negative/negation
        is_add = isinstance(node, AddExpression)
        if not is_add:
            return None

        # + -2 = Const
        if node.right and isinstance(node.right, ConstantExpression):
            assert node.right.value is not None
            if node.right.value < 0.0:
                return _OP_ADD_NEG_CONST
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
                return _OP_ADD_NEG_CONST_VAR
            return None

        # + -2x^3 = Mult(Const, Exp(Var, Const))
        if (
            isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, ConstantExpression)
            and isinstance(node.right.right, PowerExpression)
        ):
            assert node.right.left.value is not None
            if node.right.left.value < 0.0:
                return _OP_ADD_NEG_CONST_VAR_EXP
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
        new_right: MathExpression

        # Subtract term with const (2 - -3x^2 => 2 + 3x^2) or (2 - 3x => 2 + -3x)
        if tree_type == _OP_SUBTRACTION_TERM_WITH_CONST:
            assert node.right is not None and node.right.left is not None
            new_right = cast(MultiplyExpression, node.right.clone())
            assert (
                isinstance(new_right.left, ConstantExpression)
                and new_right.left.value is not None
            )
            # Flip the sign of the constant
            new_right.left.value *= -1
            result = AddExpression(node.left, new_right)
        # Subtract negative to plus positive (2 - -3 => 2 + 3)
        elif tree_type == _OP_SUBTRACTION_NEGATIVE_CONST:
            assert node.right is not None
            new_right = cast(ConstantExpression, node.right.clone())
            assert new_right.value is not None
            # Flip the sign of the constant
            new_right.value *= -1
            result = AddExpression(node.left, new_right)
        # Subtract negative to plus positive (2 - -x => 2 + x)
        elif tree_type == _OP_SUBTRACTION_NEGATE_VARIABLE:
            assert node.right is not None and isinstance(node.right, NegateExpression)
            child = node.right.get_child()
            assert child is not None
            result = AddExpression(node.left, child.clone())
        elif tree_type == _OP_SUBTRACTION:
            # Simple case of subtract to plus negate
            assert node.right is not None
            result = AddExpression(node.left, NegateExpression(node.right))
        else:
            # Plus negative to subtract cases
            assert node.left is not None and node.right is not None
            result = SubtractExpression(node.left, node.right.clone())
            if tree_type == _OP_ADD_NEG_CONST:
                assert (
                    result.right is not None
                    and isinstance(result.right, ConstantExpression)
                    and result.right.value is not None
                )
                result.right.value = -result.right.value
            elif tree_type == _OP_ADD_NEG_CONST_VAR:
                assert (
                    result.right is not None
                    and isinstance(result.right.left, ConstantExpression)
                    and result.right.left.value is not None
                )
                result.right.left.value = -result.right.left.value
            elif tree_type == _OP_ADD_NEG_CONST_VAR_EXP:
                assert (
                    result.right is not None
                    and isinstance(result.right.left, ConstantExpression)
                    and result.right.left.value is not None
                )
                result.right.left.value = -result.right.left.value
        result.set_changed()  # mark this node as changed for visualization
        return change.done(result)
