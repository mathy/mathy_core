The `Distributive Property` of numbers says that we can factor out common values from terms connected with an addition operator.

This rule is expressed by the equation `ab + ac = a(b + c)`

!!! note

    This is a core transformation used in combining like terms, though we usually skip over it mentally because humans are pretty intelligent.

    Consider that the `9y + 9y` example from above becomes `(9 + 9) * y`. If you apply a constant simplification rule, you end up with `18y`, which results from combining the two like `y` terms.

### Transformations

Given a common parent node, this rule extracts the common value from both sides, leaving an addition and a multiplication.

#### Addition

`ab + ac = a(b + c)`

```
          +               *
         / \             / \
        /   \           /   \
       /     \    ->   /     \
      *       *       a       +
     / \     / \             / \
    a   b   a   c           b   c
```

### Examples

`rule_tests:distributive_factor_out`

# API

```python

import mathy_core.rules.distributive_factor_out
```


## DistributiveFactorOutRule
```python
DistributiveFactorOutRule(self, constants: bool = False)
```
Distributive Property
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

### get_type
```python
DistributiveFactorOutRule.get_type(
    self, 
    node: mathy_core.expressions.MathExpression, 
) -> Optional[Tuple[str, mathy_core.util.TermEx, mathy_core.util.TermEx]]
```
Determine the configuration of the tree for this transformation.

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

