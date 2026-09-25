"""
Example 06 - Retry and Repair Graph (LangGraph layer)

Flow:
    agent -> validator -> valid -> END
                        -> invalid -> repair -> validator (looped, capped at MAX_RETRIES)
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_retry_and_repair_graph

if __name__ == "__main__":
    graph = build_retry_and_repair_graph()
    text = "What is a Python list?"
    print("Input:", text)
    result = graph.invoke(new_state(text))
    print("Guardrail status:", result["guardrail_status"])
    print("Attempt count:", result["attempt_count"])
    print("Output:", result["output"])
