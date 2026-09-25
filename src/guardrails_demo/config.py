"""Runtime configuration for the guardrails demo package.

All configuration is pulled from environment variables (optionally loaded
from a local .env file). Nothing here requires real credentials: if no
Google API key is present, the rest of the package falls back to an
offline stub model so every example and test still runs.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Holds the small set of values the demo package cares about."""

    google_api_key: str | None
    google_cloud_project: str | None
    google_cloud_location: str
    model_name: str
    max_retries: int
    max_tool_calls: int

    @property
    def has_live_credentials(self) -> bool:
        """True when a real Gemini call is possible."""
        return bool(self.google_api_key)


def load_settings() -> Settings:
    """Read environment variables into a Settings object."""
    return Settings(
        google_api_key=os.getenv("GOOGLE_API_KEY") or None,
        google_cloud_project=os.getenv("GOOGLE_CLOUD_PROJECT") or None,
        google_cloud_location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        model_name=os.getenv("GUARDRAILS_MODEL_NAME", "gemini-1.5-flash"),
        max_retries=int(os.getenv("GUARDRAILS_MAX_RETRIES", "2")),
        max_tool_calls=int(os.getenv("GUARDRAILS_MAX_TOOL_CALLS", "4")),
    )


settings = load_settings()
