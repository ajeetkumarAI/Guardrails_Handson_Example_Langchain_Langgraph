"""Validate tool arguments before a tool actually executes, and tool output before
it goes back to the model. Deny-by-default: an unknown tool is always rejected.
"""
from __future__ import annotations

from typing import Any, Type

from pydantic import BaseModel, ValidationError

from guardrails_demo.common.result import GuardrailResult


def validate_tool_arguments(schema: Type[BaseModel], arguments: dict[str, Any]) -> GuardrailResult:
    try:
        parsed = schema.model_validate(arguments)
    except ValidationError as exc:
        return GuardrailResult.block(
            "tool_arguments_invalid",
            "; ".join(f"{e['loc']}: {e['msg']}" for e in exc.errors()),
        )
    return GuardrailResult(
        allowed=True, category="tool_arguments_valid", metadata={"parsed": parsed.model_dump()}
    )


def check_tool_allowlist(tool_name: str, allowed_tools: list[str]) -> GuardrailResult:
    if tool_name not in allowed_tools:
        return GuardrailResult.block(
            "tool_not_allowed", f"Tool '{tool_name}' is not in the allowlist {allowed_tools}."
        )
    return GuardrailResult.allow("tool_allowed")


def validate_tool_output(output: Any, expected_type: type = str) -> GuardrailResult:
    if not isinstance(output, expected_type):
        return GuardrailResult.block(
            "tool_output_invalid",
            f"Tool output type {type(output).__name__} did not match expected {expected_type.__name__}.",
        )
    if isinstance(output, str) and not output.strip():
        return GuardrailResult.block("tool_output_invalid", "Tool returned an empty result.")
    return GuardrailResult.allow("tool_output_valid")
