from typing import Any, Optional

from mathy_core.tree import BinaryTreeNode


class BinarySearchTree(BinaryTreeNode):
    left: Optional["BinarySearchTree"]
    right: Optional["BinarySearchTree"]
    parent: Optional["BinarySearchTree"]

    def __init__(self, key: Optional[int] = None, **kwargs: Any):
        super(BinarySearchTree, self).__init__(**kwargs)
        self.key = key
        self.x = 0
        self.y = 0
        self.offset = 0

    def clone(self) -> "BinarySearchTree":  # type:ignore[override]
        result: BinarySearchTree = super(BinarySearchTree, self).clone()
        result.key = self.key
        return result

    def insert(self, key: int) -> BinaryTreeNode:
        """Insert a node in the tree with the specified key."""
        node: BinarySearchTree = self.get_root()
        while node:
            assert node.key is not None
            if key > node.key:
                if not node.right:
                    node.set_right(BinarySearchTree(key))
                    break
                node = node.right
            elif key < node.key:
                if not node.left:
                    node.set_left(BinarySearchTree(key))
                    break

                node = node.left
            else:
                break
        return self

    def find(self: "BinarySearchTree", key: int) -> Optional["BinarySearchTree"]:
        """Find a node in the tree by its key and return it.  Return None if the key
        is not found in the tree."""
        node: BinarySearchTree = self.get_root()
        while node:
            assert node.key is not None
            if key > node.key:
                if not node.right:
                    return None

                node = node.right
                continue

            if key < node.key:
                if not node.left:
                    return None

                node = node.left
                continue

            if key == node.key:
                return node

            return None

        return None
