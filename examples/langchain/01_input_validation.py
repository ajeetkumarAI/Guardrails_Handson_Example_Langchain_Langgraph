"""
Example 01 - Input Validation (LangChain layer)

Objective:
    Reject bad input before it ever reaches a model call.
Concept:
    Deterministic, zero-cost checks (empty, too short, too long, wrong type)
    should always run first - they catch the majority of malformed requests
    without spending a single token.
Example allowed input:
    "What is a Python list?"
Example rejected input:
    ""  (empty)
Expected behavior:
    Allowed input passes through untouched. Rejected input never reaches
    the model and gets a clear reason back instead.
Security consideration:
    Input validation is not a security boundary on its own, but it removes
    an entire class of noisy/garbage requests before more expensive checks run.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.input_validation import validate_input


def run(sample: object) -> None:
    result = validate_input(sample)
    print_guardrail_report("input_validation", result.allowed, result.reason)


if __name__ == "__main__":
    print("Input:", repr("What is a Python list?"))
    run("What is a Python list?")

    print("\nInput:", repr(""))
    run("")

    print("\nInput:", repr("x" * 3000))
    run("x" * 3000)

    print("\nInput:", repr(12345))
    run(12345)
