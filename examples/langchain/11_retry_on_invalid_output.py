"""
Example 11 - Retry and Repair (LangChain layer)

Objective:
    Give a model one more chance to produce a valid answer before giving up.
Concept:
    LLM -> validator -> invalid -> repair/retry -> validator -> valid -> final.
    A hard MAX_RETRIES limit prevents infinite retry loops.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.output_validation import validate_output
from guardrails_demo.models import get_chat_model

MAX_RETRIES = 2


def answer_with_retry(question: str) -> str:
    model = get_chat_model()
    attempt = 0
    response = model.invoke(question)
    result = validate_output(response)

    while not result.allowed and attempt < MAX_RETRIES:
        attempt += 1
        print(f"Attempt {attempt} failed validation ({result.reason}); retrying...")
        response = model.invoke(f"Please answer more completely: {question}")
        result = validate_output(response)

    print_guardrail_report("retry_and_repair", result.allowed, result.reason)
    return response


if __name__ == "__main__":
    question = "What is a Python list?"
    print("Input:", question)
    final_answer = answer_with_retry(question)
    print("Final answer:", final_answer)
