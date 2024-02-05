import json
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type

from .expressions import EqualExpression, MathExpression
from .parser import ExpressionParser
from .rule import BaseRule
from .util import (
    compare_equation_values,
    compare_expression_string_values,
    compare_expression_values,
)


def get_rule_tests(name: str) -> Dict[str, Any]:
    """Load a set of JSON rule test assertions.

    # Arguments
    name (str): The name of the test JSON file to open, e.g. "commutative_property"

    # Returns
    (dict): A dictionary with "valid" and "invalid" keys that contain pairs of
    expected inputs and outputs.
    """
    rule_file = Path(__file__).parent / "rules" / f"{name}.test.json"
    if not rule_file.is_file() is True:
        raise ValueError(f"does not exist: {rule_file}")
    with open(rule_file, "r") as file:
        return json.load(file)


def init_rule_for_test(example: Dict[str, Any], rule_class: Type[BaseRule]) -> BaseRule:
    """Initialize a given rule_class from a test example.

    This handles optionally passing the test example constructor arguments
    to the Rule.

    # Arguments:
    example (dict): The example assertion loaded from a call to `get_rule_tests`
    rule_class (Type[BaseRule]): The

    # Returns
    (BaseRule): The rule instance.
    """
    if "args" not in example:
        rule = rule_class()
    else:
        rule = rule_class(**example["args"])  # type: ignore
    return rule


def run_rule_tests(
    name: str,
    rule_class: Type[BaseRule],
    callback: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> None:
    """Load and assert about the transformations and validity of rules
    based on given input examples.

    When debugging a problem it can be useful to provide a "callback" function
    and add a `"debug": true` value to the example in the rules json file you
    want to debug. Then you set a breakpoint and step out of your callback function
    into the parsing/evaluation of the debug example.
    """
    tests: Dict[str, Any] = get_rule_tests(name)
    parser = ExpressionParser()
    node: Optional[MathExpression]
    ex: Dict[str, Any]
    for ex in tests["valid"]:
        # Trigger the debug callback so the user can step over into the useful stuff
        if callback is not None:
            callback(ex)
        rule = init_rule_for_test(ex, rule_class)
        assert rule.name is not None, "Rule must have a name"
        assert rule.code is not None, "Rule must have a code"
        expression = parser.parse(ex["input"]).clone()
        before = expression.clone().get_root()
        print(ex)
        target: str
        if "target" in ex:
            target = ex["target"]
            nodes = rule.find_nodes(expression)
            targets = [n.raw for n in nodes]
            nodes = [n for n in nodes if n.raw == target]
            targets_str = "\n".join(targets)
            assert (
                len(nodes) > 0
            ), f"could not find target: {target}. targets are:\n{targets_str}"
            node = nodes[0]
        else:
            node = rule.find_node(expression)

        if node is None:
            assert node is not None, f"expected to find node but did not: {expression}"
        change = rule.apply_to(node)
        assert (
            change.result is not None
        ), f"none result from rule({rule.name}) tree({node})"
        after = change.result.get_root()
        if isinstance(after, (EqualExpression)):
            eval_context = ex.get("eval_context")
            assert eval_context is not None, "Equations require eval_context"
            compare_equation_values(before, after, eval_context=eval_context)
        else:
            # Compare the values of the in-memory expressions output from the rule
            compare_expression_values(before, after)
            # Parse the output strings to new expressions, and compare the values
            compare_expression_string_values(str(before), str(after))
        actual = str(after).strip()
        expected = ex["output"]
        assert actual == expected, f"Expected '{actual}' to be '{expected}'"

    for ex in tests["invalid"]:
        # Trigger the debug callback so the user can step over into the useful stuff
        if callback is not None:
            callback(ex)
        rule = init_rule_for_test(ex, rule_class)
        expression = parser.parse(ex["input"]).clone()
        node = None
        if "target" in ex:
            target = ex["target"]
            nodes = rule.find_nodes(expression)
            nodes = [n for n in nodes if n.raw == target]
            if len(nodes) > 0:
                node = nodes[0]
        else:
            node = rule.find_node(expression)
        if node is not None:
            raise ValueError(
                "expected not to find a node, but found: {}".format(str(node))
            )


__all__ = ("get_rule_tests", "init_rule_for_test", "run_rule_tests")
