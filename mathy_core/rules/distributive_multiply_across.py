from ..expressions import (
    AddExpression,
    ConstantExpression,
    MathExpression,
    MultiplyExpression,
    PowerExpression,
    VariableExpression,
)
from ..rule import BaseRule, ExpressionChangeRule
from ..util import unlink


class DistributiveMultiplyRule(BaseRule):
    r"""
    Distributive Property
    `a(b + c) = ab + ac`

    The distributive property can be used to expand out expressions
    to allow for simplification, as well as to factor out common properties of terms.

    **Distribute across a group**

    This handles the `a(b + c)` conversion of the distributive property, which
    distributes `a` across both `b` and `c`.

    *note: this is useful because it takes a complex Multiply expression and
    replaces it with two simpler ones.  This can expose terms that can be
    combined for further expression simplification.*

                                 +
             *                  / \
            / \                /   \
           /   \              /     \
          a     +     ->     *       *
               / \          / \     / \
              /   \        /   \   /   \
             b     c      a     b a     c
    """

    @property
    def name(self) -> str:
        return "Distributive Multiply"

    @property
    def code(self) -> str:
        return "DM"

    def can_apply_to(self, node: MathExpression) -> bool:
        if isinstance(node, MultiplyExpression):
            if node.right and isinstance(node.left, AddExpression):
                return True

            if node.left and isinstance(node.right, AddExpression):
                return True

            return False

        return False

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node).save_parent()

        a: MathExpression
        b: MathExpression
        c: MathExpression
        ab: MathExpression
        ac: MathExpression

        assert node.left is not None
        assert node.right is not None
        if isinstance(node.left, AddExpression):
            assert node.left.right is not None and node.left.left is not None
            a = node.right
            b = node.left.left
            c = node.left.right
        else:
            assert node.right.right is not None and node.right.left is not None
            a = node.left
            b = node.right.left
            c = node.right.right

        unlinked = unlink(a)
        assert unlinked is not None
        a = unlinked

        # If the operands for either multiplication can be expressed
        # in a "natural" order, do so like a human would.
        a_exp_var = (
            isinstance(a, PowerExpression)
            and isinstance(a.right, VariableExpression)
            or isinstance(a.left, VariableExpression)
        )
        a_var: bool = a_exp_var or isinstance(a, VariableExpression)
        b_const: bool = isinstance(b, ConstantExpression)
        c_const: bool = isinstance(c, ConstantExpression)
        if a_var and b_const:
            ab = MultiplyExpression(b.clone(), a.clone())
        else:
            ab = MultiplyExpression(a.clone(), b.clone())

        if a_var and c_const:
            ac = MultiplyExpression(c.clone(), a.clone())
        else:
            ac = MultiplyExpression(a.clone(), c.clone())
        result = AddExpression(ab, ac)

        for n in [node, a, ab, ac, result]:
            n.set_changed()

        change.done(result)
        return change
