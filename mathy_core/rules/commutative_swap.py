from typing import Optional

from ..expressions import (
    AddExpression,
    ConstantExpression,
    EqualExpression,
    MathExpression,
    MultiplyExpression,
    PowerExpression,
    VariableExpression,
)
from ..rule import BaseRule, ExpressionChangeRule


class CommutativeSwapRule(BaseRule):
    r"""Commutative Property
    For Addition: `a + b = b + a`

             +                  +
            / \                / \
           /   \     ->       /   \
          /     \            /     \
         a       b          b       a

    For Multiplication: `a * b = b * a`

             *                  *
            / \                / \
           /   \     ->       /   \
          /     \            /     \
         a       b          b       a
    """

    preferred: bool

    def __init__(self, preferred: bool = True):
        # If false, terms that are in preferred order will not commute
        self.preferred = preferred

    @property
    def name(self) -> str:
        return "Commutative Swap"

    @property
    def code(self) -> str:
        return "CS"

    def can_apply_to(self, node: MathExpression) -> bool:
        # Must be an add/multiply
        if isinstance(node, (AddExpression, EqualExpression)):
            return True
        if not isinstance(node, MultiplyExpression):
            return False
        # When preferred is false, the commutative rule won't apply to term
        # nodes that are already in a preferred position.
        if self.preferred is False:
            # 4x won't commute to x * 4
            left_const = isinstance(node.left, ConstantExpression)
            right_var = isinstance(node.right, VariableExpression)
            if left_const and right_var:
                # UNLESS it is within a more complex term that spans multiple nodes.
                if node.parent and isinstance(node.parent, MultiplyExpression):
                    sibling = node.get_sibling()
                    return bool(sibling and isinstance(sibling, MultiplyExpression))
                # Nope
                return False

            # 8y^4 won't commute to y^4 * 8
            if isinstance(node.right, PowerExpression):
                right_left_var = isinstance(node.right.left, VariableExpression)
                right_right_const = isinstance(node.right.right, ConstantExpression)
                if right_left_var and right_right_const:
                    # UNLESS it is within a more complex term that spans multiple nodes.
                    if node.parent and isinstance(node.parent, MultiplyExpression):
                        sibling = node.get_sibling()
                        return bool(sibling and isinstance(sibling, MultiplyExpression))
                    # Nope
                    return False
        return True

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node)
        a: Optional[MathExpression] = node.left
        b: Optional[MathExpression] = node.right
        assert a is not None

        add_chain = isinstance(a, AddExpression) and isinstance(node, AddExpression)
        mul_chain = isinstance(a, MultiplyExpression) and isinstance(
            node, MultiplyExpression
        )

        # An equation can always be flipped
        if isinstance(node, EqualExpression):
            node.set_right(a)
            node.set_left(b)
        # The left node is not another sibling add
        elif not add_chain and not mul_chain:
            node.set_right(a)
            node.set_left(b)
        else:
            # If it's another add, swap their
            # children directly to avoid inner-nesting.
            two = a.right
            three = node.right
            a.set_right(three)
            node.set_right(two)

        node.set_changed()
        change.done(node)
        return change
