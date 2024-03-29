```python

import mathy_core.rules.commutative_swap
```
The `Commutative Property` of numbers says that we can re-order two `addition` or `multiplication` terms so that one occurs before the other in the expression without changing the value of the expression.

The formulation of this property is the same for addition and multiplication:

- Addition `a + b = b + a`
- Multiplication `a * b = b * a`

The commutative property is used for re-arranging the order of parts of an expression and is, as such, very important for working with mathematical expressions.

### Transformations

Given a common parent node, this rule switches the order of the children of that node. It can only be applied to addition or multiplication nodes.

#### Addition

`a + b = b + a`

```
        +                  +
       / \                / \
      /   \     ->       /   \
     /     \            /     \
    a       b          b       a
```

#### Multiplication

`a * b = b * a`

```
        *                  *
       / \                / \
      /   \     ->       /   \
     /     \            /     \
    a       b          b       a
```

### Examples

`rule_tests:commutative_swap`


## API


## CommutativeSwapRule
```python
CommutativeSwapRule(self, preferred: bool = True)
```
Commutative Property
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

