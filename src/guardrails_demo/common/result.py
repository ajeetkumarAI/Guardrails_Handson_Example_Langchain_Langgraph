"""The single result type every guardrail in this repository returns.

Keeping one shared shape means a LangChain guardrail and a LangGraph node
can be composed without translation layers between them.
"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class GuardrailResult(BaseModel):
    """Outcome of running one guardrail check.

    Attributes:
        allowed: Whether the checked content may proceed.
        reason: Human-readable explanation, mainly useful when allowed=False.
        category: A short machine-friendly label, e.g. "pii", "off_topic".
        confidence: How sure the check is of its own verdict, 0-1.
        modified_input: Optional cleaned/redacted version of the input.
        metadata: Free-form extra detail (matched patterns, scores, etc).
    """

    allowed: bool
    reason: Optional[str] = None
    category: Optional[str] = None
    confidence: float = 1.0
    modified_input: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def allow(cls, category: str, **metadata: Any) -> "GuardrailResult":
        return cls(allowed=True, category=category, metadata=metadata)

    @classmethod
    def block(cls, category: str, reason: str, **metadata: Any) -> "GuardrailResult":
        return cls(allowed=False, category=category, reason=reason, metadata=metadata)
