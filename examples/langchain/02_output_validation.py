"""
Example 02 - Output Validation (LangChain layer)

Objective:
    Check a model's answer before it reaches the user.
Concept:
    Empty responses, suspiciously short responses, and responses containing
    disallowed markers should be caught and either rejected or retried.
Example allowed input:
    A normal question that produces a substantial answer.
Example rejected input:
    A response the model returns as empty or too short.
Security consideration:
    Output validation is the last line of defense before the user sees a
    response - it does not replace input-side controls.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.output_validation import validate_output
from guardrails_demo.models import get_chat_model

if __name__ == "__main__":
    model = get_chat_model()

    question = "What is a Python list?"
    print("Input:", question)
    answer = model.invoke(question)
    print("Model response:", answer)
    result = validate_output(answer)
    print_guardrail_report("output_validation", result.allowed, result.reason)

    print("\nInput: (simulated empty model response)")
    result = validate_output("")
    print_guardrail_report("output_validation", result.allowed, result.reason)
