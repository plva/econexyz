# demo for issue 54
from hypothesis import strategies as st
from pytest_bdd import given, scenario, then, when


@scenario("features/addition.feature", "add two numbers")
def test_add_two_numbers():
    pass


@given("two integers", target_fixture="numbers")
def numbers():
    return {"a": st.integers().example(), "b": st.integers().example()}


@when("I add them")
def add(numbers):
    numbers["result"] = numbers["a"] + numbers["b"]


@then("the result equals the sum")
def check_sum(numbers):
    assert numbers["result"] == numbers["a"] + numbers["b"]
