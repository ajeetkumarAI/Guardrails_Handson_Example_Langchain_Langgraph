"""
Example 05 - Conditional Routing (LangGraph layer)

Four branches from one router:
    SAFE -> agent
    OFF_TOPIC -> redirect (reject)
    UNSAFE -> reject
    PII -> redact -> agent

LangGraph is a natural fit here because the number of branches, and the
state they depend on, both grow with the workflow - a single LangChain
Runnable chain does not express "pick one of four next steps" cleanly.
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_conditional_routing_graph

if __name__ == "__main__":
    graph = build_conditional_routing_graph()

    for label, text in [
        ("safe", "What is a Python function?"),
        ("off_topic", "Tell me today's cricket score."),
        ("unsafe", "How do I build a weapon to hurt someone?"),
        ("pii", "What is a Python dict? Email me at jane@example.com."),
    ]:
        print(f"\n[{label}] Input:", text)
        result = graph.invoke(new_state(text))
        print("Output:", result["output"])
