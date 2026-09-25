"""
Example 12 - Combined LangChain Guardrails

Objective:
    Chain input validation -> topic validation -> PII handling -> model call
    -> structured output -> output validation into one small pipeline.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.input_validation import validate_input
from guardrails_demo.langchain_guardrails.output_validation import validate_output
from guardrails_demo.langchain_guardrails.pii_guard import detect_pii, redact_pii
from guardrails_demo.langchain_guardrails.topic_guard import topic_guard
from guardrails_demo.models import get_chat_model


def handle_request(text: str) -> str:
    checks = [
        ("input_validation", validate_input(text)),
    ]
    for name, result in checks:
        if not result.allowed:
            print_guardrail_report(name, False, result.reason)
            return f"Blocked at {name}: {result.reason}"

    pii_result = detect_pii(text)
    working_text = redact_pii(text) if not pii_result.allowed else text
    print_guardrail_report("pii_check", pii_result.allowed, pii_result.reason)

    topic_result = topic_guard(working_text, escalate_when_unsure=False)
    if not topic_result.allowed:
        print_guardrail_report("topic_guard", False, topic_result.reason)
        return f"Blocked at topic_guard: {topic_result.reason}"

    model = get_chat_model()
    response = model.invoke(working_text)

    output_result = validate_output(response)
    print_guardrail_report("output_validation", output_result.allowed, output_result.reason)
    if not output_result.allowed:
        return f"Blocked at output_validation: {output_result.reason}"

    return response


if __name__ == "__main__":
    for sample in [
        "What is a Python dict? My email is jane@example.com if you need to follow up.",
        "Tell me today's cricket score.",
        "",
    ]:
        print("\n==============================")
        print("Input:", sample)
        print("Result:", handle_request(sample))
