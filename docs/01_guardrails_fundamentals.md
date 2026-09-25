# Guardrails Fundamentals

## What are guardrails?

A guardrail is any check your application runs, deliberately, around a
model call - before it, after it, or both - to keep the system's behavior
within limits you define. A guardrail can be as simple as "reject empty
input" or as involved as "route this request to a human before it touches
a production system."

## Why prompt instructions alone are not enough

Telling a model "never reveal secrets" or "only answer Python questions"
in a system prompt shapes its behavior, but it is not enforcement. A
system prompt is a strong suggestion the model tries to follow; it is not
a wall the model cannot get past. Creative phrasing, long conversations,
or unusual inputs can all erode that instruction over time. Guardrails
exist because relying purely on the model to police itself leaves no
independent, deterministic layer checking the outcome.

## Validation vs. enforcement

- **Validation** answers the question "is this allowed?" It produces a
  verdict (allowed/blocked) and, ideally, a reason.
- **Enforcement** is what actually happens as a result: rejecting the
  request, redacting part of it, routing to a different path, or stopping
  execution entirely.

A validator that nobody listens to changes nothing. Every guardrail in
this repository pairs a validation step with code that acts on the result.

## Deterministic checks vs. LLM-based checks

| | Deterministic (regex, length, allowlist) | LLM-based (classification, judgment) |
|---|---|---|
| Cost | Near zero | A model call |
| Speed | Instant | Slower |
| Coverage | Narrow, exact | Broad, flexible |
| Failure mode | Predictable | Probabilistic |

Neither replaces the other. The pattern used throughout this repository is
to run cheap deterministic checks first, and only escalate to an LLM-based
check when the cheap check is inconclusive (see `docs/07_best_practices.md`).

## Why agents introduce additional concerns

A plain chatbot can, at worst, say something wrong. An **agent** that can
call tools can *do* something wrong - send a message, modify a record,
call an external API with attacker-influenced arguments. Once a model's
output can trigger an action outside the conversation, guardrails have to
cover not just what the model says, but what it is *allowed to do*, with
what arguments, and under whose approval. This is the subject of
`docs/05_agent_security.md`.
