from typing import Any, Callable, List, Optional, TypeVar, Union

from .types import Literal

NodeType = TypeVar("NodeType", bound="BinaryTreeNode")
try:
    NodeType.__doc__ = "Template type that inherits from BinaryTreeNode."
except AttributeError:
    ...  # Boo!

# ## Constants

# Return this from a node visit function to abort a tree visit.
STOP: Literal["stop"] = "stop"
# The constant representing the left child side of a node.
LEFT: Literal["left"] = "left"
# The constant representing the right child side of a node.
RIGHT: Literal["right"] = "right"


SideType = Union[Literal["left"], Literal["right"]]
VisitStop = Literal["stop"]
VisitDataType = TypeVar("VisitDataType", bound=Any)
try:
    VisitDataType.__doc__ = "Template type of user data passed to visit functions."
except AttributeError:
    ...  # Boo!
VisitFunction = Callable[[NodeType, int, VisitDataType], Optional[VisitStop]]


class BinaryTreeNode:
    """
    The binary tree node is the base node for all of our trees, and provides a
    rich set of methods for constructing, inspecting, and modifying them.
    The node itself defines the structure of the binary tree, having left and right
    children, and a parent.
    """

    _idCounter = 0

    # Tree layout mutations. Thanks, 2009 Justin. :( :(
    x: Optional[float]
    y: Optional[float]
    offset: Optional[float]
    level: Optional[int]
    thread: Optional["BinaryTreeNode"]

    left: Optional["BinaryTreeNode"]
    right: Optional["BinaryTreeNode"]
    parent: Optional["BinaryTreeNode"]

    #  Allow specifying children in the constructor
    def __init__(
        self,
        left: "BinaryTreeNode" = None,
        right: "BinaryTreeNode" = None,
        parent: "BinaryTreeNode" = None,
        id: Optional[str] = None,
    ):
        if id is None:
            BinaryTreeNode._idCounter = BinaryTreeNode._idCounter + 1
            id = f"mn-{BinaryTreeNode._idCounter}"
        self.id = id
        self.left = None
        self.right = None
        self.set_left(left)
        self.set_right(right)
        self.parent = parent

    def clone(self) -> NodeType:
        """Create a clone of this tree"""
        result: NodeType = self.__class__()  # type:ignore
        result.id = self.id
        if self.left:
            result.set_left(self.left.clone())  # type:ignore

        if self.right:
            result.set_right(self.right.clone())  # type:ignore
        return result

    def is_leaf(self) -> bool:
        """Is this node a leaf?  A node is a leaf if it has no children."""
        return not self.left and not self.right

    def __str__(self) -> str:
        """Serialize the node as a str"""
        return "{} {}".format(self.left, self.right)

    @property
    def name(self) -> str:
        """Human readable name for this node."""
        return "BinaryTreeNode"

    def rotate(self: NodeType) -> NodeType:
        """
        Rotate a node, changing the structure of the tree, without modifying
        the order of the nodes in the tree.
        """
        node = self
        parent = self.parent
        if not node or not parent:
            return self

        grand_parent = parent.parent
        if node == parent.left:
            parent.set_left(node.right)
            node.right = parent
            parent.parent = node
        else:
            parent.set_right(node.left)
            node.left = parent
            parent.parent = node

        node.parent = grand_parent
        if not grand_parent:
            return self

        if parent == grand_parent.left:
            grand_parent.left = node
        else:
            grand_parent.right = node
        return self

    def visit_preorder(
        self: NodeType,
        visit_fn: VisitFunction,
        depth: int = 0,
        data: Optional[VisitDataType] = None,
    ) -> Optional[VisitStop]:
        """Visit the tree preorder, which visits the current node, then its left
        child, and then its right child.

        *Visit -> Left -> Right*

        This method accepts a function that will be invoked for each node in the
        tree.  The callback function is passed three arguments: the node being
        visited, the current depth in the tree, and a user specified data parameter.

        !!! info

            Traversals may be canceled by returning `STOP` from any visit function.
        """
        if visit_fn and visit_fn(self, depth, data) == STOP:
            return STOP

        if self.left and self.left.visit_preorder(visit_fn, depth + 1, data) == STOP:
            return STOP

        if self.right and self.right.visit_preorder(visit_fn, depth + 1, data) == STOP:
            return STOP
        return None

    def visit_inorder(
        self: NodeType,
        visit_fn: VisitFunction,
        depth: int = 0,
        data: Optional[VisitDataType] = None,
    ) -> Optional[VisitStop]:
        """Visit the tree inorder, which visits the left child, then the current node,
        and then its right child.

        *Left -> Visit -> Right*

        This method accepts a function that will be invoked for each node in the
        tree.  The callback function is passed three arguments: the node being
        visited, the current depth in the tree, and a user specified data parameter.

        !!! info

            Traversals may be canceled by returning `STOP` from any visit function.
        """
        if self.left and self.left.visit_inorder(visit_fn, depth + 1, data) == STOP:
            return STOP

        if visit_fn and visit_fn(self, depth, data) == STOP:
            return STOP

        if self.right and self.right.visit_inorder(visit_fn, depth + 1, data) == STOP:
            return STOP
        return None

    def visit_postorder(
        self: NodeType,
        visit_fn: VisitFunction,
        depth: int = 0,
        data: Optional[VisitDataType] = None,
    ) -> Optional[VisitStop]:
        """Visit the tree postorder, which visits its left child, then its right child,
        and finally the current node.

        *Left -> Right -> Visit*

        This method accepts a function that will be invoked for each node in the
        tree.  The callback function is passed three arguments: the node being
        visited, the current depth in the tree, and a user specified data parameter.

        !!! info

            Traversals may be canceled by returning `STOP` from any visit function.
        """
        if self.left and self.left.visit_postorder(visit_fn, depth + 1, data) == STOP:
            return STOP

        if self.right and self.right.visit_postorder(visit_fn, depth + 1, data) == STOP:
            return STOP

        if visit_fn and visit_fn(self, depth, data) == STOP:
            return STOP
        return None

    def get_root(self: NodeType) -> NodeType:
        """Return the root element of this tree"""
        result = self
        while result.parent:
            result = result.parent  # type:ignore

        return result

    # **Child Management**
    #
    # Methods for setting the children on this expression.  These take care of
    # making sure that the proper parent assignments also take place.

    def set_left(
        self: NodeType,
        child: Optional["BinaryTreeNode"] = None,
        clear_old_child_parent: bool = False,
    ) -> NodeType:
        """Set the left node to the passed `child`"""
        if child == self:
            raise ValueError("nodes cannot be their own children")
        if self.left is not None and clear_old_child_parent:
            self.left.parent = None
        self.left = child
        if self.left:
            self.left.parent = self

        return self

    def set_right(
        self: NodeType,
        child: Optional["BinaryTreeNode"] = None,
        clear_old_child_parent: bool = False,
    ) -> NodeType:
        """Set the right node to the passed `child`"""
        if child == self:
            raise ValueError("nodes cannot be their own children")
        if self.right is not None and clear_old_child_parent:
            self.right.parent = None
        self.right = child
        if self.right:
            self.right.parent = self

        return self

    def get_side(self, child: NodeType) -> SideType:
        """Determine whether the given `child` is the left or right child of this
        node"""
        if child == self.left:
            return LEFT

        if child == self.right:
            return RIGHT

        raise ValueError("BinaryTreeNode.get_side: not a child of this node")

    def set_side(self, child: NodeType, side: SideType) -> NodeType:
        """Set a new `child` on the given `side`"""
        if side == LEFT:
            return self.set_left(child)  # type:ignore

        if side == RIGHT:
            return self.set_right(child)  # type:ignore

        raise ValueError("BinaryTreeNode.set_side: Invalid side")

    def get_children(self) -> List[NodeType]:
        """Get children as an array.  If there are two children, the first object will
        always represent the left child, and the second will represent the right."""
        result: List[Any] = []
        if self.left:
            result.append(self.left)

        if self.right:
            result.append(self.right)

        return result

    def get_sibling(self: NodeType) -> Optional[NodeType]:
        """Get the sibling node of this node.  If there is no parent, or the node
        has no sibling, the return value will be None."""
        if not self.parent:
            return None

        if self.parent.left == self:
            return self.parent.right  # type:ignore

        if self.parent.right == self:
            return self.parent.left  # type:ignore

        return None
