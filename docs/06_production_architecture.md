# Production-Oriented Architecture

## The core principle

```
Cheap deterministic checks
        |
        v
More expensive semantic / LLM-based checks
        |
        v
Agent (LLM decides / responds)
        |
        v
Tool authorization
        |
        v
Tool execution
        |
        v
Output validation
```

Cheap checks run first because they reject a large share of bad requests
for close to zero cost, before anything as expensive as a model call
happens. This is not about any one check being "better" - it's about
spending the most expensive resource (a model call) only on requests that
have already passed the checks that don't need one.

## Why this reduces cost and adds defense in depth

- **Cost:** an empty or oversized request never reaches the model at all.
- **Latency:** deterministic checks return in microseconds.
- **Defense in depth:** even if a semantic or LLM-based check has a blind
  spot, a deterministic check placed earlier (or a tool-level check placed
  later) may still catch the same problem from a different angle.

## The full pipeline demonstrated in this repository

`examples/langgraph/14_production_style_agent.py`
(`langgraph_guardrails/workflows.py::build_production_style_agent_graph`)
puts every layer together:

```
START
  -> Input Validation
  -> PII Check
  -> Prompt Injection Check
  -> Topic Check
  -> Agent
  -> Tool Authorization (allowlist)
  -> Tool Input Validation
  -> Tool Execution
  -> Tool Output Validation
  -> Agent (final response)
  -> Response Validation
  -> END
```

with rejection and escalation branches at every guardrail step. Every
external action in this graph is mocked - see `langgraph_guardrails/tools.py`.

## An important limitation

No guardrail architecture, including this one, provides perfect security.
Treat every pattern here as one layer among several you would combine
with monitoring, access control, rate limiting, human review processes,
and organization-specific policy in a real deployment. See the "Important
Note" at the end of the main README.
