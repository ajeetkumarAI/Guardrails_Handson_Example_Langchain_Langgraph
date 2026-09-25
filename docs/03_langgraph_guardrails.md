# LangGraph Guardrails

LangChain is well suited to a single request/response pass. The moment a
workflow needs **state that persists across steps**, **branching that
depends on that state**, or **a pause for a human decision**, a plain
chain becomes awkward to express and hard to reason about. That is the
gap LangGraph fills in this repository.

## What LangGraph guardrails cover here

- **Stateful workflows** (`langgraph_guardrails/state.py`) - a single
  `GraphState` TypedDict carries counters, flags, and working text across
  every node in a run.
- **Conditional routing** (`langgraph_guardrails/routing.py`) - pure
  functions of state that decide the next node: allowed/blocked,
  safe/off-topic/unsafe/pii, retry/escalate, and more.
- **Retry flows** - a bounded loop between an `agent` node and a
  `validate_output` node, capped by `MAX_RETRIES`.
- **Approval workflows / human-in-the-loop** - a `human_approval` node
  that simulates a reviewer, used before any mock sensitive action runs.
- **Tool execution control** - allowlist checks, argument validation, and
  output validation wrapped around every mock tool call.
- **Agent loop protection** - a hard ceiling (`MAX_TOOL_CALLS`) so a loop
  between "propose tool" and "execute tool" cannot run forever.
- **Escalation flows** - when retries are exhausted, the graph routes to
  an escalation node instead of silently failing or looping.

## Why state-driven routing matters

Every conditional edge in this repository is a plain Python function that
reads `GraphState` and returns a branch name (see `routing.py`). Because
the decision is just a function of state, you can:

- Unit test routing logic without building or running a graph at all.
- Print the state at any point in a run and know exactly why the graph
  is about to go where it's going.
- Add a new branch by adding a new state field and a new `if`, without
  touching the nodes that produced that state.

## Graph shape used across the examples

Most of the LangGraph examples in this repository follow a variation of:

```
START -> input guardrail(s) -> agent -> tool guardrail(s) -> tool
       -> output guardrail -> END
                              \-> retry -> agent (capped)
                              \-> escalate -> END
```

See `examples/langgraph/14_production_style_agent.py` for the fullest
version of this shape, and `docs/06_production_architecture.md` for the
reasoning behind it.
