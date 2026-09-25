"""Small string/formatting helpers shared by the guardrail modules."""
from __future__ import annotations


def truncate(text: str, max_chars: int = 400) -> str:
    """Shorten text for display/logging without losing the start of it."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


def contains_any(text: str, terms: list[str]) -> str | None:
    """Return the first term from `terms` found in `text` (case-insensitive)."""
    lowered = text.lower()
    for term in terms:
        if term.lower() in lowered:
            return term
    return None


def print_guardrail_report(step: str, allowed: bool, reason: str | None = None) -> None:
    """Print a small, consistent terminal report used by every example script."""
    verdict = "ALLOWED" if allowed else "BLOCKED"
    print(f"\n[{step}] Guardrail verdict: {verdict}")
    if reason:
        print(f"[{step}] Reason: {reason}")
