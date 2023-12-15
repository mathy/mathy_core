# mathy_core.rules.variable_multiply

## VariableMultiplyRule
```python
VariableMultiplyRule(self, args, kwargs)
```

This restates `x^b * x^d` as `x^(b + d)` which has the effect of isolating
the exponents attached to the variables, so they can be combined.

    1. When there are two terms with the same base being multiplied together, their
       exponents are added together. "x * x^3" = "x^4" because "x = x^1" so
       "x^1 * x^3 = x^(1 + 3) = x^4"

    TODO: 2. When there is a power raised to another power, they can be combined by
             multiplying the exponents together. "x^(2^2) = x^4"

The rule identifies terms with explicit and implicit powers, so the following
transformations are all valid:

Explicit powers: x^b * x^d = x^(b+d)

          *
         / \
        /   \          ^
       /     \    =   / \
      ^       ^      x   +
     / \     / \        / \
    x   b   x   d      b   d


Implicit powers: x * x^d = x^(1 + d)

        *
       / \
      /   \          ^
     /     \    =   / \
    x       ^      x   +
           / \        / \
          x   d      1   d


### get_type
```python
VariableMultiplyRule.get_type(
    self, 
    node: mathy_core.expressions.MathExpression, 
) -> Optional[Tuple[str, mathy_core.util.TermEx, mathy_core.util.TermEx]]
```
Determine the configuration of the tree for this transformation.

Support two types of tree configurations:
 - Simple is where the node's left and right children are exactly
   terms that can be multiplied together.
 - Chained is where the node's left child is a term, but the right
   child is a continuation of a more complex term, as indicated by
   the presence of another Multiply node. In this case the left child
   of the next multiply node is the target.

Structure:
 - Simple node(mult),node.left(term),node.right(term)
 - Chained node(mult),node.left(term),node.right(mult),node.right.left(term)

