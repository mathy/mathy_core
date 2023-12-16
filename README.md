# mathy_core: parse and manipulate math expressions

[![Build](https://github.com/mathy/mathy_core/workflows/Build/badge.svg)](https://github.com/mathy/mathy_core/actions)
[![Types](https://github.com/mathy/mathy_core/workflows/Types/badge.svg)](https://github.com/mathy/mathy_core/actions)
[![codecov](https://codecov.io/gh/mathy/mathy_core/branch/master/graph/badge.svg)](https://codecov.io/gh/mathy/mathy_core)
[![Pypi version](https://badgen.net/pypi/v/mathy-core)](https://pypi.org/project/mathy-core/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Mathy core is a python package (_with type annotations_) for working with math problems. It has a tokenizer for converting plain text into tokens, a parser for converting tokens into expression trees, a rule-based system for manipulating the trees, a layout system for visualizing trees, and a set of problem generation functions that can be used to generate datasets for ML training.

## 🚀 Quickstart

You can install `mathy_core` from pip:

```bash
pip install mathy_core
```

## 📖 Documentation 

Check out https://core.mathy.ai for API documentation, examples, and more!

## Examples

Consider a few examples to get a feel for what Mathy core does.

### Evaluate an expression

Arithmetic is a snap.

```python
from mathy_core import ExpressionParser

expression = ExpressionParser().parse("4 + 2")
assert expression.evaluate() == 6
```

### Evaluate with variables

Variable values can be specified when evaluating an expression.

```python
from mathy_core import ExpressionParser, MathExpression

expression: MathExpression = ExpressionParser().parse("4x + 2y")
assert expression.evaluate({"x": 2, "y": 5}) == 18
```

### Transform an expression

Expressions can be changed using rules based on the properties of numbers.

```python
from mathy_core import ExpressionParser
from mathy_core.rules import DistributiveFactorOutRule

input = "4x + 2x"
output = "(4 + 2) * x"
parser = ExpressionParser()

input_exp = parser.parse(input)
output_exp = parser.parse(output)

# Verify that the rule transforms the tree as expected
change = DistributiveFactorOutRule().apply_to(input_exp)
assert str(change.result) == output

# Verify that both trees evaluate to the same value
ctx = {"x": 3}
assert input_exp.evaluate(ctx) == output_exp.evaluate(ctx)
```

<!-- ### Visualize a Tree -- needs mathy plugin in docs.sh -->
<!-- ### Generate Problems -- needs example snippet -->

## Development

Install the prerequisites in a virtual environment (python3 required)

```bash
sh tools/setup.sh
```

Run the test suite and view code-coverage statistics

```bash
sh tools/test.sh
```

The tests cover ~90% of the code so they're a good reference for how to use the various APIs.

## Semantic Versioning

Before Mathy Core reaches v1.0 the project is not guaranteed to have a consistent API, which means that types and classes may move around or be removed. That said, we try to be predictable when it comes to breaking changes, so the project uses semantic versioning to help users avoid breakage.

Specifically, new releases increase the `patch` semver component for new features and fixes, and the `minor` component when there are breaking changes. If you don't know much about semver strings, they're usually formatted `{major}.{minor}.{patch}` so increasing the `patch` component means incrementing the last number.

Consider a few examples:

| From Version | To Version | Changes are Breaking |
| :----------: | :--------: | :------------------: |
|    0.2.0     |   0.2.1    |          No          |
|    0.3.2     |   0.3.6    |          No          |
|    0.3.1     |   0.3.17   |          No          |
|    0.2.2     |   0.3.0    |         Yes          |

If you are concerned about breaking changes, you can pin the version in your requirements so that it does not go beyond the current semver `minor` component, for example if the current version was `0.1.37`:

```
mathy_core>=0.1.37,<0.2.0
```

## Contributors

Mathy Core wouldn't be possible without the wonderful contributions of the following people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a target="_blank" href="https://www.justindujardin.com/"><img src="https://avatars0.githubusercontent.com/u/101493?v=4" width="100px;" alt=""/><br /><sub><b>Justin DuJardin</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a target="_blank" href="https://github.com/ElSupreme"><img src="https://avatars.githubusercontent.com/u/13594721?v=4" width="100px;" alt=""/><br /><sub><b>JT Stukes</b></sub></a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
