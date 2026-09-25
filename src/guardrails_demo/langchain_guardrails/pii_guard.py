"""Lightweight, regex-based PII detection and redaction.

Educational note: these patterns are intentionally simple. They are not a
substitute for a real data-loss-prevention (DLP) product. Real systems use
context-aware models, allowlists/denylists, locale-aware phone/ID formats,
and audited logging.
"""
from __future__ import annotations

import re

from guardrails_demo.common.result import GuardrailResult

PATTERNS: dict[str, re.Pattern[str]] = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "phone": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "ip_address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}


def detect_pii(text: str) -> GuardrailResult:
    """Return a blocked result listing every PII category found in `text`."""
    found: dict[str, list[str]] = {}
    for category, pattern in PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            found[category] = matches

    if found:
        categories = ", ".join(found.keys())
        return GuardrailResult(
            allowed=False,
            category="pii_detected",
            reason=f"Detected potential PII: {categories}",
            metadata={"matches": found},
        )
    return GuardrailResult.allow("pii_detected")


def redact_pii(text: str) -> str:
    """Replace each recognised PII pattern with a category-labelled placeholder."""
    redacted = text
    for category, pattern in PATTERNS.items():
        placeholder = f"[{category.upper()}_REDACTED]"
        redacted = pattern.sub(placeholder, redacted)
    return redacted
