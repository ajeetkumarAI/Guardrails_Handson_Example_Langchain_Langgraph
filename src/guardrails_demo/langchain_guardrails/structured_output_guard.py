"""Validate that a model's structured response actually matches its schema."""
from __future__ import annotations

from typing import Any, Type, TypeVar

from pydantic import BaseModel, ValidationError

from guardrails_demo.common.result import GuardrailResult

SchemaT = TypeVar("SchemaT", bound=BaseModel)


def validate_structured_output(schema: Type[SchemaT], raw: dict[str, Any]) -> GuardrailResult:
    """Try to parse `raw` into `schema`; report exactly what failed if it doesn't."""
    try:
        parsed = schema.model_validate(raw)
    except ValidationError as exc:
        errors = [f"{err['loc']}: {err['msg']}" for err in exc.errors()]
        return GuardrailResult(
            allowed=False,
            category="schema_validation_failed",
            reason="; ".join(errors),
            metadata={"raw_input": raw},
        )
    return GuardrailResult(
        allowed=True,
        category="schema_validation_passed",
        metadata={"parsed": parsed.model_dump()},
    )
