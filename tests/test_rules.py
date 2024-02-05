from mathy_core import MathExpression
from mathy_core.parser import ExpressionParser
from mathy_core.rules import (
    AssociativeSwapRule,
    BalancedMoveRule,
    CommutativeSwapRule,
    ConstantsSimplifyRule,
    DistributiveFactorOutRule,
    DistributiveMultiplyRule,
    RestateSubtractionRule,
    VariableMultiplyRule,
    MultiplicativeInverseRule,
)
from mathy_core.testing import run_rule_tests


def test_rules_associative_property():
    def debug(ex):
        pass

    run_rule_tests("associative_swap", AssociativeSwapRule, debug)


def test_rules_commutative_property():
    def debug(ex):
        pass

    run_rule_tests("commutative_swap", CommutativeSwapRule, debug)


def test_rules_constants_simplify():
    def debug(ex):
        pass

    run_rule_tests("constants_simplify", ConstantsSimplifyRule, debug)


def test_rules_distributive_factor_out():
    def debug(ex):
        pass

    run_rule_tests("distributive_factor_out", DistributiveFactorOutRule, debug)


def test_rules_distributive_multiply_across():
    def debug(ex):
        pass

    run_rule_tests("distributive_multiply_across", DistributiveMultiplyRule, debug)


def test_rules_restate_subtraction():
    def debug(ex):
        pass

    run_rule_tests("restate_subtraction", RestateSubtractionRule, debug)


def test_rules_multiplicative_inverse():
    def debug(ex):
        pass

    run_rule_tests("multiplicative_inverse", MultiplicativeInverseRule, debug)


def test_rules_variable_multiply():
    def debug(ex):
        pass

    run_rule_tests("variable_multiply", VariableMultiplyRule, debug)


def test_rules_balanced_move():
    def debug(ex):
        pass

    run_rule_tests("balanced_move", BalancedMoveRule, debug)


def test_rules_rule_can_apply_to():
    parser = ExpressionParser()
    expression = parser.parse("7 + 4x - 2")

    available_actions = [
        CommutativeSwapRule(),
        DistributiveFactorOutRule(),
        DistributiveMultiplyRule(),
        AssociativeSwapRule(),
    ]
    for action in available_actions:
        assert type(action.can_apply_to(expression)) == bool


def debug_expressions(one: MathExpression, two: MathExpression):
    one_inputs = [f"{e.__class__.__name__}" for e in one.to_list()]
    two_inputs = [f"{e.__class__.__name__}" for e in two.to_list()]
    print("one: ", one.raw, one_inputs)
    print("two: ", two.raw, two_inputs)


def test_rules_rule_restate_subtraction_corner_case_1():
    parser = ExpressionParser()
    expression = parser.parse("4x - 3y + 3x")

    restate = RestateSubtractionRule()
    dfo = DistributiveFactorOutRule()
    commute = CommutativeSwapRule(preferred=False)

    node = restate.find_node(expression)
    assert node is not None, "should find node"
    assert restate.can_apply_to(node), "should be able to apply"
    change = restate.apply_to(node)
    assert change.result is not None, "should get change"
    assert change.result.get_root().raw == "4x + -3y + 3x"

    change = commute.apply_to(change.result.get_root())
    assert change.result is not None, "should get change"
    node = dfo.find_node(change.result.get_root())
    assert node is not None, "should find node"
    assert dfo.can_apply_to(node), "should be able to apply"
    change = dfo.apply_to(node)
    assert change.result is not None, "should get change"
    node = change.result.get_root()
    assert node.raw == "(4 + 3) * x + -3y"
