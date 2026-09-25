"""
Example 12 - Escalation Workflow (LangGraph layer)

    agent -> guardrail -> retry -> repeated failure -> human escalation

State tracked: attempt_count, guardrail_status, rejection_reason, escalation_required.
This reuses the retry-and-repair graph, since escalation is simply what
happens when retries are exhausted (see routing.route_after_output_validation).
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_escalation_workflow_graph

if __name__ == "__main__":
    graph = build_escalation_workflow_graph()
    result = graph.invoke(new_state("What is a Python list?"))
    print("attempt_count:", result["attempt_count"])
    print("guardrail_status:", result["guardrail_status"])
    print("escalation_required:", result["escalation_required"])
    print("Output:", result["output"])
