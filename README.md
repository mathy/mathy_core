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

## 🎛 API

<!-- NOTE: The below code is auto-generated. Update source files to change API documentation. -->
<!-- AUTO_DOCZ_START -->

# Tokenizer <kbd>class</kbd>

```python (doc)
Tokenizer(self, exclude_padding: bool = True)
```

The Tokenizer produces a list of tokens from an input string.

## eat_token <kbd>method</kbd>

```python (doc)
Tokenizer.eat_token(
    self,
    context: mathy_core.tokenizer.TokenContext,
    typeFn: Callable[[str], bool],
) -> str
```

Eat all of the tokens of a given type from the front of the stream
until a different type is hit, and return the text.

## identify_alphas <kbd>method</kbd>

```python (doc)
Tokenizer.identify_alphas(
    self,
    context: mathy_core.tokenizer.TokenContext,
) -> int
```

Identify and tokenize functions and variables.

## identify_constants <kbd>method</kbd>

```python (doc)
Tokenizer.identify_constants(
    self,
    context: mathy_core.tokenizer.TokenContext,
) -> int
```

Identify and tokenize a constant number.

## identify_operators <kbd>method</kbd>

```python (doc)
Tokenizer.identify_operators(
    self,
    context: mathy_core.tokenizer.TokenContext,
) -> bool
```

Identify and tokenize operators.

## is_alpha <kbd>method</kbd>

```python (doc)
Tokenizer.is_alpha(self, c: str) -> bool
```

Is this character a letter

## is_number <kbd>method</kbd>

```python (doc)
Tokenizer.is_number(self, c: str) -> bool
```

Is this character a number

## tokenize <kbd>method</kbd>

```python (doc)
Tokenizer.tokenize(self, buffer: str) -> List[mathy_core.tokenizer.Token]
```

Return an array of `Token`s from a given string input.
This throws an exception if an unknown token type is found in the input.

# mathy_core.parser

## ExpressionParser <kbd>class</kbd>

```python (doc)
ExpressionParser(self) -> None
```

Parser for converting text into binary trees. Trees encode the order of
operations for an input, and allow evaluating it to detemrine the expression
value.

### Grammar Rules

Symbols:

```
( )    == Non-terminal
{ }*   == 0 or more occurrences
{ }+   == 1 or more occurrences
{ }?   == 0 or 1 occurrences
[ ]    == Mandatory (1 must occur)
|      == logical OR
" "    == Terminal symbol (literal)
```

Non-terminals defined/parsed by Tokenizer:

```
(Constant) = anything that can be parsed by `float(in)`
(Variable) = any string containing only letters (a-z and A-Z)
```

Rules:

```
(Function)     = [ functionName ] "(" (AddExp) ")"
(Factor)       = { (Variable) | (Function) | "(" (AddExp) ")" }+ { { "^" }? (UnaryExp) }?
(FactorPrefix) = [ (Constant) { (Factor) }? | (Factor) ]
(UnaryExp)     = { "-" }? (FactorPrefix)
(ExpExp)       = (UnaryExp) { { "^" }? (UnaryExp) }?
(MultExp)      = (ExpExp) { { "*" | "/" }? (ExpExp) }*
(AddExp)       = (MultExp) { { "+" | "-" }? (MultExp) }*
(EqualExp)     = (AddExp) { { "=" }? (AddExp) }*
(start)        = (EqualExp)
```

### check <kbd>method</kbd>

```python (doc)
ExpressionParser.check(
    self,
    tokens: mathy_core.parser.TokenSet,
    do_assert: bool = False,
) -> bool
```

Check if the `self.current_token` is a member of a set Token types

Args: - `tokens` The set of Token types to check against

`Returns` True if the `current_token`'s type is in the set else False

### eat <kbd>method</kbd>

```python (doc)
ExpressionParser.eat(self, type: int) -> bool
```

Assign the next token in the queue to current_token if its type
matches that of the specified parameter. If the type does not match,
raise a syntax exception.

Args: - `type` The type that your syntax expects @current_token to be

### next <kbd>method</kbd>

```python (doc)
ExpressionParser.next(self) -> bool
```

Assign the next token in the queue to `self.current_token`.

Return True if there are still more tokens in the queue, or False if there
are no more tokens to look at.

### parse <kbd>method</kbd>

```python (doc)
ExpressionParser.parse(
    self,
    input_text: str,
) -> mathy_core.expressions.MathExpression
```

Parse a string representation of an expression into a tree
that can be later evaluated.

Returns : The evaluatable expression tree.

## TokenSet <kbd>class</kbd>

```python (doc)
TokenSet(self, source: int)
```

TokenSet objects are bitmask combinations for checking to see
if a token is part of a valid set.

### add <kbd>method</kbd>

```python (doc)
TokenSet.add(self, addTokens: int) -> 'TokenSet'
```

Add tokens to self set and return a TokenSet representing
their combination of flags. Value can be an integer or an instance
of `TokenSet`

### contains <kbd>method</kbd>

```python (doc)
TokenSet.contains(self, type: int) -> bool
```

Returns true if the given type is part of this set

# mathy_core.tree

## BinaryTreeNode <kbd>class</kbd>

```python (doc)
BinaryTreeNode(
    self,
    left: Optional[BinaryTreeNode] = None,
    right: Optional[BinaryTreeNode] = None,
    parent: Optional[BinaryTreeNode] = None,
    id: Optional[str] = None,
)
```

The binary tree node is the base node for all of our trees, and provides a
rich set of methods for constructing, inspecting, and modifying them.
The node itself defines the structure of the binary tree, having left and right
children, and a parent.

### clone <kbd>method</kbd>

```python (doc)
BinaryTreeNode.clone(self: ~NodeType) -> ~NodeType
```

Create a clone of this tree

### get_children <kbd>method</kbd>

```python (doc)
BinaryTreeNode.get_children(self: ~NodeType) -> List[~NodeType]
```

Get children as an array. If there are two children, the first object will
always represent the left child, and the second will represent the right.

### get_root <kbd>method</kbd>

```python (doc)
BinaryTreeNode.get_root(self: ~NodeType) -> ~NodeType
```

Return the root element of this tree

### get_root_side <kbd>method</kbd>

```python (doc)
BinaryTreeNode.get_root_side(
    self: 'BinaryTreeNode',
) -> typing_extensions.Literal['left', 'right']
```

Return the side of the tree that this node lives on

### get_sibling <kbd>method</kbd>

```python (doc)
BinaryTreeNode.get_sibling(self: ~NodeType) -> Optional[~NodeType]
```

Get the sibling node of this node. If there is no parent, or the node
has no sibling, the return value will be None.

### get_side <kbd>method</kbd>

```python (doc)
BinaryTreeNode.get_side(
    self,
    child: Optional[BinaryTreeNode],
) -> typing_extensions.Literal['left', 'right']
```

Determine whether the given `child` is the left or right child of this
node

### is_leaf <kbd>method</kbd>

```python (doc)
BinaryTreeNode.is_leaf(self) -> bool
```

Is this node a leaf? A node is a leaf if it has no children.

### rotate <kbd>method</kbd>

```python (doc)
BinaryTreeNode.rotate(self: ~NodeType) -> ~NodeType
```

Rotate a node, changing the structure of the tree, without modifying
the order of the nodes in the tree.

### set_left <kbd>method</kbd>

```python (doc)
BinaryTreeNode.set_left(
    self: ~NodeType,
    child: Optional[BinaryTreeNode] = None,
    clear_old_child_parent: bool = False,
) -> ~NodeType
```

Set the left node to the passed `child`

### set_right <kbd>method</kbd>

```python (doc)
BinaryTreeNode.set_right(
    self: ~NodeType,
    child: Optional[BinaryTreeNode] = None,
    clear_old_child_parent: bool = False,
) -> ~NodeType
```

Set the right node to the passed `child`

### set_side <kbd>method</kbd>

```python (doc)
BinaryTreeNode.set_side(
    self,
    child: ~NodeType,
    side: typing_extensions.Literal['left', 'right'],
) -> ~NodeType
```

Set a new `child` on the given `side`

### visit_inorder <kbd>method</kbd>

```python (doc)
BinaryTreeNode.visit_inorder(
    self,
    visit_fn: Callable[[Any, int, Optional[Any]], Optional[typing_extensions.Literal['stop']]],
    depth: int = 0,
    data: Optional[Any] = None,
) -> Optional[typing_extensions.Literal['stop']]
```

Visit the tree inorder, which visits the left child, then the current node,
and then its right child.

_Left -> Visit -> Right_

This method accepts a function that will be invoked for each node in the
tree. The callback function is passed three arguments: the node being
visited, the current depth in the tree, and a user specified data parameter.

!!! info

    Traversals may be canceled by returning `STOP` from any visit function.

### visit_postorder <kbd>method</kbd>

```python (doc)
BinaryTreeNode.visit_postorder(
    self,
    visit_fn: Callable[[Any, int, Optional[Any]], Optional[typing_extensions.Literal['stop']]],
    depth: int = 0,
    data: Optional[Any] = None,
) -> Optional[typing_extensions.Literal['stop']]
```

Visit the tree postorder, which visits its left child, then its right child,
and finally the current node.

_Left -> Right -> Visit_

This method accepts a function that will be invoked for each node in the
tree. The callback function is passed three arguments: the node being
visited, the current depth in the tree, and a user specified data parameter.

!!! info

    Traversals may be canceled by returning `STOP` from any visit function.

### visit_preorder <kbd>method</kbd>

```python (doc)
BinaryTreeNode.visit_preorder(
    self,
    visit_fn: Callable[[Any, int, Optional[Any]], Optional[typing_extensions.Literal['stop']]],
    depth: int = 0,
    data: Optional[Any] = None,
) -> Optional[typing_extensions.Literal['stop']]
```

Visit the tree preorder, which visits the current node, then its left
child, and then its right child.

_Visit -> Left -> Right_

This method accepts a function that will be invoked for each node in the
tree. The callback function is passed three arguments: the node being
visited, the current depth in the tree, and a user specified data parameter.

!!! info

    Traversals may be canceled by returning `STOP` from any visit function.

## NodeType

Template type that inherits from BinaryTreeNode.

## VisitDataType

Template type of user data passed to visit functions.

# mathy_core.expressions

## AbsExpression <kbd>class</kbd>

```python (doc)
AbsExpression(
    self,
    child: Optional[mathy_core.expressions.MathExpression] = None,
    child_on_left: bool = False,
)
```

Evaluates the absolute value of an expression.

## AddExpression <kbd>class</kbd>

```python (doc)
AddExpression(
    self,
    left: Optional[mathy_core.expressions.MathExpression] = None,
    right: Optional[mathy_core.expressions.MathExpression] = None,
)
```

Add one and two

## BinaryExpression <kbd>class</kbd>

```python (doc)
BinaryExpression(
    self,
    left: Optional[mathy_core.expressions.MathExpression] = None,
    right: Optional[mathy_core.expressions.MathExpression] = None,
)
```

An expression that operates on two sub-expressions

### get_priority <kbd>method</kbd>

```python (doc)
BinaryExpression.get_priority(self) -> int
```

Return a number representing the order of operations priority
of this node. This can be used to check if a node is `locked`
with respect to another node, i.e. the other node must be resolved
first during evaluation because of it's priority.

### to_math_ml_fragment <kbd>method</kbd>

```python (doc)
BinaryExpression.to_math_ml_fragment(self) -> str
```

Render this node as a MathML element fragment

## ConstantExpression <kbd>class</kbd>

```python (doc)
ConstantExpression(self, value: Optional[int, float] = None)
```

A Constant value node, where the value is accessible as `node.value`

## DivideExpression <kbd>class</kbd>

```python (doc)
DivideExpression(
    self,
    left: Optional[mathy_core.expressions.MathExpression] = None,
    right: Optional[mathy_core.expressions.MathExpression] = None,
)
```

Divide one by two

## EqualExpression <kbd>class</kbd>

```python (doc)
EqualExpression(
    self,
    left: Optional[mathy_core.expressions.MathExpression] = None,
    right: Optional[mathy_core.expressions.MathExpression] = None,
)
```

Evaluate equality of two expressions

### operate <kbd>method</kbd>

```python (doc)
EqualExpression.operate(
    self,
    one: Union[float, int],
    two: Union[float, int],
) -> Union[float, int]
```

Return the value of the equation if one == two.

Raise ValueError if both sides of the equation don't agree.

## FactorialExpression <kbd>class</kbd>

```python (doc)
FactorialExpression(
    self,
    child: Optional[mathy_core.expressions.MathExpression] = None,
    child_on_left: bool = False,
)
```

Factorial of a constant, e.g. `5` evaluates to `120`

## FunctionExpression <kbd>class</kbd>

```python (doc)
FunctionExpression(
    self,
    child: Optional[mathy_core.expressions.MathExpression] = None,
    child_on_left: bool = False,
)
```

A Specialized UnaryExpression that is used for functions. The function name in
text (used by the parser and tokenizer) is derived from the name() method on the
class.

## MathExpression <kbd>class</kbd>

```python (doc)
MathExpression(
    self,
    id: Optional[str] = None,
    left: Optional[MathExpression] = None,
    right: Optional[MathExpression] = None,
    parent: Optional[MathExpression] = None,
)
```

Math tree node with helpers for manipulating expressions.

`mathy:x+y=z`

### add_class <kbd>method</kbd>

```python (doc)
MathExpression.add_class(
    self,
    classes: Union[List[str], str],
) -> 'MathExpression'
```

Associate a class name with an expression. This class name will be
attached to nodes when the expression is converted to a capable output
format.

See `MathExpression.to_math_ml_fragment`

### all_changed <kbd>method</kbd>

```python (doc)
MathExpression.all_changed(self) -> None
```

Mark this node and all of its children as changed

### clear_classes <kbd>method</kbd>

```python (doc)
MathExpression.clear_classes(self) -> None
```

Clear all the classes currently set on the nodes in this expression.

### clone <kbd>method</kbd>

```python (doc)
MathExpression.clone(self) -> 'MathExpression'
```

A specialization of the clone method that can track and report a cloned
subtree node.

See `MathExpression.clone_from_root` for more details.

### clone_from_root <kbd>method</kbd>

```python (doc)
MathExpression.clone_from_root(
    self,
    node: Optional[MathExpression] = None,
) -> 'MathExpression'
```

Clone this node including the entire parent hierarchy that it has. This
is useful when you want to clone a subtree and still maintain the overall
hierarchy.

**Arguments**

- **node (MathExpression)**: The node to clone.

**Returns**

`(MathExpression)`: The cloned node.

### color

Color to use for this node when rendering it as changed with
`.terminal_text`

### evaluate <kbd>method</kbd>

```python (doc)
MathExpression.evaluate(
    self,
    context: Union[Dict[str, Optional[float, int]]] = None,
) -> Union[float, int]
```

Evaluate the expression, resolving all variables to constant values

### find_id <kbd>method</kbd>

```python (doc)
MathExpression.find_id(
    self,
    id: str,
) -> Optional[MathExpression]
```

Find an expression by its unique ID.

Returns: The found `MathExpression` or `None`

### find_type <kbd>method</kbd>

```python (doc)
MathExpression.find_type(self, instanceType: Type[~NodeType]) -> List[~NodeType]
```

Find an expression in this tree by type.

- instanceType: The type to check for instances of

Returns the found `MathExpression` objects of the given type.

### make_ml_tag <kbd>method</kbd>

```python (doc)
MathExpression.make_ml_tag(
    self,
    tag: str,
    content: str,
    classes: List[str] = [],
) -> str
```

Make a MathML tag for the given content while respecting the node's given
classes.

**Arguments**

- **tag (str)**: The ML tag name to create.
- **content (str)**: The ML content to place inside of the tag.
  classes (List[str]) An array of classes to attach to this tag.

**Returns**

`(str)`: A MathML element with the given tag, content, and classes

### path_to_root <kbd>method</kbd>

```python (doc)
MathExpression.path_to_root(self) -> str
```

Generate a namespaced path key to from the current node to the root.
This key can be used to identify a node inside of a tree.

### raw

raw text representation of the expression.

### set_changed <kbd>method</kbd>

```python (doc)
MathExpression.set_changed(self) -> None
```

Mark this node as having been changed by the application of a Rule

### terminal_text

Text output of this node that includes terminal color codes that
highlight which nodes have been changed in this tree as a result of
a transformation.

### to_list <kbd>method</kbd>

```python (doc)
MathExpression.to_list(
    self,
    visit: str = 'preorder',
) -> List[MathExpression]
```

Convert this node hierarchy into a list.

### to_math_ml <kbd>method</kbd>

```python (doc)
MathExpression.to_math_ml(self) -> str
```

Convert this expression into a MathML container.

### to_math_ml_fragment <kbd>method</kbd>

```python (doc)
MathExpression.to_math_ml_fragment(self) -> str
```

Convert this single node into MathML.

### with_color <kbd>method</kbd>

```python (doc)
MathExpression.with_color(self, text: str, style: str = 'bright') -> str
```

Render a string that is colored if something has changed

## MultiplyExpression <kbd>class</kbd>

```python (doc)
MultiplyExpression(
    self,
    left: Optional[mathy_core.expressions.MathExpression] = None,
    right: Optional[mathy_core.expressions.MathExpression] = None,
)
```

Multiply one and two

## NegateExpression <kbd>class</kbd>

```python (doc)
NegateExpression(
    self,
    child: Optional[mathy_core.expressions.MathExpression] = None,
    child_on_left: bool = False,
)
```

Negate an expression, e.g. `4` becomes `-4`

### to_math_ml_fragment <kbd>method</kbd>

```python (doc)
NegateExpression.to_math_ml_fragment(self) -> str
```

Convert this single node into MathML.

## PowerExpression <kbd>class</kbd>

```python (doc)
PowerExpression(
    self,
    left: Optional[mathy_core.expressions.MathExpression] = None,
    right: Optional[mathy_core.expressions.MathExpression] = None,
)
```

Raise one to the power of two

## SgnExpression <kbd>class</kbd>

```python (doc)
SgnExpression(
    self,
    child: Optional[mathy_core.expressions.MathExpression] = None,
    child_on_left: bool = False,
)
```

### operate <kbd>method</kbd>

```python (doc)
SgnExpression.operate(self, value: Union[float, int]) -> Union[float, int]
```

Determine the sign of an value.

**Returns**

`(int)`: -1 if negative, 1 if positive, 0 if 0

## SubtractExpression <kbd>class</kbd>

```python (doc)
SubtractExpression(
    self,
    left: Optional[mathy_core.expressions.MathExpression] = None,
    right: Optional[mathy_core.expressions.MathExpression] = None,
)
```

Subtract one from two

## UnaryExpression <kbd>class</kbd>

```python (doc)
UnaryExpression(
    self,
    child: Optional[mathy_core.expressions.MathExpression] = None,
    child_on_left: bool = False,
)
```

An expression that operates on one sub-expression

# mathy_core.rules.associative_swap

## AssociativeSwapRule <kbd>class</kbd>

```python (doc)
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

# mathy_core.rules.balanced_move

## BalancedMoveRule <kbd>class</kbd>

```python (doc)
BalancedMoveRule(self, args, kwargs)
```

Balanced rewrite rule moves nodes from one side of an equation
to the other by performing the same operation on both sides.

Addition: `a + 2 = 3` -> `a + 2 = 3 - 2`
Multiplication: `3a = 3` -> `3a / 3 = 3 / 3`

### get_type <kbd>method</kbd>

```python (doc)
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

# mathy_core.rules.commutative_swap

## CommutativeSwapRule <kbd>class</kbd>

```python (doc)
CommutativeSwapRule(self, preferred: bool = True)
```

Commutative Property
For Addition: `a + b = b + a`

         +                  +
        / \                / \
       /   \     ->       /   \
      /     \            /     \
     a       b          b       a

For Multiplication: `a * b = b * a`

         *                  *
        / \                / \
       /   \     ->       /   \
      /     \            /     \
     a       b          b       a

# mathy_core.rules.constants_simplify

## ConstantsSimplifyRule <kbd>class</kbd>

```python (doc)
ConstantsSimplifyRule(self, args, kwargs)
```

Given a binary operation on two constants, simplify to the resulting
constant expression

### get_type <kbd>method</kbd>

```python (doc)
ConstantsSimplifyRule.get_type(
    self,
    node: mathy_core.expressions.MathExpression,
) -> Optional[Tuple[str, mathy_core.expressions.ConstantExpression, mathy_core.expressions.ConstantExpression]]
```

Determine the configuration of the tree for this transformation.

Support the three types of tree configurations:

- Simple is where the node's left and right children are exactly
  constants linked by an add operation.
- Chained Right is where the node's left child is a constant, but the right
  child is another binary operation of the same type. In this case the left
  child of the next binary node is the target.

Structure:

- Simple
  - node(add),node.left(const),node.right(const)
- Chained Right
  - node(add),node.left(const),node.right(add),node.right.left(const)
- Chained Right Deep
  - node(add),node.left(const),node.right(add),node.right.left(const)

# mathy_core.rules.distributive_factor_out

## DistributiveFactorOutRule <kbd>class</kbd>

```python (doc)
DistributiveFactorOutRule(self, constants: bool = False)
```

Distributive Property
`ab + ac = a(b + c)`

The distributive property can be used to expand out expressions
to allow for simplification, as well as to factor out common properties
of terms.

**Factor out a common term**

This handles the `ab + ac` conversion of the distributive property, which
factors out a common term from the given two addition operands.

           +               *
          / \             / \
         /   \           /   \
        /     \    ->   /     \
       *       *       a       +
      / \     / \             / \
     a   b   a   c           b   c

### get_type <kbd>method</kbd>

```python (doc)
DistributiveFactorOutRule.get_type(
    self,
    node: mathy_core.expressions.MathExpression,
) -> Optional[Tuple[str, mathy_core.util.TermEx, mathy_core.util.TermEx]]
```

Determine the configuration of the tree for this transformation.

Support the three types of tree configurations:

- Simple is where the node's left and right children are exactly
  terms linked by an add operation.
- Chained Left is where the node's left child is a term, but the right
  child is another add operation. In this case the left child
  of the next add node is the target.
- Chained Right is where the node's right child is a term, but the left
  child is another add operation. In this case the right child
  of the child add node is the target.

Structure:

- Simple
  - node(add),node.left(term),node.right(term)
- Chained Left
  - node(add),node.left(term),node.right(add),node.right.left(term)
- Chained Right
  - node(add),node.right(term),node.left(add),node.left.right(term)

# mathy_core.rules.distributive_multiply_across

## DistributiveMultiplyRule <kbd>class</kbd>

```python (doc)
DistributiveMultiplyRule(self, args, kwargs)
```

Distributive Property
`a(b + c) = ab + ac`

The distributive property can be used to expand out expressions
to allow for simplification, as well as to factor out common properties of terms.

**Distribute across a group**

This handles the `a(b + c)` conversion of the distributive property, which
distributes `a` across both `b` and `c`.

_note: this is useful because it takes a complex Multiply expression and
replaces it with two simpler ones. This can expose terms that can be
combined for further expression simplification._

                             +
         *                  / \
        / \                /   \
       /   \              /     \
      a     +     ->     *       *
           / \          / \     / \
          /   \        /   \   /   \
         b     c      a     b a     c

# mathy_core.rules.variable_multiply

## VariableMultiplyRule <kbd>class</kbd>

```python (doc)
VariableMultiplyRule(self, args, kwargs)
```

This restates `x^b * x^d` as `x^(b + d)` which has the effect of isolating
the exponents attached to the variables, so they can be combined.

    1. When there are two terms with the same base being multiplied together, their
       exponents are added together. "x * x^3" = "x^4" because "x = x^1" so
       "x^1 * x^3 = x^(1 + 3) = x^4"

    TODO: 2. When there is a power raised to another power, they can be combined by
             multiplying the exponents together. "x^(2^2) = x^4"

The rule identifies terms with explicit and implicit powers, so the following
transformations are all valid:

Explicit powers: x^b \* x^d = x^(b+d)

          *
         / \
        /   \          ^
       /     \    =   / \
      ^       ^      x   +
     / \     / \        / \
    x   b   x   d      b   d

Implicit powers: x \* x^d = x^(1 + d)

        *
       / \
      /   \          ^
     /     \    =   / \
    x       ^      x   +
           / \        / \
          x   d      1   d

### get_type <kbd>method</kbd>

```python (doc)
VariableMultiplyRule.get_type(
    self,
    node: mathy_core.expressions.MathExpression,
) -> Optional[Tuple[str, mathy_core.util.TermEx, mathy_core.util.TermEx]]
```

Determine the configuration of the tree for this transformation.

Support two types of tree configurations:

- Simple is where the node's left and right children are exactly
  terms that can be multiplied together.
- Chained is where the node's left child is a term, but the right
  child is a continuation of a more complex term, as indicated by
  the presence of another Multiply node. In this case the left child
  of the next multiply node is the target.

Structure:

- Simple node(mult),node.left(term),node.right(term)
- Chained node(mult),node.left(term),node.right(mult),node.right.left(term)

# mathy_core.layout

## TreeLayout <kbd>class</kbd>

```python (doc)
TreeLayout(self, args, kwargs)
```

Calculate a visual layout for input trees.

### layout <kbd>method</kbd>

```python (doc)
TreeLayout.layout(
    self,
    node: mathy_core.tree.BinaryTreeNode,
    unit_x_multiplier: float = 1.0,
    unit_y_multiplier: float = 1.0,
) -> 'TreeMeasurement'
```

Assign x/y values to all nodes in the tree, and return an object containing
the measurements of the tree.

Returns a TreeMeasurement object that describes the bounds of the tree

### transform <kbd>method</kbd>

```python (doc)
TreeLayout.transform(
    self,
    node: mathy_core.tree.BinaryTreeNode = None,
    x: float = 0,
    unit_x_multiplier: float = 1,
    unit_y_multiplier: float = 1,
    measure: Optional[TreeMeasurement] = None,
) -> 'TreeMeasurement'
```

Transform relative to absolute coordinates, and measure the bounds of the tree.

Return a measurement of the tree in output units.

## TreeMeasurement <kbd>class</kbd>

```python (doc)
TreeMeasurement(self) -> None
```

Summary of the rendered tree

# mathy_core.problems

## Problem Generation

Utility functions for helping generate input problems.

## DefaultType

Template type for a default return value

## gen_binomial_times_binomial <kbd>function</kbd>

```python (doc)
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

**Example**

```
(2e + 12p)(16 + 7e)
```

`mathy:(2e + 12p)(16 + 7e)`

## gen_binomial_times_monomial <kbd>function</kbd>

```python (doc)
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

**Example**

```
(4x^3 + y) * 2x
```

`mathy:(4x^3 + y) * 2x`

## gen_combine_terms_in_place <kbd>function</kbd>

```python (doc)
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

**Example**

```
4y + 12j + 73q + 19k + 13z + 56l + (24x + 12x) + 43n + 17j
```

`mathy:4y + 12j + 73q + 19k + 13z + 56l + (24x + 12x) + 43n + 17j`

## gen_commute_haystack <kbd>function</kbd>

```python (doc)
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

**Example**

```
4y + 12j + 73q + 19k + 13z + 24x + 56l + 12x  + 43n + 17j"
                              ^-----------^
```

`mathy:4y + 12j + 73q + 19k + 13z + 24x + 56l + 12x + 43n + 17j`

## gen_move_around_blockers_one <kbd>function</kbd>

```python (doc)
gen_move_around_blockers_one(
    number_blockers: int,
    powers_probability: float = 0.5,
) -> Tuple[str, int]
```

Two like terms separated by (n) blocker terms.

**Example**

```
4x + (y + f) + x
```

`mathy:4x + (y + f) + x`

## gen_move_around_blockers_two <kbd>function</kbd>

```python (doc)
gen_move_around_blockers_two(
    number_blockers: int,
    powers_probability: float = 0.5,
) -> Tuple[str, int]
```

Two like terms with three blockers.

**Example**

```
7a + 4x + (2f + j) + x + 3d
```

`mathy:7a + 4x + (2f + j) + x + 3d`

## gen_simplify_multiple_terms <kbd>function</kbd>

```python (doc)
gen_simplify_multiple_terms(
    num_terms: int,
    optional_var: bool = False,
    op: Union[List[str], str] = None,
    common_variables: bool = True,
    inner_terms_scaling: float = 0.3,
    powers_probability: float = 0.33,
    optional_var_probability: float = 0.8,
    noise_probability: float = 0.8,
    shuffle_probability: float = 0.66,
    share_var_probability: float = 0.5,
    grouping_noise_probability: float = 0.66,
    noise_terms: int = None,
) -> Tuple[str, int]
```

Generate a polynomial problem with like terms that need to be combined and
simplified.

**Example**

```
2a + 3j - 7b + 17.2a + j
```

`mathy:2a + 3j - 7b + 17.2a + j`

## get_blocker <kbd>function</kbd>

```python (doc)
get_blocker(
    num_blockers: int = 1,
    exclude_vars: Optional[List[str]] = None,
) -> str
```

Get a string of terms to place between target simplification terms
in order to challenge the agent's ability to use commutative/associative
rules to move terms around.

## get_rand_vars <kbd>function</kbd>

```python (doc)
get_rand_vars(
    num_vars: int,
    exclude_vars: Optional[List[str]] = None,
    common_variables: bool = False,
) -> List[str]
```

Get a list of random variables, excluding the given list of hold-out variables

## split_in_two_random <kbd>function</kbd>

```python (doc)
split_in_two_random(value: int) -> Tuple[int, int]
```

Split a given number into two smaller numbers that sum to it.
Returns: a tuple of (lower, higher) numbers that sum to the input

## use_pretty_numbers <kbd>function</kbd>

```python (doc)
use_pretty_numbers(enabled: bool = True) -> None
```

Determine if problems should include only pretty numbers or
a whole range of integers and floats. Using pretty numbers will
restrict the numbers that are generated to integers between 1 and 12. When not using pretty numbers, floats and large integers will
be included in the output from `rand_number`

<!-- AUTO_DOCZ_END -->

## Contributors

Mathy Core wouldn't be possible without the wonderful contributions of the following people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a target="_blank" href="https://www.justindujardin.com/"><img src="https://avatars0.githubusercontent.com/u/101493?v=4" width="100px;" alt=""/><br /><sub><b>Justin DuJardin</b></sub></a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
