"""The shared graph state used across the LangGraph examples.

Keeping guardrail bookkeeping (attempt counts, risk level, escalation
flags) directly on the graph state is what lets routing decisions be
made purely from state, which is the pattern docs/03_langgraph_guardrails.md
explains in more detail.
"""
from __future__ import annotations

from typing import Any, Optional, TypedDict


class GraphState(TypedDict, total=False):
    user_input: str
    working_text: str
    output: str

    guardrail_status: str  # "pending" | "allowed" | "blocked" | "needs_review"
    rejection_reason: Optional[str]
    risk_level: str  # "low" | "medium" | "high"

    attempt_count: int
    model_call_count: int
    tool_call_count: int
    requested_tool_calls: list[str]

    approval_required: bool
    approved: bool
    escalation_required: bool

    tool_name: Optional[str]
    tool_arguments: dict[str, Any]
    tool_result: Optional[str]

    metadata: dict[str, Any]


def new_state(user_input: str) -> GraphState:
    """Build a fresh state dict with sensible defaults for a new run."""
    return GraphState(
        user_input=user_input,
        working_text=user_input,
        output="",
        guardrail_status="pending",
        rejection_reason=None,
        risk_level="low",
        attempt_count=0,
        model_call_count=0,
        tool_call_count=0,
        requested_tool_calls=[],
        approval_required=False,
        approved=False,
        escalation_required=False,
        tool_name=None,
        tool_arguments={},
        tool_result=None,
        metadata={},
    )
