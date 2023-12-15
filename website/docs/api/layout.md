```python

import mathy_core.layout
```

Mathy uses the Tidier algorithm to create visual tree layouts for helping understand and interpret complex node trees.

`mathy:(28 + 1x)(17x - 2y)` 


## API


## TreeLayout
```python
TreeLayout(self, args, kwargs)
```
Calculate a visual layout for input trees.
### layout
```python
TreeLayout.layout(
    self, 
    node: mathy_core.tree.BinaryTreeNode, 
    unit_x_multiplier: float = 1.0, 
    unit_y_multiplier: float = 1.0, 
) -> 'TreeMeasurement'
```
Assign x/y values to all nodes in the tree, and return an object containing
the measurements of the tree.

Returns a TreeMeasurement object that describes the bounds of the tree
### transform
```python
TreeLayout.transform(
    self, 
    node: Optional[mathy_core.tree.BinaryTreeNode] = None, 
    x: float = 0, 
    unit_x_multiplier: float = 1, 
    unit_y_multiplier: float = 1, 
    measure: Optional[TreeMeasurement] = None, 
) -> 'TreeMeasurement'
```
Transform relative to absolute coordinates, and measure the bounds of
the tree.

Return a measurement of the tree in output units.
## TreeMeasurement
```python
TreeMeasurement(self) -> None
```
Summary of the rendered tree
