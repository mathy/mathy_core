# mathy_core

<p align="center">
  <a href="/"><img mathy-logo src="/img/mathy_core_logo.png" alt="Mathy Core"></a>
</p>
<p align="center">
    <em>Parse text into trees, visualize them, and make them dance by your rules.</em>
</p>
<p align="center">
<a href="https://github.com/mathy/mathy_core/actions">
    <img src="https://github.com/mathy/mathy_core/workflows/Build/badge.svg" />
</a>
<a href="https://codecov.io/gh/mathy/mathy_core">
    <img src="https://codecov.io/gh/mathy/mathy_core/branch/master/graph/badge.svg?token=CqPEOdEMJX" />
</a>
<a href="https://pypi.org/project/mathy_core" target="_blank">
    <img src="https://badge.fury.io/py/mathy_core.svg" alt="Package version">
</a>
</p>

Mathy includes a Computer Algebra System (or CAS). Its job is to turn text into math trees that can be examined and manipulated by a multi-step process:

1. [Tokenize](./api/tokenizer.md) the text into a list of `type`/`value` pairs
2. [Parse](./api/parser.md) the token list into an Expression tree
3. [Modify](./api/rule.md) the tree by applying a transformation rule to it.

## Requirements

- Python 3.6+

## Installation

```bash
$ pip install mathy_envs
```

## Examples

### Arithmetic

To understand how Mathy's CAS components work, let's add some numbers and assert that the result is what we think it should be.

```Python
{!./snippets/cas/overview/evaluate_expression.py!}
```

### Variables Evaluation

Mathy can also deal with expressions that have variables.

When an expression has variables in it, you can evaluate it by providing the "context" to use:

```Python
{!./snippets/cas/overview/evaluate_expression_variables.py!}
```

### Tree Transformations

Mathy can also transform the parsed Expression trees using rules that change the tree structure without altering the value it outputs when you call `evaluate()`.

```python

{!./snippets/cas/overview/rules_factor_out.py!}

```

## Contributors

Mathy Core wouldn't be possible without the contributions of the following people:

<div class="contributors-wrapper">
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

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
</div>

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome!
