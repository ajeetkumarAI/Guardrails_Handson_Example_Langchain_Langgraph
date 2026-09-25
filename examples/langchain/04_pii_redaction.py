"""
Example 04 - PII Redaction (LangChain layer)

Objective:
    Transform text so detected PII is replaced with a labelled placeholder
    instead of being dropped or exposed.
Concept:
    Redaction != detection. Detection tells you PII exists; redaction
    changes the text so it's safe to log, store, or forward.
"""
from guardrails_demo.langchain_guardrails.pii_guard import redact_pii

if __name__ == "__main__":
    original = "Contact John at john@example.com or call 555-123-4567."
    print("Original: ", original)
    print("Redacted: ", redact_pii(original))
