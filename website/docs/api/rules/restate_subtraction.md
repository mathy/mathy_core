```python

import mathy_core.rules.restate_subtraction
```

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
