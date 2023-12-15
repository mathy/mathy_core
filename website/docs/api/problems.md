# mathy_core.problems
Problem Generation
---

Utility functions for helping generate input problems.

## DefaultType
Template type for a default return value
## gen_binomial_times_binomial
```python
gen_binomial_times_binomial(
    op: str = '+', 
    min_vars: int = 1, 
    max_vars: int = 2, 
    simple_variables: bool = True, 
    powers_probability: float = 0.33, 
    like_variables_probability: float = 1.0, 
) -> Tuple[str, int]
```
Generate a binomial multiplied by another binomial.

__Example__


```
(2e + 12p)(16 + 7e)
```

`mathy:(2e + 12p)(16 + 7e)`

## gen_binomial_times_monomial
```python
gen_binomial_times_monomial(
    op: str = '+', 
    min_vars: int = 1, 
    max_vars: int = 2, 
    simple_variables: bool = True, 
    powers_probability: float = 0.33, 
    like_variables_probability: float = 1.0, 
) -> Tuple[str, int]
```
Generate a binomial multiplied by a monomial.

__Example__


```
(4x^3 + y) * 2x
```

`mathy:(4x^3 + y) * 2x`

## gen_combine_terms_in_place
```python
gen_combine_terms_in_place(
    min_terms: int = 16, 
    max_terms: int = 26, 
    easy: bool = True, 
    powers: bool = False, 
) -> Tuple[str, int]
```
Generate a problem that puts one pair of like terms next to each other
somewhere inside a large tree of unlike terms.

The problem is intended to be solved in a very small number of moves, making
training across many episodes relatively quick, and reducing the combinatorial
explosion of branches that need to be searched to solve the task.

The hope is that by focusing the agent on selecting the right moves inside of a
ridiculously large expression it will learn to select actions to combine like terms
invariant of the sequence length.

__Example__


```
4y + 12j + 73q + 19k + 13z + 56l + (24x + 12x) + 43n + 17j
```

`mathy:4y + 12j + 73q + 19k + 13z + 56l + (24x + 12x) + 43n + 17j`


## gen_commute_haystack
```python
gen_commute_haystack(
    min_terms: int = 5, 
    max_terms: int = 8, 
    commute_blockers: int = 1, 
    easy: bool = True, 
    powers: bool = False, 
) -> Tuple[str, int]
```
A problem with a bunch of terms that have no matches, and a single
set of two terms that do match, but are separated by one other term.
The challenge is to commute the terms to each other in one move.

__Example__


```
4y + 12j + 73q + 19k + 13z + 24x + 56l + 12x  + 43n + 17j"
                              ^-----------^
```

`mathy:4y + 12j + 73q + 19k + 13z + 24x + 56l + 12x  + 43n + 17j`

## gen_move_around_blockers_one
```python
gen_move_around_blockers_one(
    number_blockers: int, 
    powers_probability: float = 0.5, 
) -> Tuple[str, int]
```
Two like terms separated by (n) blocker terms.

__Example__


```
4x + (y + f) + x
```

`mathy:4x + (y + f) + x`
## gen_move_around_blockers_two
```python
gen_move_around_blockers_two(
    number_blockers: int, 
    powers_probability: float = 0.5, 
) -> Tuple[str, int]
```
Two like terms with three blockers.

__Example__


```
7a + 4x + (2f + j) + x + 3d
```

`mathy:7a + 4x + (2f + j) + x + 3d`
## gen_simplify_multiple_terms
```python
gen_simplify_multiple_terms(
    num_terms: int, 
    optional_var: bool = False, 
    op: Optional[List[str], str] = None, 
    common_variables: bool = True, 
    inner_terms_scaling: float = 0.3, 
    powers_probability: float = 0.33, 
    optional_var_probability: float = 0.8, 
    noise_probability: float = 0.8, 
    shuffle_probability: float = 0.66, 
    share_var_probability: float = 0.5, 
    grouping_noise_probability: float = 0.66, 
    noise_terms: Optional[int] = None, 
) -> Tuple[str, int]
```
Generate a polynomial problem with like terms that need to be combined and
simplified.

__Example__


```
2a + 3j - 7b + 17.2a + j
```

`mathy:2a + 3j - 7b + 17.2a + j`

## get_blocker
```python
get_blocker(
    num_blockers: int = 1, 
    exclude_vars: Optional[List[str]] = None, 
) -> str
```
Get a string of terms to place between target simplification terms
in order to challenge the agent's ability to use commutative/associative
rules to move terms around.
## get_rand_vars
```python
get_rand_vars(
    num_vars: int, 
    exclude_vars: Optional[List[str]] = None, 
    common_variables: bool = False, 
) -> List[str]
```
Get a list of random variables, excluding the given list of hold-out variables
## MathyTermTemplate
```python
MathyTermTemplate(
    self, 
    variable: Optional[str] = None, 
    exponent: Optional[float, int] = None, 
) -> None
```
MathyTermTemplate(variable: Optional[str] = None, exponent: Union[float, int, NoneType] = None)
## split_in_two_random
```python
split_in_two_random(value: int) -> Tuple[int, int]
```
Split a given number into two smaller numbers that sum to it.
Returns: a tuple of (lower, higher) numbers that sum to the input

## use_pretty_numbers
```python
use_pretty_numbers(enabled: bool = True) -> None
```
Determine if problems should include only pretty numbers or
a whole range of integers and floats. Using pretty numbers will
restrict the numbers that are generated to integers between 1 and
12. When not using pretty numbers, floats and large integers will
be included in the output from `rand_number`
