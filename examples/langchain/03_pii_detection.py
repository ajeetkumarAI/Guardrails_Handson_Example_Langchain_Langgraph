"""
Example 03 - PII Detection (LangChain layer)

Objective:
    Detect emails, phone numbers, credit-card-like numbers, and IP addresses.
Concept:
    Regex-based pattern matching. This is educational, not a complete
    enterprise DLP (data loss prevention) solution - real systems combine
    context, locale-aware formats, and often a trained model.
Example allowed input:
    "How do I format a date in Python?"
Example rejected input:
    "Contact John at john@example.com or 555-123-4567"
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.pii_guard import detect_pii

if __name__ == "__main__":
    safe_text = "How do I format a date in Python?"
    print("Input:", safe_text)
    result = detect_pii(safe_text)
    print_guardrail_report("pii_detection", result.allowed, result.reason)

    risky_text = "Contact John at john@example.com or 555-123-4567, server is 192.168.1.10"
    print("\nInput:", risky_text)
    result = detect_pii(risky_text)
    print_guardrail_report("pii_detection", result.allowed, result.reason)
    print("Matches:", result.metadata.get("matches"))
