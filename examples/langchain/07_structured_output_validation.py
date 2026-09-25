"""
Example 07 - Structured Output Validation (LangChain layer)

Objective:
    Validate that a model's structured response matches a Pydantic schema
    before the application trusts it.
Concept:
    required fields, enum ("Literal") values, numeric ranges, and outright
    malformed responses should all be caught explicitly.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.structured_output_guard import (
    validate_structured_output,
)
from guardrails_demo.schemas import ProductReview

if __name__ == "__main__":
    good = {"sentiment": "positive", "summary": "Great build quality.", "confidence": 0.92}
    print("Input:", good)
    result = validate_structured_output(ProductReview, good)
    print_guardrail_report("structured_output", result.allowed, result.reason)

    bad_enum = {"sentiment": "great", "summary": "Nice.", "confidence": 0.5}
    print("\nInput:", bad_enum)
    result = validate_structured_output(ProductReview, bad_enum)
    print_guardrail_report("structured_output", result.allowed, result.reason)

    bad_confidence = {"sentiment": "negative", "summary": "Broke fast.", "confidence": 5}
    print("\nInput:", bad_confidence)
    result = validate_structured_output(ProductReview, bad_confidence)
    print_guardrail_report("structured_output", result.allowed, result.reason)

    missing_field = {"sentiment": "neutral", "confidence": 0.4}
    print("\nInput:", missing_field)
    result = validate_structured_output(ProductReview, missing_field)
    print_guardrail_report("structured_output", result.allowed, result.reason)
