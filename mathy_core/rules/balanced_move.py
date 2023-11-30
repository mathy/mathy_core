from typing import Optional

from ..expressions import (
    AddExpression,
    ConstantExpression,
    DivideExpression,
    EqualExpression,
    MathExpression,
    MultiplyExpression,
    SubtractExpression,
)
from ..rule import BaseRule, ExpressionChangeRule
from ..tree import LEFT, RIGHT
from ..types import Literal
from ..util import get_term_ex, unlink

_TYPE_ADDITION = "TYPE_ADDITION"
_TYPE_CONST_OF_MULTIPLY = "TYPE_CONST_OF_MULTIPLY"


class BalancedMoveRule(BaseRule):
    r"""Balanced rewrite rule moves nodes from one side of an equation
    to the other by performing the same operation on both sides.

    Addition: `a + 2 = 3` -> `a + 2 - 2 = 3 - 2`
    Multiplication: `3a = 3` -> `3a / 3 = 3 / 3`
    """

    @property
    def name(self) -> str:
        return "Balanced Move"

    @property
    def code(self) -> str:
        return "BM"

    def has_add_siblings(self, node: MathExpression) -> bool:
        root = node.get_root()
        root_side = node.get_root_side()
        node_subtree = root.left if root_side == LEFT else root.right
        assert node_subtree is not None
        if len(node_subtree.find_type(AddExpression)) > 0:
            return True
        return False

    def get_type(self, node: MathExpression) -> Optional[str]:
        """Determine the configuration of the tree for this transformation.

        Supports the following configurations:
         - Addition is a term connected by an addition to the side of an equation
           or inequality. It generates two subtractions to move from one side to the
           other.
         - Multiply is a coefficient of a term that must be divided on both sides of
           the equation or inequality.
        """
        root = node.get_root()
        if not isinstance(root, EqualExpression) or isinstance(
            node.parent, EqualExpression
        ):
            return None

        if isinstance(node.parent, MultiplyExpression) and isinstance(
            node, ConstantExpression
        ):
            # NOTE: Don't allow divisions or multiplications if there are additions
            #       remaining on the same side of the equation
            if self.has_add_siblings(node):
                return None

            return _TYPE_CONST_OF_MULTIPLY

        if isinstance(node.parent, AddExpression):
            if isinstance(node, ConstantExpression) or get_term_ex(node) is not None:
                return _TYPE_ADDITION

        return None

    def can_apply_to(self, node: MathExpression) -> bool:
        change_type = self.get_type(node)
        return True if change_type is not None else False

    def apply_to(self, node: MathExpression) -> ExpressionChangeRule:
        change = super().apply_to(node)
        change_type = self.get_type(node)
        node = node.clone_from_root()
        root = node.get_root()
        left_new = None
        right_new = None
        if change_type == _TYPE_CONST_OF_MULTIPLY:
            left_new = DivideExpression(root.left, node.clone())
            right_new = DivideExpression(root.right, node.clone())
        elif change_type == _TYPE_ADDITION:
            assert isinstance(node.parent, AddExpression), "expected add parent"
            assert (
                node.parent.parent is not None
            ), "expected node parent to have a parent"
            # If the parent is an Add, this node is a left/right child of an add...
            # You can replace the parent Add with whatever the other sibling is to
            # remove this node.
            save_sibling = unlink(node.get_sibling())
            assert save_sibling is not None
            node_clone = node.clone()
            grandparent = node.parent.parent
            grandparent_side = grandparent.get_side(node.parent)
            update_side: Literal["left", "right"] = (
                LEFT if node.get_root_side() == RIGHT else RIGHT
            )
            grandparent.set_side(save_sibling, grandparent_side)
            new_sub = SubtractExpression(
                root.left if update_side == LEFT else root.right, node_clone
            )
            new_sub.set_changed()
            root.set_side(new_sub, update_side)
            change.done(root)
            return change
        assert left_new is not None, "invalid left node"
        assert right_new is not None, "invalid right node"
        left_new.set_changed()
        right_new.set_changed()
        root.set_left(left_new)
        root.set_right(right_new)
        change.done(root)
        return change
