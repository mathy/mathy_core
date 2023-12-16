```python

import mathy_core.rules.restate_subtraction
```
Subtraction operations aren't commutable, but addition of negative values are. This flips a subtraction to a plus negation, to "unlock" terms and allow moving them around, e.g. for like-terms simplification.

### Examples

`rule_tests:restate_subtraction`


## API


## RestateSubtractionRule
```python
RestateSubtractionRule(self, args, kwargs)
```
Convert subtract operators to plus negative to allow commuting
### get_type
```python
RestateSubtractionRule.get_type(
    self, 
    node: mathy_core.expressions.MathExpression, 
) -> Optional[str]
```
Determine the configuration of the tree for this transformation.

Support two types of tree configurations:
 - Subtraction is a subtract to be restate as a plus negation
 - PlusNegative is a plus negative const to be restated as subtraction

