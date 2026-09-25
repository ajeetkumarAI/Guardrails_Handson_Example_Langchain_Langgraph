"""Chat model access, with a transparent offline fallback.

Every example in this repository should run for a newcomer who has not
configured any cloud credentials yet. get_chat_model() returns a real
langchain-google-genai chat model when GOOGLE_API_KEY is set, and a tiny
deterministic StubChatModel otherwise. Both expose the same .invoke(text)
-> str interface used throughout the examples, so swapping between them
is invisible to the rest of the code.
"""
from __future__ import annotations

from guardrails_demo.config import settings


class StubChatModel:
    """A deterministic, offline stand-in for a real chat model.

    This is intentionally simple: it does not call any network service.
    It exists so the guardrail patterns in this repository (which are the
    point of the lesson) can be exercised without a Gemini API key.
    """

    name = "stub-offline-model"

    def invoke(self, prompt: str) -> str:
        cleaned = prompt.strip()
        if not cleaned:
            return "I did not receive any input to respond to."
        return f"[stub-response] Here is a placeholder answer for: {cleaned[:200]}"


class GeminiChatModel:
    """Thin wrapper around langchain-google-genai's ChatGoogleGenerativeAI."""

    def __init__(self, model_name: str) -> None:
        from langchain_google_genai import ChatGoogleGenerativeAI

        self.name = model_name
        self._client = ChatGoogleGenerativeAI(model=model_name)

    def invoke(self, prompt: str) -> str:
        result = self._client.invoke(prompt)
        content = getattr(result, "content", result)
        return str(content)


def get_chat_model():
    """Return a live Gemini model if credentials exist, else an offline stub."""
    if settings.has_live_credentials:
        try:
            return GeminiChatModel(settings.model_name)
        except Exception:
            # Fall back gracefully rather than crashing a learning example.
            return StubChatModel()
    return StubChatModel()
