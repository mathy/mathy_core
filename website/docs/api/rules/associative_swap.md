```python

import mathy_core.rules.associative_swap
```
The `Associative Property` of numbers says that we can re-group two `addition` or `multiplication` terms so that one is evaluated before the other without changing the value of the expression.

The formulation of this property is the same for addition and multiplication:

- Addition `(a + b) + c = a + (b + c)`
- Multiplication `(a * b) * c = a * (b * c)`

!!! note

      Interestingly, applying the associative property of numbers to a binary expression tree is a standard tree operation called a "node rotation."

### Transformations

#### Addition

```
(a + b) + c = a + (b + c)

     (y) +            + (x)
        / \          / \
       /   \        /   \
  (x) +     c  ->  a     + (y)
     / \                / \
    /   \              /   \
   a     b            b     c
```

#### Multiplication

```
(a * b) * c = a * (b * c)

     (x) *            * (y)
        / \          / \
       /   \        /   \
  (y) *     c  <-  a     * (x)
     / \                / \
    /   \              /   \
   a     b            b     c
```

### Examples

`rule_tests:associative_swap`


## API


## AssociativeSwapRule
```python
AssociativeSwapRule(self, args, kwargs)
```
Associative Property
Addition: `(a + b) + c = a + (b + c)`

         (y) +            + (x)
            / \          / \
           /   \        /   \
      (x) +     c  ->  a     + (y)
         / \                / \
        /   \              /   \
       a     b            b     c

 Multiplication: `(ab)c = a(bc)`

         (x) *            * (y)
            / \          / \
           /   \        /   \
      (y) *     c  <-  a     * (x)
         / \                / \
        /   \              /   \
       a     b            b     c

