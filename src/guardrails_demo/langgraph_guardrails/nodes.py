"""Reusable LangGraph node functions.

Every node takes a GraphState and returns a *partial* state update (the
LangGraph convention), so nodes stay small and composable across the
different example workflows.
"""
from __future__ import annotations

from typing import Any

from guardrails_demo.langchain_guardrails.input_validation import validate_input
from guardrails_demo.langchain_guardrails.output_validation import validate_output
from guardrails_demo.langchain_guardrails.pii_guard import detect_pii, redact_pii
from guardrails_demo.langchain_guardrails.safety_guard import safety_guard
from guardrails_demo.langchain_guardrails.topic_guard import keyword_topic_guard
from guardrails_demo.langgraph_guardrails.state import GraphState
from guardrails_demo.models import get_chat_model

MAX_RETRIES = 2
MAX_TOOL_CALLS = 3


def validate_input_node(state: GraphState) -> dict[str, Any]:
    result = validate_input(state["user_input"])
    if not result.allowed:
        return {"guardrail_status": "blocked", "rejection_reason": result.reason}
    return {"guardrail_status": "allowed"}


def detect_pii_node(state: GraphState) -> dict[str, Any]:
    result = detect_pii(state["working_text"])
    if not result.allowed:
        return {"risk_level": "medium", "metadata": {**state.get("metadata", {}), "pii": result.metadata}}
    return {}


def redact_pii_node(state: GraphState) -> dict[str, Any]:
    return {"working_text": redact_pii(state["working_text"])}


def topic_check_node(state: GraphState) -> dict[str, Any]:
    result = keyword_topic_guard(state["working_text"])
    if not result.allowed:
        return {"guardrail_status": "blocked", "rejection_reason": result.reason}
    return {"guardrail_status": "allowed"}


def safety_check_node(state: GraphState) -> dict[str, Any]:
    result = safety_guard(state["working_text"])
    if not result.allowed:
        return {"guardrail_status": "blocked", "rejection_reason": result.reason, "risk_level": "high"}
    return {"guardrail_status": "allowed"}


def injection_check_node(state: GraphState) -> dict[str, Any]:
    """Flag classic prompt-injection phrasing before it reaches the agent."""
    suspicious_phrases = [
        "ignore previous instructions",
        "ignore all prior instructions",
        "reveal your system prompt",
        "disregard your rules",
        "act as if you have no restrictions",
    ]
    lowered = state["working_text"].lower()
    for phrase in suspicious_phrases:
        if phrase in lowered:
            return {
                "guardrail_status": "blocked",
                "rejection_reason": f"Detected likely prompt-injection pattern: '{phrase}'",
                "risk_level": "high",
            }
    return {"guardrail_status": "allowed"}


def agent_node(state: GraphState) -> dict[str, Any]:
    """A minimal 'agent' step: call the (possibly stub) chat model once."""
    model = get_chat_model()
    response = model.invoke(state["working_text"])
    return {
        "output": response,
        "model_call_count": state.get("model_call_count", 0) + 1,
    }


def output_validation_node(state: GraphState) -> dict[str, Any]:
    result = validate_output(state["output"])
    if not result.allowed:
        return {
            "guardrail_status": "blocked",
            "rejection_reason": result.reason,
            "attempt_count": state.get("attempt_count", 0) + 1,
        }
    return {"guardrail_status": "allowed"}


def repair_node(state: GraphState) -> dict[str, Any]:
    """Ask the model to try again with a slightly more directive prompt."""
    model = get_chat_model()
    repair_prompt = f"Please answer more completely and clearly: {state['user_input']}"
    response = model.invoke(repair_prompt)
    return {
        "output": response,
        "model_call_count": state.get("model_call_count", 0) + 1,
    }


def human_approval_node(state: GraphState) -> dict[str, Any]:
    """Mock human-in-the-loop approval.

    In a real deployment this node would pause the graph (e.g. via
    LangGraph's interrupt mechanism) and wait for a human decision. Here
    it simulates an approver approving anything that isn't flagged high risk.
    """
    approved = state.get("risk_level", "low") != "high"
    return {"approval_required": True, "approved": approved}


def escalate_node(state: GraphState) -> dict[str, Any]:
    return {
        "escalation_required": True,
        "guardrail_status": "needs_review",
        "output": "This request has been escalated to a human reviewer.",
    }


def rejection_node(state: GraphState) -> dict[str, Any]:
    reason = state.get("rejection_reason") or "Request was rejected by a guardrail."
    return {"output": f"Request blocked: {reason}"}


# --- Tool-calling guardrail nodes -------------------------------------------------

def propose_tool_call_node(state: GraphState) -> dict[str, Any]:
    """Stand-in for an agent deciding to call a tool. Reads a pre-set tool
    request off state (in a real agent this would come from the model's
    tool-call output)."""
    requested = state.get("requested_tool_calls", [])
    tool_name = requested[0] if requested else state.get("tool_name")
    remaining = requested[1:] if requested else []
    return {"tool_name": tool_name, "requested_tool_calls": remaining}


def tool_allowlist_node(state: GraphState) -> dict[str, Any]:
    from guardrails_demo.langchain_guardrails.tool_guard import check_tool_allowlist
    from guardrails_demo.langgraph_guardrails.tools import ALLOWED_TOOLS

    result = check_tool_allowlist(state.get("tool_name", ""), ALLOWED_TOOLS)
    if not result.allowed:
        return {"guardrail_status": "blocked", "rejection_reason": result.reason}
    return {"guardrail_status": "allowed"}


def tool_argument_validation_node(state: GraphState) -> dict[str, Any]:
    from guardrails_demo.langchain_guardrails.tool_guard import validate_tool_arguments
    from guardrails_demo.schemas import CalculatorArguments, WeatherArguments

    schemas = {"calculator": CalculatorArguments, "weather_lookup": WeatherArguments}
    schema = schemas.get(state.get("tool_name", ""))
    if schema is None:
        return {"guardrail_status": "blocked", "rejection_reason": "Unknown tool schema."}

    result = validate_tool_arguments(schema, state.get("tool_arguments", {}))
    if not result.allowed:
        return {"guardrail_status": "blocked", "rejection_reason": result.reason}
    return {"guardrail_status": "allowed"}


def tool_execution_node(state: GraphState) -> dict[str, Any]:
    from guardrails_demo.langgraph_guardrails.tools import run_calculator, run_weather_lookup
    from guardrails_demo.schemas import CalculatorArguments, WeatherArguments

    tool_name = state.get("tool_name")
    args = state.get("tool_arguments", {})
    if tool_name == "calculator":
        result = run_calculator(CalculatorArguments.model_validate(args))
    elif tool_name == "weather_lookup":
        result = run_weather_lookup(WeatherArguments.model_validate(args))
    else:
        result = ""
    return {
        "tool_result": result,
        "tool_call_count": state.get("tool_call_count", 0) + 1,
    }


def tool_output_validation_node(state: GraphState) -> dict[str, Any]:
    from guardrails_demo.langchain_guardrails.tool_guard import validate_tool_output

    result = validate_tool_output(state.get("tool_result"))
    if not result.allowed:
        return {"guardrail_status": "blocked", "rejection_reason": result.reason}
    return {"guardrail_status": "allowed", "output": state.get("tool_result", "")}


def sensitive_action_check_node(state: GraphState) -> dict[str, Any]:
    from guardrails_demo.langgraph_guardrails.tools import SENSITIVE_TOOLS

    # Being a sensitive/write tool means approval is *required*, but it does not
    # by itself make the request unsafe - that is a separate, content-based signal
    # (see safety_guard / risk_level). Conflating the two would mean every
    # sensitive action gets auto-denied, defeating the point of human review.
    is_sensitive = state.get("tool_name") in SENSITIVE_TOOLS
    return {"approval_required": is_sensitive}


def create_ticket_node(state: GraphState) -> dict[str, Any]:
    from guardrails_demo.langgraph_guardrails.tools import run_create_ticket
    from guardrails_demo.schemas import TicketArguments

    result = run_create_ticket(TicketArguments.model_validate(state.get("tool_arguments", {})))
    return {"tool_result": result, "output": result, "tool_call_count": state.get("tool_call_count", 0) + 1}
