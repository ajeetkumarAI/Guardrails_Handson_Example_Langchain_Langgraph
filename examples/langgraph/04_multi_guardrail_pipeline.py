"""
Example 04 - Multi-Guardrail Pipeline (LangGraph layer)

Flow:
    input validation -> PII check -> topic check -> safety check -> agent -> output check
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_multi_guardrail_pipeline_graph

if __name__ == "__main__":
    graph = build_multi_guardrail_pipeline_graph()

    for text in [
        "What is a Python function?",
        "Tell me today's cricket score.",
        "",
    ]:
        print("\nInput:", repr(text))
        result = graph.invoke(new_state(text))
        print("Guardrail status:", result["guardrail_status"])
        print("Output:", result["output"])
