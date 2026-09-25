"""Deterministic checks on raw user input, before any model call happens.

These run first because they are the cheapest possible guardrail: no
network call, no tokens spent, just plain Python. See docs/09... no,
see docs/07_best_practices.md for why cheap checks should always run
before expensive ones.
"""
from __future__ import annotations

from guardrails_demo.common.result import GuardrailResult

MIN_LENGTH = 2
MAX_LENGTH = 2000


def check_not_empty(text: str) -> GuardrailResult:
    if text is None or not text.strip():
        return GuardrailResult.block("input_empty", "Input is empty or whitespace only.")
    return GuardrailResult.allow("input_empty")


def check_min_length(text: str, minimum: int = MIN_LENGTH) -> GuardrailResult:
    if len(text.strip()) < minimum:
        return GuardrailResult.block(
            "input_too_short", f"Input must be at least {minimum} characters."
        )
    return GuardrailResult.allow("input_too_short")


def check_max_length(text: str, maximum: int = MAX_LENGTH) -> GuardrailResult:
    if len(text) > maximum:
        return GuardrailResult.block(
            "input_too_long", f"Input exceeds the {maximum} character limit."
        )
    return GuardrailResult.allow("input_too_long")


def check_is_text(value: object) -> GuardrailResult:
    if not isinstance(value, str):
        return GuardrailResult.block(
            "input_wrong_type", f"Expected text input, received {type(value).__name__}."
        )
    return GuardrailResult.allow("input_wrong_type")


def validate_input(
    value: object, min_length: int = MIN_LENGTH, max_length: int = MAX_LENGTH
) -> GuardrailResult:
    """Run every deterministic input check and stop at the first failure."""
    type_check = check_is_text(value)
    if not type_check.allowed:
        return type_check

    text = value  # narrowed to str by check_is_text
    for check in (check_not_empty, lambda t: check_min_length(t, min_length), lambda t: check_max_length(t, max_length)):
        result = check(text)
        if not result.allowed:
            return result
    return GuardrailResult.allow("input_validation")
