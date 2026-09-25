"""Shared Pydantic schemas used across the LangChain and LangGraph examples."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ProductReview(BaseModel):
    """Example structured-output target for Example 07 (structured output)."""

    sentiment: Literal["positive", "negative", "neutral"]
    summary: str = Field(min_length=1, max_length=280)
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("summary")
    @classmethod
    def summary_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("summary cannot be blank")
        return value


class CalculatorArguments(BaseModel):
    """Argument schema for the mock calculator tool used in tool-guard examples."""

    operation: Literal["add", "subtract", "multiply", "divide"]
    left: float
    right: float

    @field_validator("right")
    @classmethod
    def no_divide_by_zero(cls, value: float, info):
        if info.data.get("operation") == "divide" and value == 0:
            raise ValueError("cannot divide by zero")
        return value


class WeatherArguments(BaseModel):
    """Argument schema for the mock weather-lookup tool."""

    city: str = Field(min_length=2, max_length=80)


class TicketArguments(BaseModel):
    """Argument schema for a mock sensitive 'create_ticket' write action."""

    title: str = Field(min_length=3, max_length=140)
    priority: Literal["low", "medium", "high", "urgent"]
