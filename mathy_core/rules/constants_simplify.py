from typing import Optional, Tuple

from ..expressions import (
    AddExpression,
    BinaryExpression,
    ConstantExpression,
    MathExpression,
    MultiplyExpression,
    NegateExpression,
    VariableExpression,
)
from ..rule import BaseRule, ExpressionChangeRule

_POS_SIMPLE: str = "simple"
_POS_NEGATION_SIMPLE: str = "negation_simple"
_POS_SIMPLE_VAR_MULT: str = "simple_var_multiply"
_POS_CHAINED_RIGHT: str = "chained_right"
_POS_CHAINED_RIGHT_LEFT: str = "chained_right_left"
_POS_CHAINED_RIGHT_LEFT_LEFT: str = "chained_right_left_left"
_POS_CHAINED_LEFT_LEFT_RIGHT: str = "chained_left_left_right"
_POS_CHAINED_RIGHT_DEEP: str = "chained_right_deep"


class ConstantsSimplifyRule(BaseRule):
    """Given a binary operation on two constants, simplify to the resulting
    constant expression"""

    @property
    def name(self) -> str:
        return "Constant Arithmetic"

    @property
    def code(self) -> str:
        return "CA"

    def get_type(
        self, node: MathExpression
    ) -> Optional[Tuple[str, ConstantExpression, ConstantExpression]]:
        """Determine the configuration of the tree for this transformation.

        Support the three types of tree configurations:
         - Simple is where the node's left and right children are exactly
           constants linked by an add operation.
         - Chained Right is where the node's left child is a constant, but the right
           child is another binary operation of the same type. In this case the left
           child of the next binary node is the target.

        Structure:
         - Simple
            * node(add),node.left(const),node.right(const)
         - Chained Right
            * node(add),node.left(const),node.right(add),node.right.left(const)
         - Chained Right Deep
            * node(add),node.left(const),node.right(add),node.right.left(const)
        """
        # Check for a negation wrapping a simple binary op with constants
        # -(3 + 2)
        if isinstance(node, NegateExpression):
            child = node.get_child()
            if (
                child is not None
                and isinstance(child, BinaryExpression)
                and isinstance(child.left, ConstantExpression)
                and isinstance(child.right, ConstantExpression)
            ):
                return _POS_NEGATION_SIMPLE, child.left, child.right

        # Check simple case of left/right child binary op with constants
        # (4 * 2) + 3
        if (
            isinstance(node, BinaryExpression)
            and isinstance(node.left, ConstantExpression)
            and isinstance(node.right, ConstantExpression)
        ):
            return _POS_SIMPLE, node.left, node.right

        # Check for const * var * const
        # (4n * 2) + 3
        if (
            isinstance(node, MultiplyExpression)
            and isinstance(node.left, MultiplyExpression)
            and isinstance(node.left.left, ConstantExpression)
            and isinstance(node.left.right, VariableExpression)
            and isinstance(node.right, ConstantExpression)
        ):
            return _POS_SIMPLE_VAR_MULT, node.left.left, node.right

        # Check for a continuation to the right that's more than one node
        # e.g. "5 * (8h * t)" = "40h * t"
        if (
            isinstance(node, BinaryExpression)
            and isinstance(node.left, ConstantExpression)
            and isinstance(node.right, BinaryExpression)
            and isinstance(node.right.left, BinaryExpression)
            and isinstance(node.right.left.left, ConstantExpression)
        ):
            # Add/Multiply continuations are okay
            if (
                isinstance(node, AddExpression)
                and isinstance(node.right, AddExpression)
                and isinstance(node.right.left, AddExpression)
                or isinstance(node, MultiplyExpression)
                and isinstance(node.right, MultiplyExpression)
                and isinstance(node.right.left, MultiplyExpression)
            ):
                return (
                    _POS_CHAINED_RIGHT_DEEP,
                    node.left,
                    node.right.left.left,
                )

        # Check for a continuation to the right
        # "(7 * 10y^3) * x"
        if (
            isinstance(node, BinaryExpression)
            and isinstance(node.left, ConstantExpression)
            and isinstance(node.right, BinaryExpression)
            and isinstance(node.right.left, ConstantExpression)
        ):
            # Add/Multiply continuations are okay
            if (
                isinstance(node, AddExpression)
                and isinstance(node.right, AddExpression)
                or isinstance(node, MultiplyExpression)
                and isinstance(node.right, MultiplyExpression)
            ):
                return (
                    _POS_CHAINED_RIGHT,
                    node.left,
                    node.right.left,
                )

        # Check for a continuation to the right
        # "(7q * 10y^3) * x"
        if (
            isinstance(node, MultiplyExpression)
            and isinstance(node.left, MultiplyExpression)
            and isinstance(node.left.left, ConstantExpression)
            and isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, ConstantExpression)
        ):
            return (
                _POS_CHAINED_RIGHT_LEFT,
                node.left.left,
                node.right.left,
            )

        # Check for variable terms with constants on the left and right
        # "792z^4 * 490f * q^3"
        #   ^--------^
        if (
            isinstance(node, MultiplyExpression)
            and isinstance(node.left, MultiplyExpression)
            and isinstance(node.left.left, ConstantExpression)
            and isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, MultiplyExpression)
            and isinstance(node.right.left.left, ConstantExpression)
        ):
            return (
                _POS_CHAINED_RIGHT_LEFT_LEFT,
                node.left.left,
                node.right.left.left,
            )

        # Check for variable terms with constants nested on the left and right
        # "(u^3 * 36c^6) * 7u^3"
        #         ^--------^
        if (
            isinstance(node, MultiplyExpression)
            and isinstance(node.left, MultiplyExpression)
            and isinstance(node.left.right, MultiplyExpression)
            and isinstance(node.left.right.left, ConstantExpression)
            and isinstance(node.right, MultiplyExpression)
            and isinstance(node.right.left, ConstantExpression)
        ):
            return (
                _POS_CHAINED_LEFT_LEFT_RIGHT,
                node.left.right.left,
                node.right.left,
            )

        return None

    def can_apply_to(self, node: MathExpression) -> bool:
        return self.get_type(node) is not None

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node)
        type_result = self.get_type(node)
        assert (
            type_result is not None
        ), "make sure can_apply_to returns True before calling apply_to"
        arrangement, left_const, right_const = type_result
        change.save_parent()
        result: MathExpression
        value: MathExpression
        if arrangement == _POS_SIMPLE:
            result = ConstantExpression(node.evaluate())
        elif arrangement == _POS_NEGATION_SIMPLE:
            # If a negation parent exists, flip the result
            result = ConstantExpression(node.evaluate())
        elif arrangement == _POS_SIMPLE_VAR_MULT:
            assert isinstance(node, MultiplyExpression)
            assert node.left is not None
            assert isinstance(node.left.right, VariableExpression)
            value = ConstantExpression(
                MultiplyExpression(left_const, right_const).evaluate()
            )
            result = MultiplyExpression(value, node.left.right)
        elif arrangement == _POS_CHAINED_LEFT_LEFT_RIGHT:
            assert isinstance(node, MultiplyExpression) and node.left is not None
            assert node.left.right is not None and node.right is not None
            value = ConstantExpression(
                MultiplyExpression(left_const, right_const).evaluate()
            )
            result = MultiplyExpression(
                node.left.left,
                MultiplyExpression(
                    MultiplyExpression(value, node.left.right.right), node.right.right
                ),
            )

        elif arrangement == _POS_CHAINED_RIGHT_LEFT:
            assert node.right is not None and node.left is not None
            value = ConstantExpression(
                MultiplyExpression(left_const, right_const).evaluate()
            )
            value = MultiplyExpression(value, node.left.right)
            result = MultiplyExpression(value, node.right.right)
        elif arrangement == _POS_CHAINED_RIGHT_LEFT_LEFT:
            assert node.left is not None and node.right is not None
            assert node.right.left is not None
            value = ConstantExpression(
                MultiplyExpression(left_const, right_const).evaluate()
            )
            value = MultiplyExpression(value, node.left.right)
            result = MultiplyExpression(
                value, MultiplyExpression(node.right.left.right, node.right.right)
            )
        elif arrangement == _POS_CHAINED_RIGHT:
            assert node.right is not None
            if isinstance(node, AddExpression):
                value = ConstantExpression(
                    AddExpression(left_const, right_const).evaluate()
                )
                result = AddExpression(value, node.right.right)
            elif isinstance(node, MultiplyExpression):
                value = ConstantExpression(
                    MultiplyExpression(left_const, right_const).evaluate()
                )
                result = MultiplyExpression(value, node.right.right)
            else:
                raise NotImplementedError(
                    f"can't deal with operand of {type(node)} type"
                )
        elif arrangement == _POS_CHAINED_RIGHT_DEEP:
            assert node.right is not None and node.right.left is not None
            if isinstance(node, AddExpression):
                value = ConstantExpression(
                    AddExpression(left_const, right_const).evaluate()
                )
                result = AddExpression(
                    AddExpression(value, node.right.left.right), node.right.right
                )
            elif isinstance(node, MultiplyExpression):
                value = ConstantExpression(
                    MultiplyExpression(left_const, right_const).evaluate()
                )
                result = MultiplyExpression(
                    MultiplyExpression(value, node.right.left.right), node.right.right
                )
            else:
                raise NotImplementedError(
                    f"can't deal with operand of {type(node)} type"
                )
        else:
            raise ValueError(f"unknown node arrangement for: {node}")
        assert result is not None
        result.set_changed()
        return change.done(result)
