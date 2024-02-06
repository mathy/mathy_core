```python

import mathy_core.rules.multiplicative_inverse
```
The `Multiplicative Inverse` rule converts division operations into multiplication by the reciprocal. This transformation can simplify the structure of mathematical expressions and prepare them for further simplification.

This rule is expressed with the equation `a / b = a * (1 / b)`

**Convert Division to Multiplication by Reciprocal**

This handles the `a / b` conversion to `a * (1 / b)`.

**Handle Division by a Negative Denominator**

When the denominator is negative, the rule handles it by negating the numerator and converting the division into multiplication by the positive reciprocal of the denominator.

This handles the `4 / -(2 + 3)` conversion to `4 * -1 / (2 + 3)`

### Examples

`rule_tests:multiplicative_inverse`


## API


## MultiplicativeInverseRule
```python
MultiplicativeInverseRule(self, args, kwargs)
```
Convert division operations to multiplication by the reciprocal.
### get_type
```python
MultiplicativeInverseRule.get_type(
    self, 
    node: mathy_core.expressions.MathExpression, 
) -> Optional[str]
```
Determine the configuration of the tree for this transformation.

Support different types of tree configurations based on the division operation:
- DivisionExpression restated as multiplication by reciprocal
- DivisionNegativeDenominator is a division by a negative term

