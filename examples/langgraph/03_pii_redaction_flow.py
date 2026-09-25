"""
Example 03 - PII Redaction Workflow (LangGraph layer)

Flow:
    START -> detect_pii -> redact -> agent -> output_validation -> END
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_pii_redaction_graph

if __name__ == "__main__":
    graph = build_pii_redaction_graph()
    text = "What is a Python dict? Reach me at jane@example.com."
    print("Input:", text)
    result = graph.invoke(new_state(text))
    print("Working text after redaction:", result["working_text"])
    print("Final state guardrail_status:", result["guardrail_status"])
    print("Output:", result["output"])
