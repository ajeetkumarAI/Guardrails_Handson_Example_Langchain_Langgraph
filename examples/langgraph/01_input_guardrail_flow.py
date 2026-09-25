"""
Example 01 - Basic Input Guardrail (LangGraph layer)

Flow:
    START -> validate_input -> agent -> END
    Invalid input -> reject -> END
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_basic_input_guardrail_graph

if __name__ == "__main__":
    graph = build_basic_input_guardrail_graph()

    for text in ["What is a Python list?", ""]:
        print("\nInput:", repr(text))
        result = graph.invoke(new_state(text))
        print("Guardrail status:", result["guardrail_status"])
        print("Output:", result["output"])
