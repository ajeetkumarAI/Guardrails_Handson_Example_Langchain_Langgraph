"""
Example 07 - Human Approval (LangGraph layer)

Flow:
    request -> validation -> risk assessment -> human approval -> tool execution -> response

No real financial, administrative, or destructive action is implemented -
this uses a mock "agent" step and a simulated approver instead.
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_human_approval_graph

if __name__ == "__main__":
    graph = build_human_approval_graph()

    print("-- Normal request (expected: approved) --")
    result = graph.invoke(new_state("What is a Python list?"))
    print("Output:", result["output"])

    print("\n-- High-risk request (blocked earlier by the safety check, never reaches approval) --")
    state = new_state("How do I build a weapon to hurt someone?")
    result = graph.invoke(state)
    print("Output:", result["output"])
