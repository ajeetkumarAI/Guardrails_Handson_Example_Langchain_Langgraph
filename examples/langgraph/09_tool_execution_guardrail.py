"""
Example 09 - Tool Execution Guardrail (LangGraph layer)

Flow:
    agent -> tool request -> argument validator -> authorization check -> tool -> output validator -> agent

Deny-by-default: any tool not on the allowlist is rejected, regardless of
whether its arguments would otherwise be valid.
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_tool_execution_guardrail_graph

if __name__ == "__main__":
    graph = build_tool_execution_guardrail_graph()

    print("-- Allowed tool, valid arguments --")
    state = new_state("calculate 2 + 3")
    state["tool_name"] = "calculator"
    state["tool_arguments"] = {"operation": "add", "left": 2, "right": 3}
    result = graph.invoke(state)
    print("Output:", result["output"])

    print("\n-- Tool not on the allowlist (deny-by-default) --")
    state = new_state("run shell command")
    state["tool_name"] = "shell_exec"
    state["tool_arguments"] = {}
    result = graph.invoke(state)
    print("Output:", result["output"])
