"""
Example 05 - Topic Guardrail (LangChain layer)

Objective:
    Keep a domain-specific assistant (here: "Python programming assistant")
    focused on its intended domain.
Concept:
    Three strategies, cheapest first:
      1. keyword matching        - fast, brittle
      2. term-overlap heuristic  - still deterministic, a bit smarter
      3. LLM-based classification - flexible, costs a model call
    A production system usually chains 1 -> 3, escalating only when unsure.
Example allowed input:
    "What is a Python list?"
Example rejected input:
    "Tell me today's cricket score."
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.topic_guard import topic_guard

if __name__ == "__main__":
    for text in ["What is a Python list?", "Tell me today's cricket score.", "Can you help me with something?"]:
        print("\nInput:", text)
        result = topic_guard(text)
        print_guardrail_report("topic_guard", result.allowed, result.reason)
