from guardrails_demo.langchain_guardrails.input_validation import validate_input


def test_valid_input_is_allowed():
    result = validate_input("What is a Python list?")
    assert result.allowed


def test_empty_input_is_blocked():
    result = validate_input("")
    assert not result.allowed
    assert result.category == "input_empty"


def test_oversized_input_is_blocked():
    result = validate_input("x" * 3000)
    assert not result.allowed
    assert result.category == "input_too_long"


def test_wrong_type_is_blocked():
    result = validate_input(12345)
    assert not result.allowed
    assert result.category == "input_wrong_type"


def test_too_short_input_is_blocked():
    result = validate_input("a", min_length=2)
    assert not result.allowed
    assert result.category == "input_too_short"
