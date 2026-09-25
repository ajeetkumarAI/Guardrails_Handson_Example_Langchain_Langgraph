"""
Example 11 - Sensitive Action Approval (LangGraph layer)

    normal read operation   -> automatic
    sensitive write action  -> approval required

Uses a mock "create_ticket" tool. No real ticket is created and no real
email is sent anywhere in this repository.
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_sensitive_action_approval_graph

if __name__ == "__main__":
    graph = build_sensitive_action_approval_graph()

    print("-- Sensitive write action (requires approval) --")
    state = new_state("open a ticket")
    state["tool_name"] = "create_ticket"
    state["tool_arguments"] = {"title": "Server is down", "priority": "high"}
    result = graph.invoke(state)
    print("Approval required:", result["approval_required"])
    print("Approved:", result["approved"])
    print("Output:", result["output"])
