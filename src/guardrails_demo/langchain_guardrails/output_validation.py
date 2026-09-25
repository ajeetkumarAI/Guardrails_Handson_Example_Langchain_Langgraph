"""Checks applied to a model's response before it reaches the user."""
from __future__ import annotations

from guardrails_demo.common.result import GuardrailResult
from guardrails_demo.common.utils import contains_any

PROHIBITED_TERMS = ["confidential_internal_marker", "system_secret_key"]


def check_output_not_empty(text: str) -> GuardrailResult:
    if not text or not text.strip():
        return GuardrailResult.block("output_empty", "Model returned an empty response.")
    return GuardrailResult.allow("output_empty")


def check_output_min_quality(text: str, min_length: int = 5) -> GuardrailResult:
    if len(text.strip()) < min_length:
        return GuardrailResult.block(
            "output_too_short", "Model response is too short to be useful."
        )
    return GuardrailResult.allow("output_too_short")


def check_prohibited_content(text: str) -> GuardrailResult:
    hit = contains_any(text, PROHIBITED_TERMS)
    if hit:
        return GuardrailResult.block(
            "output_prohibited_content", f"Response contains a disallowed marker: {hit}"
        )
    return GuardrailResult.allow("output_prohibited_content")


def validate_output(text: str) -> GuardrailResult:
    for check in (check_output_not_empty, check_output_min_quality, check_prohibited_content):
        result = check(text)
        if not result.allowed:
            return result
    return GuardrailResult.allow("output_validation")
