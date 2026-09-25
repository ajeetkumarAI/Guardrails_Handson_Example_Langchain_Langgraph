"""
Example 10 - Agent Loop Protection (LangGraph layer)

Demonstrates a hard ceiling on tool-calling iterations (MAX_TOOL_CALLS),
so an agent that keeps requesting tools cannot loop forever.
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_agent_loop_protection_graph

if __name__ == "__main__":
    graph = build_agent_loop_protection_graph()

    state = new_state("keep calculating")
    # Simulate an agent that wants to call the tool many more times than allowed.
    state["requested_tool_calls"] = ["calculator"] * 10
    state["tool_name"] = "calculator"
    state["tool_arguments"] = {"operation": "add", "left": 1, "right": 1}

    result = graph.invoke(state)
    print("Tool calls actually executed:", result["tool_call_count"])
    print("Escalation required:", result["escalation_required"])
    print("Output:", result["output"])
