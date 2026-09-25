# LangChain + LangGraph Guardrails

A hands-on, original learning repository for building safe, reliable, and
controlled LLM and agent applications using **LangChain** and
**LangGraph** together.

---

## Introduction

**What are guardrails?** A guardrail is a deliberate check your
application runs around a model call - before it, after it, or both - to
keep behavior inside limits you define, rather than limits the model
infers on its own.

**Why LLM applications need them.** A model will confidently produce
malformed output, wander off-topic, leak formatting it shouldn't, or - if
it can call tools - attempt an action nobody approved. None of that
requires malicious intent from the user; it can just as easily come from
an ambiguous prompt or an edge case the model hasn't seen.

**Why prompt instructions alone are insufficient.** A system prompt is a
strong suggestion the model tries to follow, not a wall it cannot cross.
It has no independent enforcement mechanism - it relies entirely on the
model continuing to comply, which is precisely what long conversations,
unusual phrasing, and injected instructions can erode.

**Validation vs. enforcement.** Validation produces a verdict
(allowed/blocked, with a reason). Enforcement is the code that acts on
that verdict - rejecting, redacting, retrying, or escalating. A validator
nobody listens to changes nothing.

**Deterministic vs. LLM-based checks.** Deterministic checks (length,
regex, allowlists) are instant and free but narrow. LLM-based checks are
flexible but cost a model call and are probabilistic. This repository
runs the cheap check first and escalates to the expensive one only when
needed (`docs/07_best_practices.md`).

**Why agents introduce additional concerns.** A chatbot can, at worst,
say something wrong. An agent that can call tools can *do* something
wrong. Once model output can trigger a real action, guardrails must cover
not just what the model says, but what it's authorized to do, with what
arguments, and under whose approval (`docs/05_agent_security.md`).

---

## Learning objectives

By working through this repository you should come away understanding:

- Input validation
- Output validation
- PII protection (detection and redaction)
- Topic restrictions
- Content safety
- Prompt injection detection
- Structured output validation
- Tool input validation
- Tool output validation
- Retry and repair
- Human approval
- Agent loop protection
- State-based controls
- Multi-layer guardrail architecture

---

## Two layers of architecture

### Layer 1 — LangChain (single-call guardrails)

```
User Input
   |
   v
LangChain preprocessing
   |
   v
Input guardrails
   |
   v
Prompt / Model
   |
   v
Output validation
   |
   v
Final response
```

This layer is enough when your workflow is a straight line: one request,
one model call, checked on both sides, with at most a single
reject-and-stop exit. See `examples/langchain/12_combined_langchain_guardrails.py`.

### Layer 2 — LangGraph (stateful, multi-step guardrails)

```
START
  |
  v
Input Validation
  |
  v
Safety Check
  |
  v
Agent
  |
  v
Tool Validation
  |
  v
Tool Execution
  |
  v
Output Validation
  |
  v
END
```

with rejection, retry, escalation, and human-approval branches at every
gate. Graph orchestration earns its keep once a workflow needs state that
persists across steps, more than a couple of named branches, or a pause
for a human decision - see `docs/04_langchain_vs_langgraph.md`.

## Guardrail architecture

The repository uses layered controls. Cheap deterministic checks run first;
only requests that pass those checks reach model or tool execution. Every
decision is recorded in workflow state so the next node can allow, block,
retry, redact, or escalate the request.

```mermaid
flowchart LR
  U[User request] --> I[Input validation]
  I -->|blocked| R[Reject with reason]
  I -->|allowed| P[PII and safety checks]
  P -->|redact or block| R
  P -->|allowed| T[Topic and injection checks]
  T -->|blocked| R
  T --> A[Agent or model]
  A --> Z{Tool requested?}
  Z -->|no| O[Output validation]
  Z -->|yes| Auth[Tool authorization]
  Auth -->|denied| R
  Auth --> Args[Tool input validation]
  Args -->|invalid| Repair[Repair or retry]
  Args --> Exec[Tool execution]
  Exec --> ToolOut[Tool output validation]
  ToolOut -->|invalid| Repair
  ToolOut --> O
  Repair -->|retry budget remains| A
  Repair -->|budget exhausted| Esc[Human escalation]
  O -->|invalid| Repair
  O -->|valid| Done[Final response]
```

### Common guardrail scenarios

#### Input, PII, and topic checks

```mermaid
flowchart TD
  Start[Incoming text] --> Empty{Empty or too long?}
  Empty -->|yes| Block1[Block request]
  Empty -->|no| PII{PII detected?}
  PII -->|yes| Choice{Redaction enabled?}
  Choice -->|yes| Redact[Redact sensitive values]
  Choice -->|no| Block2[Block request]
  PII -->|no| Topic{Allowed topic?}
  Redact --> Topic
  Topic -->|no| Block3[Block request]
  Topic -->|yes| Model[Continue to model]
```

#### Prompt injection protection

```mermaid
flowchart LR
  Request[User request] --> Detect[Pattern and semantic checks]
  Detect -->|suspicious| Stop[Block before agent]
  Detect -->|clean| Context[Build trusted context]
  Context --> Agent[Run agent]
```

#### Tool authorization and validation

```mermaid
flowchart TD
  Agent[Agent proposes tool call] --> Allowlist{Tool allowlisted?}
  Allowlist -->|no| Deny[Reject action]
  Allowlist -->|yes| Sensitive{Sensitive action?}
  Sensitive -->|yes| Approval{Human approval?}
  Approval -->|no| Pause[Pause or escalate]
  Approval -->|yes| Arguments[Validate arguments]
  Sensitive -->|no| Arguments
  Arguments -->|invalid| Repair[Repair or reject]
  Arguments -->|valid| Execute[Execute least-privilege tool]
  Execute --> Output[Validate tool output]
```

#### Retry, repair, and escalation

```mermaid
flowchart LR
  Response[Model response] --> Validate{Valid output?}
  Validate -->|yes| Return[Return response]
  Validate -->|no| Count{Retry budget left?}
  Count -->|yes| Repair[Repair prompt]
  Repair --> Response
  Count -->|no| Escalate[Escalate to a human]
```

---

## Repository structure

```
langchain-langgraph-guardrails/
├── README.md
├── QUICKSTART.md
├── requirements.txt
├── .env.example
├── docs/                     7 concept guides (fundamentals -> production architecture)
├── src/guardrails_demo/
│   ├── config.py             environment-driven settings
│   ├── models.py             Gemini model, with an offline stub fallback
│   ├── schemas.py            shared Pydantic schemas
│   ├── langchain_guardrails/ input/output/PII/topic/safety/structured/tool guards
│   ├── langgraph_guardrails/ state, nodes, routing, workflows, mock tools
│   └── common/               GuardrailResult, logging, small utils
├── examples/
│   ├── langchain/            12 runnable examples
│   └── langgraph/            14 runnable examples
├── notebooks/                3 walkthrough notebooks
└── tests/                    6 test files, all offline-runnable
```

---

## LangChain examples (`examples/langchain/`)

| # | Example | Concept |
|---|---|---|
| 01 | Input validation | empty / length / type checks before any model call |
| 02 | Output validation | empty / quality / prohibited-content checks |
| 03 | PII detection | regex-based email, phone, credit-card, IP detection |
| 04 | PII redaction | replace detected PII with labelled placeholders |
| 05 | Topic guardrail | keyword -> semantic -> LLM classification, escalating |
| 06 | Content safety | labelled safe/unsafe test cases |
| 07 | Structured output validation | Pydantic schema enforcement |
| 08 | Prompt injection detection | pattern-based instruction-override detection |
| 09 | Tool input validation | reject malformed/unauthorized tool arguments |
| 10 | Tool output validation | reject malformed/unexpected tool output |
| 11 | Retry and repair | bounded retry loop on invalid output |
| 12 | Combined guardrails | input + topic + PII + model + structured + output, chained |

## LangGraph examples (`examples/langgraph/`)

| # | Example | Concept |
|---|---|---|
| 01 | Basic input guardrail flow | START -> validate -> agent, with rejection |
| 02 | Output guardrail flow | agent -> validate -> retry (capped) |
| 03 | PII redaction workflow | detect -> redact -> agent -> validate |
| 04 | Multi-guardrail pipeline | input -> PII -> topic -> safety -> agent -> output |
| 05 | Conditional routing | safe / off-topic / unsafe / pii branches |
| 06 | Retry and repair graph | agent -> validator -> repair loop, capped |
| 07 | Human approval | mock sensitive action gated by a simulated reviewer |
| 08 | Prompt injection protection | detector before the agent ever sees suspicious input |
| 09 | Tool execution guardrail | allowlist -> argument validation -> execute -> output check |
| 10 | Agent loop protection | hard ceiling on tool-calling iterations |
| 11 | Sensitive action approval | mock create_ticket tool, approval-gated |
| 12 | Escalation workflow | retries exhausted -> human escalation |
| 13 | State-based guardrails | routing driven entirely by counters/flags on state |
| 14 | Production-style agent | the full pipeline, end to end |

---

## Guardrail decision table

| Problem | Deterministic check | LLM check | LangChain | LangGraph |
|---|---|---|---|---|
| Empty input | Yes | No | Yes | Optional |
| PII | Yes | Optional | Yes | Yes |
| Topic validation | Limited | Yes | Yes | Yes |
| Prompt injection | Limited | Yes | Yes | Yes |
| Tool authorization | Yes | Optional | Yes | Yes |
| Retry | Yes | Optional | Yes | Yes |
| Human approval | No | Optional | Possible | Strong fit |
| Multi-step routing | No | No | Limited | Strong fit |

Neither framework is universally better - the right choice depends on how
stateful and branching your workflow actually is.

---

## Learning path

**Beginner**
1. What are guardrails? (`docs/01_guardrails_fundamentals.md`)
2. Input validation (LangChain Example 01)
3. Output validation (LangChain Example 02)
4. PII (LangChain Examples 03-04)
5. Structured output (LangChain Example 07)

**Intermediate**
6. Topic validation (LangChain Example 05)
7. Prompt injection (LangChain Example 08)
8. Tool validation (LangChain Examples 09-10)
9. Retry (LangChain Example 11)
10. LangGraph routing (LangGraph Examples 04-05)

**Advanced**
11. Human approval (LangGraph Examples 07, 11)
12. Agent loop protection (LangGraph Example 10)
13. Tool authorization (LangGraph Example 09)
14. State-based controls (LangGraph Example 13)
15. Production architecture (LangGraph Example 14, `docs/06_production_architecture.md`)

---

## Configuration

Copy `.env.example` to `.env` and fill in your own values if you want to
run against real Gemini. Nothing is required to run the examples or
tests - see `guardrails_demo/models.py` for the offline fallback.

`.env` is already listed in `.gitignore`.

---

## What This Repository Demonstrates

- LangChain guardrail patterns (input, output, PII, topic, safety,
  structured output, tool validation)
- LangGraph workflow guardrails (state, routing, retries, human approval,
  agent loop control, escalation)
- Deterministic validation and semantic/LLM-based validation, chained
  cheapest-first
- Prompt injection detection as one layer among several
- Tool security: allowlisting, argument validation, output validation,
  least privilege
- Defense in depth: independent checks stacked so one blind spot is
  covered by another

## Important Note

These examples are educational. A production system built on these
patterns still needs additional security controls, monitoring, access
control, testing, governance, and organization-specific policy. No
guardrail here - or anywhere - provides perfect security.

---

## References

- LangChain documentation: https://python.langchain.com/
- LangGraph documentation: https://langchain-ai.github.io/langgraph/
- Google Gemini / Google GenAI documentation: https://ai.google.dev/gemini-api/docs
- Pydantic documentation: https://docs.pydantic.dev/

---

## Output showcase

The examples run offline with the built-in stub model, so the behavior is
repeatable without an API key. The showcase below captures the three core
outcomes: an allowed request, a blocked prompt injection, and PII detection.

![Terminal output showing allowed, blocked, and PII-detected requests](docs/assets/guardrails-output-showcase.svg)

To reproduce the output locally:

```bash
PYTHONPATH=src python examples/langgraph/01_input_guardrail_flow.py
PYTHONPATH=src python examples/langchain/03_pii_detection.py
pytest -q
```
