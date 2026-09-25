"""
Example 13 - State-Based Guardrails (LangGraph layer)

Graph state tracks: model call count, tool call count, retry count, risk
level, and guardrail status. Every routing decision reads directly from
this state rather than re-deriving it, which is what makes multi-step
workflows auditable: you can print `state` at any point and know exactly
why the graph took the path it did.
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_state_based_guardrail_graph

if __name__ == "__main__":
    graph = build_state_based_guardrail_graph()
    result = graph.invoke(new_state("What is a Python list?"))

    print("Final state snapshot:")
    for key in ["guardrail_status", "risk_level", "attempt_count", "model_call_count"]:
        print(f"  {key}: {result.get(key)}")
    print("Output:", result["output"])
