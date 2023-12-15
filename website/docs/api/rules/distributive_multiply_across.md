The `Distributive Property` can distribute multiplication across grouped terms. This has the effect of removing a grouping and can expose the terms that were inside for further simplification depending on the problem type.

This rule is expressed by the equation `a(b + c) = ab + ac`

### Transformations

Given a multiplication of `a` and `(b + c)`, this rule distributes `a` across `b` and `c`, leaving only the simpler form of `ab` and `ac`.

#### Addition

`a(b + c) = ab + ac`

```
                             +
         *                  / \
        / \                /   \
       /   \              /     \
      a     +     ->     *       *
           / \          / \     / \
          /   \        /   \   /   \
         b     c      a     b a     c
```

### Examples

`rule_tests:distributive_multiply_across`

# API

```python

import mathy_core.rules.distributive_multiply_across
```


## DistributiveMultiplyRule
```python
DistributiveMultiplyRule(self, args, kwargs)
```

Distributive Property
`a(b + c) = ab + ac`

The distributive property can be used to expand out expressions
to allow for simplification, as well as to factor out common properties of terms.

**Distribute across a group**

This handles the `a(b + c)` conversion of the distributive property, which
distributes `a` across both `b` and `c`.

*note: this is useful because it takes a complex Multiply expression and
replaces it with two simpler ones.  This can expose terms that can be
combined for further expression simplification.*

                             +
         *                  / \
        / \                /   \
       /   \              /     \
      a     +     ->     *       *
           / \          / \     / \
          /   \        /   \   /   \
         b     c      a     b a     c

