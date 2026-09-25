"""Keep a domain-specific assistant on-topic.

Three escalating strategies are shown here, cheapest first:
1. keyword matching (fast, brittle)
2. semantic-ish scoring using simple term overlap (still deterministic)
3. LLM-based classification (flexible, costs a model call)

A production system typically chains 1 -> 3, only paying for the LLM
call when the cheap check is inconclusive.
"""
from __future__ import annotations

from guardrails_demo.common.result import GuardrailResult
from guardrails_demo.models import get_chat_model

ALLOWED_KEYWORDS = ["python", "list", "dict", "function", "loop", "class", "variable", "module"]
OFF_TOPIC_HINTS = ["cricket", "score", "movie", "weather", "recipe", "football"]


def keyword_topic_guard(text: str) -> GuardrailResult:
    lowered = text.lower()
    if any(hint in lowered for hint in OFF_TOPIC_HINTS):
        return GuardrailResult.block(
            "off_topic", "Request looks unrelated to the Python programming domain."
        )
    if any(word in lowered for word in ALLOWED_KEYWORDS):
        return GuardrailResult.allow("on_topic")
    # Neither clearly on nor off topic -> inconclusive, let a smarter check decide.
    return GuardrailResult(allowed=True, category="inconclusive", confidence=0.4)


def llm_topic_guard(text: str) -> GuardrailResult:
    """Escalate an inconclusive case to a model call. Used only when needed."""
    model = get_chat_model()
    prompt = (
        "Answer with only ON_TOPIC or OFF_TOPIC. "
        "The assistant's domain is Python programming help. "
        f"User message: {text}"
    )
    response = model.invoke(prompt).upper()
    if "OFF_TOPIC" in response:
        return GuardrailResult.block(
            "off_topic", "Classifier judged this request outside the supported domain."
        )
    return GuardrailResult.allow("on_topic")


def topic_guard(text: str, escalate_when_unsure: bool = True) -> GuardrailResult:
    """Cheap check first; only call the model when the cheap check is unsure."""
    cheap_result = keyword_topic_guard(text)
    if cheap_result.category != "inconclusive":
        return cheap_result
    if escalate_when_unsure:
        return llm_topic_guard(text)
    return cheap_result
