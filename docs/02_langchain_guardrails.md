# LangChain Guardrails

This repository uses LangChain for everything that revolves around a
single model call: preparing input, calling the model, and checking what
comes back.

## What LangChain guardrails cover here

- **Input validation** (`langchain_guardrails/input_validation.py`) - type,
  emptiness, length checks before a model is ever invoked.
- **Output validation** (`langchain_guardrails/output_validation.py`) -
  emptiness, minimum quality, prohibited-content checks on a response.
- **PII detection and redaction** (`langchain_guardrails/pii_guard.py`) -
  regex-based, clearly labelled as educational rather than enterprise DLP.
- **Topic guardrails** (`langchain_guardrails/topic_guard.py`) - keyword
  matching escalating to an LLM classifier only when needed.
- **Content safety** (`langchain_guardrails/safety_guard.py`) - a generic,
  labelled safe/unsafe keyword check standing in for a real moderation
  classifier.
- **Structured output validation** (`langchain_guardrails/structured_output_guard.py`)
  - Pydantic-schema enforcement on model output.
- **Tool guardrails** (`langchain_guardrails/tool_guard.py`) - argument
  validation, allowlisting, and output-shape checks for tool calls.

## When a LangChain-only pipeline is enough

If your application is a single request -> single model call -> single
response, with no multi-step retries, no branching logic, and no need to
pause for a human, a LangChain pipeline of guardrail functions wired
around one model call is sufficient and simpler to reason about than a
full graph. Example 12 (`examples/langchain/12_combined_langchain_guardrails.py`)
shows exactly this shape.

The moment you need retries with a cap, multiple named branches, or a
step that waits on an external decision, you are better served by
LangGraph - see `docs/04_langchain_vs_langgraph.md`.
