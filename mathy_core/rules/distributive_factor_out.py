from typing import Optional, Tuple

from ..expressions import (
    AddExpression,
    MathExpression,
    MultiplyExpression,
    SubtractExpression,
)
from ..rule import BaseRule, ExpressionChangeRule
from ..util import FactorResult, TermEx, factor_add_terms_ex, get_term_ex, make_term

_POS_SIMPLE = "simple"
_POS_CHAINED_BOTH = "chained_both"
_POS_CHAINED_LEFT = "chained_left"
_POS_CHAINED_LEFT_RIGHT = "chained_left_right"
_POS_CHAINED_RIGHT_LEFT = "chained_right_left"
_POS_CHAINED_RIGHT = "chained_right"


class DistributiveFactorOutRule(BaseRule):
    r"""Distributive Property
        `ab + ac = a(b + c)`

         The distributive property can be used to expand out expressions
         to allow for simplification, as well as to factor out common properties
         of terms.

         **Factor out a common term**

         This handles the `ab + ac` conversion of the distributive property, which
         factors out a common term from the given two addition operands.

                   +               *
                  / \             / \
                 /   \           /   \
                /     \    ->   /     \
               *       *       a       +
              / \     / \             / \
             a   b   a   c           b   c
    """

    constants: bool

    def __init__(self, constants: bool = False):
        # If true, will factor common numbers out of a const+const expression
        self.constants = constants

    @property
    def name(self) -> str:
        return "Distributive Factoring"

    @property
    def code(self) -> str:
        return "DF"

    def get_type(self, node: MathExpression) -> Optional[Tuple[str, TermEx, TermEx]]:
        """Determine the configuration of the tree for this transformation.

        Support the three types of tree configurations:

         - Simple is where the node's left and right children are exactly
           terms linked by an add operation.
         - Chained Left is where the node's left child is a term, but the right
           child is another add operation. In this case the left child
           of the next add node is the target.
         - Chained Right is where the node's right child is a term, but the left
           child is another add operation. In this case the right child
           of the child add node is the target.

        Structure:

         - Simple
            * node(add),node.left(term),node.right(term)
         - Chained Left
            * node(add),node.left(term),node.right(add),node.right.left(term)
         - Chained Right
            * node(add),node.right(term),node.left(add),node.left.right(term)
        """
        if not isinstance(node, AddExpression):
            return None
        # Left node in both cases is always resolved as a term.
        left_term = get_term_ex(node.left)
        right_term = get_term_ex(node.right)

        # No terms found for either child
        if left_term is None and right_term is None:
            # Check for the rare case where both terms are chained.
            # This happens when forcing the associative groups into
            # a certain form. It's not usually useful, but it's a
            # valid thing to do.

            if isinstance(node.right, AddExpression):
                right_term = get_term_ex(node.right.left)
            if right_term is None or right_term.variable is None:
                return None

            if isinstance(node.left, AddExpression):
                left_term = get_term_ex(node.left.right)
            if left_term is None or left_term.variable is None:
                return None
            return _POS_CHAINED_BOTH, left_term, right_term

        # Simplest case of each child being a term exactly.
        if left_term is not None and right_term is not None:
            return _POS_SIMPLE, left_term, right_term

        # Left child is a term
        if left_term is not None:
            if isinstance(node.right, AddExpression):
                right_term = get_term_ex(node.right.left)
            if right_term is not None:
                if right_term.variable is None:
                    return None
                return (
                    _POS_CHAINED_RIGHT,
                    left_term,
                    right_term,
                )

            # check inside another group
            if isinstance(node.right, AddExpression) and isinstance(
                node.right.left, AddExpression
            ):
                right_term = get_term_ex(node.right.left.left)
            if right_term is None or right_term.variable is None:
                return None
            return (
                _POS_CHAINED_RIGHT_LEFT,
                left_term,
                right_term,
            )

        # Right child is a term
        if right_term is not None:
            if isinstance(node.left, AddExpression):
                left_term = get_term_ex(node.left.right)
            if left_term is not None:
                if left_term.variable is None:
                    return None
                return _POS_CHAINED_LEFT, left_term, right_term

            # check inside another group
            if isinstance(node.left, AddExpression) and isinstance(
                node.left.right, AddExpression
            ):
                left_term = get_term_ex(node.left.right.right)
            if left_term is None or left_term.variable is None:
                return None
            return (
                _POS_CHAINED_LEFT_RIGHT,
                left_term,
                right_term,
            )

        return None

    def can_apply_to(self, node: MathExpression) -> bool:
        type_tuple = self.get_type(node)
        if type_tuple is None:
            return False
        type, l_term, r_term = type_tuple
        # Don't try factoring out terms with no variables, e.g "4 + 84"
        if (
            self.constants is False
            and l_term.variable is None
            and r_term.variable is None
        ):
            return False

        f = factor_add_terms_ex(l_term, r_term)
        if not f:
            return False

        if f.best == 1 and not f.variable and not f.exponent:
            return False

        return True

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node).save_parent()
        type_result = self.get_type(node)
        assert (
            type_result is not None
        ), "make sure can_apply_to returns True before calling apply_to"
        tree_position, left_term, right_term = type_result
        assert left_term is not None
        assert right_term is not None
        factors = factor_add_terms_ex(left_term, right_term)
        assert isinstance(factors, FactorResult)
        a = make_term(factors.best, factors.variable, factors.exponent)
        b = make_term(factors.left, factors.leftVariable, factors.leftExponent)
        c = make_term(factors.right, factors.rightVariable, factors.rightExponent)
        inside = (
            AddExpression(b, c)
            if isinstance(node, AddExpression)
            else SubtractExpression(b, c)
        )
        # NOTE: we swap the output order of the extracted
        #       common factor and what remains to prefer
        #       ordering that can be expressed without an
        #       explicit multiplication symbol.
        result: MathExpression = MultiplyExpression(inside, a)
        result.all_changed()

        # Fix the links to existing nodes on the left side of the result
        left_positions = [
            _POS_CHAINED_LEFT,
            _POS_CHAINED_BOTH,
        ]
        if tree_position in left_positions:
            assert node.left is not None
            # Because in the chained mode we extract node.left.right, the other
            # child is the remainder we want to be sure to preserve.
            # e.g. "(4 + p) + p" we need to keep "4"
            keep_child = node.left.left
            result = AddExpression(keep_child, result)

        # Fix the links to existing nodes on the left-right side of the result
        if tree_position == _POS_CHAINED_LEFT_RIGHT:
            assert node.left is not None and node.left.right is not None
            keep_child = AddExpression(node.left.left, node.left.right.left)
            result = AddExpression(keep_child, result)

        # Fix the links to existing nodes on the right-left side of the result
        if tree_position == _POS_CHAINED_RIGHT_LEFT:
            assert node.right is not None and node.right.left is not None
            keep_child = AddExpression(node.right.left.right, node.right.right)
            result = AddExpression(result, keep_child)

        # Fix the links to existing nodes on the right side of the result
        right_positions = [
            _POS_CHAINED_RIGHT,
            _POS_CHAINED_BOTH,
        ]
        if tree_position in right_positions:
            assert node.right is not None
            # Because in the chained mode we extract node.right.left, the other
            # child is the remainder we want to be sure to preserve.
            # e.g. "p + (p + 2x)" we need to keep 2x
            keep_child = node.right.right
            result = AddExpression(result, keep_child)
        change.done(result)
        return change
