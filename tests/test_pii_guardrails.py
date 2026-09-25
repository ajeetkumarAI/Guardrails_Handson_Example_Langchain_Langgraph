from guardrails_demo.langchain_guardrails.pii_guard import detect_pii, redact_pii


def test_no_pii_detected_in_clean_text():
    result = detect_pii("How do I write a for loop in Python?")
    assert result.allowed


def test_email_is_detected():
    result = detect_pii("Contact me at jane@example.com")
    assert not result.allowed
    assert "email" in result.metadata["matches"]


def test_phone_is_detected():
    result = detect_pii("Call 555-123-4567 for support")
    assert not result.allowed
    assert "phone" in result.metadata["matches"]


def test_redaction_removes_email():
    redacted = redact_pii("Contact John at john@example.com")
    assert "john@example.com" not in redacted
    assert "[EMAIL_REDACTED]" in redacted


def test_redaction_removes_phone():
    redacted = redact_pii("Call me at 555-123-4567")
    assert "555-123-4567" not in redacted
    assert "[PHONE_REDACTED]" in redacted
