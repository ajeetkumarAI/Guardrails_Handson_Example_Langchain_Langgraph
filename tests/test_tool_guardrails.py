from guardrails_demo.langchain_guardrails.tool_guard import (
    check_tool_allowlist,
    validate_tool_arguments,
    validate_tool_output,
)
from guardrails_demo.schemas import CalculatorArguments


def test_valid_tool_arguments_pass():
    result = validate_tool_arguments(CalculatorArguments, {"operation": "add", "left": 2, "right": 3})
    assert result.allowed


def test_divide_by_zero_is_rejected():
    result = validate_tool_arguments(CalculatorArguments, {"operation": "divide", "left": 4, "right": 0})
    assert not result.allowed


def test_invalid_operation_is_rejected():
    result = validate_tool_arguments(CalculatorArguments, {"operation": "power", "left": 2, "right": 3})
    assert not result.allowed


def test_tool_allowlist_blocks_unknown_tool():
    result = check_tool_allowlist("shell_exec", ["calculator", "weather_lookup"])
    assert not result.allowed


def test_tool_allowlist_allows_known_tool():
    result = check_tool_allowlist("calculator", ["calculator", "weather_lookup"])
    assert result.allowed


def test_tool_output_rejects_empty_result():
    result = validate_tool_output("")
    assert not result.allowed


def test_tool_output_rejects_wrong_type():
    result = validate_tool_output(42, expected_type=str)
    assert not result.allowed
