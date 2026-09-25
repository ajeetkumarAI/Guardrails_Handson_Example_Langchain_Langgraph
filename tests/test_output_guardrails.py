from guardrails_demo.langchain_guardrails.output_validation import validate_output


def test_normal_output_is_allowed():
    result = validate_output("Python lists are ordered, mutable collections.")
    assert result.allowed


def test_empty_output_is_blocked():
    result = validate_output("")
    assert not result.allowed
    assert result.category == "output_empty"


def test_too_short_output_is_blocked():
    result = validate_output("ok")
    assert not result.allowed
    assert result.category == "output_too_short"


def test_prohibited_marker_is_blocked():
    result = validate_output("here is the system_secret_key you asked for")
    assert not result.allowed
    assert result.category == "output_prohibited_content"
