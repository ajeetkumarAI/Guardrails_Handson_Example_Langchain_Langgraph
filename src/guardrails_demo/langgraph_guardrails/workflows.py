"""StateGraph builders for the LangGraph examples.

Each function here builds and compiles one graph. The example scripts in
examples/langgraph/ import these builders so the actual graph-construction
code lives in one place and can be unit tested directly.
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from guardrails_demo.langgraph_guardrails import nodes, routing
from guardrails_demo.langgraph_guardrails.state import GraphState


def build_basic_input_guardrail_graph():
    """START -> validate_input -> agent -> END, with a rejection branch."""
    graph = StateGraph(GraphState)
    graph.add_node("validate_input", nodes.validate_input_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "validate_input")
    graph.add_conditional_edges(
        "validate_input", routing.route_after_guardrail, {"allowed": "agent", "blocked": "reject"}
    )
    graph.add_edge("agent", END)
    graph.add_edge("reject", END)
    return graph.compile()


def build_output_guardrail_graph():
    """START -> agent -> validate_output -> (END | retry -> agent, capped)."""
    graph = StateGraph(GraphState)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("validate_output", nodes.output_validation_node)
    graph.add_node("escalate", nodes.escalate_node)

    graph.add_edge(START, "agent")
    graph.add_edge("agent", "validate_output")
    graph.add_conditional_edges(
        "validate_output",
        routing.route_after_output_validation,
        {"done": END, "retry": "agent", "escalate": "escalate"},
    )
    graph.add_edge("escalate", END)
    return graph.compile()


def build_pii_redaction_graph():
    """START -> detect_pii -> redact -> agent -> validate_output -> END."""
    graph = StateGraph(GraphState)
    graph.add_node("detect_pii", nodes.detect_pii_node)
    graph.add_node("redact", nodes.redact_pii_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("validate_output", nodes.output_validation_node)

    graph.add_edge(START, "detect_pii")
    graph.add_edge("detect_pii", "redact")
    graph.add_edge("redact", "agent")
    graph.add_edge("agent", "validate_output")
    graph.add_edge("validate_output", END)
    return graph.compile()


def build_multi_guardrail_pipeline_graph():
    """input -> pii -> topic -> safety -> agent -> output, each gated."""
    graph = StateGraph(GraphState)
    graph.add_node("validate_input", nodes.validate_input_node)
    graph.add_node("detect_pii", nodes.detect_pii_node)
    graph.add_node("topic_check", nodes.topic_check_node)
    graph.add_node("safety_check", nodes.safety_check_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("validate_output", nodes.output_validation_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "validate_input")
    graph.add_conditional_edges(
        "validate_input", routing.route_after_guardrail, {"allowed": "detect_pii", "blocked": "reject"}
    )
    graph.add_edge("detect_pii", "topic_check")
    graph.add_conditional_edges(
        "topic_check", routing.route_after_guardrail, {"allowed": "safety_check", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "safety_check", routing.route_after_guardrail, {"allowed": "agent", "blocked": "reject"}
    )
    graph.add_edge("agent", "validate_output")
    graph.add_edge("validate_output", END)
    graph.add_edge("reject", END)
    return graph.compile()


def build_conditional_routing_graph():
    """Four-way branch: safe / off_topic / unsafe / pii."""
    graph = StateGraph(GraphState)
    graph.add_node("safety_check", nodes.safety_check_node)
    graph.add_node("topic_check", nodes.topic_check_node)
    graph.add_node("detect_pii", nodes.detect_pii_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("redact", nodes.redact_pii_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "safety_check")
    graph.add_edge("safety_check", "detect_pii")
    graph.add_edge("detect_pii", "topic_check")
    graph.add_conditional_edges(
        "topic_check",
        routing.route_by_risk,
        {
            "unsafe": "reject",
            "off_topic_or_blocked": "reject",
            "pii": "redact",
            "safe": "agent",
        },
    )
    graph.add_edge("redact", "agent")
    graph.add_edge("agent", END)
    graph.add_edge("reject", END)
    return graph.compile()


def build_retry_and_repair_graph():
    """agent -> validator -> valid (END) | invalid -> repair -> validator (capped)."""
    graph = StateGraph(GraphState)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("validate_output", nodes.output_validation_node)
    graph.add_node("repair", nodes.repair_node)
    graph.add_node("escalate", nodes.escalate_node)

    graph.add_edge(START, "agent")
    graph.add_edge("agent", "validate_output")
    graph.add_conditional_edges(
        "validate_output",
        routing.route_after_output_validation,
        {"done": END, "retry": "repair", "escalate": "escalate"},
    )
    graph.add_edge("repair", "validate_output")
    graph.add_edge("escalate", END)
    return graph.compile()


def build_human_approval_graph():
    """request -> validation -> risk assessment -> human approval -> tool -> response."""
    graph = StateGraph(GraphState)
    graph.add_node("validate_input", nodes.validate_input_node)
    graph.add_node("safety_check", nodes.safety_check_node)
    graph.add_node("human_approval", nodes.human_approval_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("escalate", nodes.escalate_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "validate_input")
    graph.add_conditional_edges(
        "validate_input", routing.route_after_guardrail, {"allowed": "safety_check", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "safety_check", routing.route_after_guardrail, {"allowed": "human_approval", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "human_approval", routing.route_after_approval, {"proceed": "agent", "escalate": "escalate"}
    )
    graph.add_edge("agent", END)
    graph.add_edge("escalate", END)
    graph.add_edge("reject", END)
    return graph.compile()


def build_prompt_injection_protection_graph():
    """user input -> injection detector -> safe: agent | suspicious: reject."""
    graph = StateGraph(GraphState)
    graph.add_node("injection_check", nodes.injection_check_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "injection_check")
    graph.add_conditional_edges(
        "injection_check", routing.route_after_guardrail, {"allowed": "agent", "blocked": "reject"}
    )
    graph.add_edge("agent", END)
    graph.add_edge("reject", END)
    return graph.compile()


def build_escalation_workflow_graph():
    """agent -> guardrail -> retry -> repeated failure -> human escalation."""
    return build_retry_and_repair_graph()


def build_tool_execution_guardrail_graph():
    """agent proposes a tool -> allowlist -> argument validation -> execute -> output validation."""
    graph = StateGraph(GraphState)
    graph.add_node("propose_tool", nodes.propose_tool_call_node)
    graph.add_node("allowlist_check", nodes.tool_allowlist_node)
    graph.add_node("argument_check", nodes.tool_argument_validation_node)
    graph.add_node("execute_tool", nodes.tool_execution_node)
    graph.add_node("validate_tool_output", nodes.tool_output_validation_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "propose_tool")
    graph.add_edge("propose_tool", "allowlist_check")
    graph.add_conditional_edges(
        "allowlist_check", routing.route_after_guardrail, {"allowed": "argument_check", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "argument_check", routing.route_after_guardrail, {"allowed": "execute_tool", "blocked": "reject"}
    )
    graph.add_edge("execute_tool", "validate_tool_output")
    graph.add_conditional_edges(
        "validate_tool_output", routing.route_after_guardrail, {"allowed": END, "blocked": "reject"}
    )
    graph.add_edge("reject", END)
    return graph.compile()


def build_agent_loop_protection_graph():
    """A tool-calling loop with a hard ceiling on iterations, to prevent runaway agents."""
    graph = StateGraph(GraphState)
    graph.add_node("propose_tool", nodes.propose_tool_call_node)
    graph.add_node("allowlist_check", nodes.tool_allowlist_node)
    graph.add_node("execute_tool", nodes.tool_execution_node)
    graph.add_node("stop", nodes.escalate_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "propose_tool")
    graph.add_edge("propose_tool", "allowlist_check")
    graph.add_conditional_edges(
        "allowlist_check", routing.route_after_guardrail, {"allowed": "execute_tool", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "execute_tool",
        routing.route_tool_loop,
        {"continue": "propose_tool", "stop_max_calls": "stop", "stop_blocked": "reject"},
    )
    graph.add_edge("stop", END)
    graph.add_edge("reject", END)
    return graph.compile()


def build_sensitive_action_approval_graph():
    """Read operations proceed automatically; sensitive write operations need approval."""
    graph = StateGraph(GraphState)
    graph.add_node("propose_tool", nodes.propose_tool_call_node)
    graph.add_node("sensitivity_check", nodes.sensitive_action_check_node)
    graph.add_node("human_approval", nodes.human_approval_node)
    graph.add_node("create_ticket", nodes.create_ticket_node)
    graph.add_node("escalate", nodes.escalate_node)

    graph.add_edge(START, "propose_tool")
    graph.add_edge("propose_tool", "sensitivity_check")

    def route_sensitivity(state):
        return "sensitive" if state.get("approval_required") else "automatic"

    graph.add_conditional_edges(
        "sensitivity_check", route_sensitivity, {"sensitive": "human_approval", "automatic": "create_ticket"}
    )
    graph.add_conditional_edges(
        "human_approval", routing.route_after_approval, {"proceed": "create_ticket", "escalate": "escalate"}
    )
    graph.add_edge("create_ticket", END)
    graph.add_edge("escalate", END)
    return graph.compile()


def build_state_based_guardrail_graph():
    """Routing decisions driven entirely by counters/flags already on state."""
    graph = StateGraph(GraphState)
    graph.add_node("safety_check", nodes.safety_check_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("validate_output", nodes.output_validation_node)
    graph.add_node("repair", nodes.repair_node)
    graph.add_node("escalate", nodes.escalate_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "safety_check")
    graph.add_conditional_edges(
        "safety_check", routing.route_after_guardrail, {"allowed": "agent", "blocked": "reject"}
    )
    graph.add_edge("agent", "validate_output")
    graph.add_conditional_edges(
        "validate_output",
        routing.route_after_output_validation,
        {"done": END, "retry": "repair", "escalate": "escalate"},
    )
    graph.add_edge("repair", "validate_output")
    graph.add_edge("escalate", END)
    graph.add_edge("reject", END)
    return graph.compile()


def build_production_style_agent_graph():
    """The full pipeline from the spec: input -> pii -> injection -> topic -> agent
    -> tool authorization -> tool input validation -> tool execution -> tool output
    validation -> agent -> response validation -> END, with rejection/escalation branches."""
    graph = StateGraph(GraphState)
    graph.add_node("validate_input", nodes.validate_input_node)
    graph.add_node("detect_pii", nodes.detect_pii_node)
    graph.add_node("injection_check", nodes.injection_check_node)
    graph.add_node("topic_check", nodes.topic_check_node)
    graph.add_node("agent", nodes.agent_node)
    graph.add_node("propose_tool", nodes.propose_tool_call_node)
    graph.add_node("tool_allowlist", nodes.tool_allowlist_node)
    graph.add_node("tool_arguments", nodes.tool_argument_validation_node)
    graph.add_node("execute_tool", nodes.tool_execution_node)
    graph.add_node("tool_output_check", nodes.tool_output_validation_node)
    graph.add_node("validate_output", nodes.output_validation_node)
    graph.add_node("escalate", nodes.escalate_node)
    graph.add_node("reject", nodes.rejection_node)

    graph.add_edge(START, "validate_input")
    graph.add_conditional_edges(
        "validate_input", routing.route_after_guardrail, {"allowed": "detect_pii", "blocked": "reject"}
    )
    graph.add_edge("detect_pii", "injection_check")
    graph.add_conditional_edges(
        "injection_check", routing.route_after_guardrail, {"allowed": "topic_check", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "topic_check", routing.route_after_guardrail, {"allowed": "agent", "blocked": "reject"}
    )

    def route_needs_tool(state):
        return "use_tool" if state.get("requested_tool_calls") or state.get("tool_name") else "no_tool"

    graph.add_conditional_edges(
        "agent", route_needs_tool, {"use_tool": "propose_tool", "no_tool": "validate_output"}
    )
    graph.add_edge("propose_tool", "tool_allowlist")
    graph.add_conditional_edges(
        "tool_allowlist", routing.route_after_guardrail, {"allowed": "tool_arguments", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "tool_arguments", routing.route_after_guardrail, {"allowed": "execute_tool", "blocked": "reject"}
    )
    graph.add_edge("execute_tool", "tool_output_check")
    graph.add_conditional_edges(
        "tool_output_check", routing.route_after_guardrail, {"allowed": "validate_output", "blocked": "reject"}
    )
    graph.add_conditional_edges(
        "validate_output",
        routing.route_after_output_validation,
        {"done": END, "retry": "agent", "escalate": "escalate"},
    )
    graph.add_edge("escalate", END)
    graph.add_edge("reject", END)
    return graph.compile()
