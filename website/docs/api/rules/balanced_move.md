# mathy_core.rules.balanced_move

## BalancedMoveRule
```python
BalancedMoveRule(self, args, kwargs)
```
Balanced rewrite rule moves nodes from one side of an equation
to the other by performing the same operation on both sides.

Addition: `a + 2 = 3` -> `a + 2 - 2 = 3 - 2`
Multiplication: `3a = 3` -> `3a / 3 = 3 / 3`

### get_type
```python
BalancedMoveRule.get_type(
    self, 
    node: mathy_core.expressions.MathExpression, 
) -> Optional[str]
```
Determine the configuration of the tree for this transformation.

Supports the following configurations:
 - Addition is a term connected by an addition to the side of an equation
   or inequality. It generates two subtractions to move from one side to the
   other.
 - Multiply is a coefficient of a term that must be divided on both sides of
   the equation or inequality.

