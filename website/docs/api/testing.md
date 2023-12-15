```python

import mathy_core.testing
```

## get_rule_tests
```python
get_rule_tests(name: str) -> Dict[str, Any]
```
Load a set of JSON rule test assertions.

__Arguments__

- __name (str)__: The name of the test JSON file to open, e.g. "commutative_property"

__Returns__

`(dict)`: A dictionary with "valid" and "invalid" keys that contain pairs of
expected inputs and outputs.

## init_rule_for_test
```python
init_rule_for_test(
    example: Dict[str, Any], 
    rule_class: Type[mathy_core.rule.BaseRule], 
) -> mathy_core.rule.BaseRule
```
Initialize a given rule_class from a test example.

This handles optionally passing the test example constructor arguments
to the Rule.

__Arguments:__

example (dict): The example assertion loaded from a call to `get_rule_tests`
rule_class (Type[BaseRule]): The

__Returns__

`(BaseRule)`: The rule instance.

## run_rule_tests
```python
run_rule_tests(
    name: str, 
    rule_class: Type[mathy_core.rule.BaseRule], 
    callback: Optional[Callable[[Dict[str, Any]], NoneType]] = None, 
) -> None
```
Load and assert about the transformations and validity of rules
based on given input examples.

When debugging a problem it can be useful to provide a "callback" function
and add a `"debug": true` value to the example in the rules json file you
want to debug. Then you set a breakpoint and step out of your callback function
into the parsing/evaluation of the debug example.
