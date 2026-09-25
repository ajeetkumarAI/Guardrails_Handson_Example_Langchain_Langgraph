from guardrails_demo.langchain_guardrails.topic_guard import keyword_topic_guard


def test_on_topic_keyword_allowed():
    result = keyword_topic_guard("What is a Python list?")
    assert result.allowed


def test_off_topic_keyword_blocked():
    result = keyword_topic_guard("Tell me today's cricket score.")
    assert not result.allowed
    assert result.category == "off_topic"


def test_inconclusive_case_is_flagged():
    result = keyword_topic_guard("Can you help me with something?")
    assert result.category == "inconclusive"
    assert result.confidence < 1.0
