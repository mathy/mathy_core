# Fraction Reduction

The `Fraction Reduction` rule simplifies fractions by canceling out common factors in the numerator and denominator. This transformation reduces the complexity of expressions and produces equivalent fractions in their simplest form.

This rule implements the mathematical principle that when a factor appears in both the numerator and denominator of a fraction, it can be canceled out: `(a × c) / (b × c) = a / b`

## Operations

**Numeric Fraction Reduction**

This handles cases where the numerator and denominator contain common numeric factors. For example, `6/3` simplifies to `2`.

**Variable Cancellation**

When the same variable appears in both the numerator and denominator, the rule cancels them out:

- If the powers are equal, the variable is removed completely
- If the powers differ, the variable remains with the difference of the exponents

For example:

- `(6x) / (3x)` simplifies to `2`
- `(6x^2) / (3x)` simplifies to `2x`

**Coefficient Reduction**

The rule also handles coefficient reduction in conjunction with variable cancellation. It first factors out common terms, then reduces the numerical coefficient to its simplest form.

For example, `(3x^2) / (6x)` simplifies to `(1/2)x`.

**Exponent Simplification**

When variables with exponents appear in both the numerator and denominator, the rule simplifies by subtracting the exponents.

For example, `x^4 / x^2` simplifies to `x^2`.

## Implementation Details

The rule creates a reduced fraction by:

1. Identifying common factors in the numerator and denominator
2. Reducing the numeric coefficients to their simplest form using GCD
3. Handling variable terms by adjusting their exponents appropriately
4. Constructing a new expression with the simplified terms

### Examples

`rule_tests:fraction_reduction`
