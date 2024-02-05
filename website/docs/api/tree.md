```python

import mathy_core.tree
```

## BinaryTreeNode
```python
BinaryTreeNode(
    self: ~NodeType, 
    left: Optional[~NodeType] = None, 
    right: Optional[~NodeType] = None, 
    parent: Optional[~NodeType] = None, 
    id: Optional[str] = None, 
)
```

The binary tree node is the base node for all of our trees, and provides a
rich set of methods for constructing, inspecting, and modifying them.
The node itself defines the structure of the binary tree, having left and right
children, and a parent.

### clone
```python
BinaryTreeNode.clone(self: ~NodeType) -> ~NodeType
```
Create a clone of this tree
### get_children
```python
BinaryTreeNode.get_children(self: ~NodeType) -> List[~NodeType]
```
Get children as an array.  If there are two children, the first object will
always represent the left child, and the second will represent the right.
### get_root
```python
BinaryTreeNode.get_root(self: ~NodeType) -> ~NodeType
```
Return the root element of this tree
### get_root_side
```python
BinaryTreeNode.get_root_side(self: ~NodeType) -> Literal['left', 'right']
```
Return the side of the tree that this node lives on
### get_sibling
```python
BinaryTreeNode.get_sibling(self: ~NodeType) -> Optional[~NodeType]
```
Get the sibling node of this node.  If there is no parent, or the node
has no sibling, the return value will be None.
### get_side
```python
BinaryTreeNode.get_side(
    self, 
    child: Optional[~NodeType], 
) -> Literal['left', 'right']
```
Determine whether the given `child` is the left or right child of this
node
### is_leaf
```python
BinaryTreeNode.is_leaf(self) -> bool
```
Is this node a leaf?  A node is a leaf if it has no children.
### rotate
```python
BinaryTreeNode.rotate(self: ~NodeType) -> ~NodeType
```

Rotate a node, changing the structure of the tree, without modifying
the order of the nodes in the tree.

### set_left
```python
BinaryTreeNode.set_left(
    self: ~NodeType, 
    child: Optional[~NodeType] = None, 
    clear_old_child_parent: bool = False, 
) -> ~NodeType
```
Set the left node to the passed `child`
### set_right
```python
BinaryTreeNode.set_right(
    self: ~NodeType, 
    child: Optional[~NodeType] = None, 
    clear_old_child_parent: bool = False, 
) -> ~NodeType
```
Set the right node to the passed `child`
### set_side
```python
BinaryTreeNode.set_side(
    self, 
    child: ~NodeType, 
    side: Literal['left', 'right'], 
) -> ~NodeType
```
Set a new `child` on the given `side`
### visit_inorder
```python
BinaryTreeNode.visit_inorder(
    self, 
    visit_fn: Callable[[Any, int, Optional[Any]], Optional[Literal['stop']]], 
    depth: int = 0, 
    data: Optional[Any] = None, 
) -> Optional[Literal['stop']]
```
Visit the tree inorder, which visits the left child, then the current node,
and then its right child.

*Left -> Visit -> Right*

This method accepts a function that will be invoked for each node in the
tree.  The callback function is passed three arguments: the node being
visited, the current depth in the tree, and a user specified data parameter.

!!! info

    Traversals may be canceled by returning `STOP` from any visit function.

### visit_postorder
```python
BinaryTreeNode.visit_postorder(
    self, 
    visit_fn: Callable[[Any, int, Optional[Any]], Optional[Literal['stop']]], 
    depth: int = 0, 
    data: Optional[Any] = None, 
) -> Optional[Literal['stop']]
```
Visit the tree postorder, which visits its left child, then its right child,
and finally the current node.

*Left -> Right -> Visit*

This method accepts a function that will be invoked for each node in the
tree.  The callback function is passed three arguments: the node being
visited, the current depth in the tree, and a user specified data parameter.

!!! info

    Traversals may be canceled by returning `STOP` from any visit function.

### visit_preorder
```python
BinaryTreeNode.visit_preorder(
    self, 
    visit_fn: Callable[[Any, int, Optional[Any]], Optional[Literal['stop']]], 
    depth: int = 0, 
    data: Optional[Any] = None, 
) -> Optional[Literal['stop']]
```
Visit the tree preorder, which visits the current node, then its left
child, and then its right child.

*Visit -> Left -> Right*

This method accepts a function that will be invoked for each node in the
tree.  The callback function is passed three arguments: the node being
visited, the current depth in the tree, and a user specified data parameter.

!!! info

    Traversals may be canceled by returning `STOP` from any visit function.

## VisitDataType
Template type of user data passed to visit functions.