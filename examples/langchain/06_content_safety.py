"""
Example 06 - Content Safety (LangChain layer)

Objective:
    Demonstrate a generic content-safety guardrail using clearly labelled,
    non-graphic safe/unsafe test cases.
Concept:
    input -> safety check -> allow/reject.
    A real deployment would use a dedicated moderation classifier here
    instead of a keyword list.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.safety_guard import (
    SAFE_TEST_CASES,
    UNSAFE_TEST_CASES,
    safety_guard,
)

if __name__ == "__main__":
    print("-- Safe test cases --")
    for name, text in SAFE_TEST_CASES.items():
        result = safety_guard(text)
        print(f"\n[{name}] Input: {text}")
        print_guardrail_report("safety_guard", result.allowed, result.reason)

    print("\n-- Unsafe test cases (labelled, non-graphic) --")
    for name, text in UNSAFE_TEST_CASES.items():
        result = safety_guard(text)
        print(f"\n[{name}] Input: {text}")
        print_guardrail_report("safety_guard", result.allowed, result.reason)
