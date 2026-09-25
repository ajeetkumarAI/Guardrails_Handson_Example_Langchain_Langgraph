"""Conditional-edge functions: pure functions of state that return a branch name.

Centralising these here (rather than inlining lambdas in every workflow)
keeps the branching logic testable on its own, without building a graph.
"""
from __future__ import annotations

from guardrails_demo.langgraph_guardrails.nodes import MAX_RETRIES, MAX_TOOL_CALLS
from guardrails_demo.langgraph_guardrails.state import GraphState


def route_after_guardrail(state: GraphState) -> str:
    """Generic router used after any single pass/fail guardrail node."""
    return "allowed" if state.get("guardrail_status") == "allowed" else "blocked"


def route_after_output_validation(state: GraphState) -> str:
    if state.get("guardrail_status") == "allowed":
        return "done"
    if state.get("attempt_count", 0) >= MAX_RETRIES:
        return "escalate"
    return "retry"


def route_by_risk(state: GraphState) -> str:
    risk = state.get("risk_level", "low")
    if risk == "high":
        return "unsafe"
    if state.get("guardrail_status") == "blocked":
        return "off_topic_or_blocked"
    if state.get("metadata", {}).get("pii"):
        return "pii"
    return "safe"


def route_after_approval(state: GraphState) -> str:
    return "proceed" if state.get("approved") else "escalate"


def route_tool_loop(state: GraphState) -> str:
    """Used inside an agent/tool loop to enforce a hard iteration ceiling."""
    if state.get("tool_call_count", 0) >= MAX_TOOL_CALLS:
        return "stop_max_calls"
    if state.get("guardrail_status") == "blocked":
        return "stop_blocked"
    return "continue"
