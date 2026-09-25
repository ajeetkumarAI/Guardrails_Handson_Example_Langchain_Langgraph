# LangChain vs. LangGraph: Complementary, Not Competing

A common misconception is that LangChain and LangGraph are alternatives
to choose between. In this repository they are used together: LangChain
handles the "one model call, checked on both sides" unit of work, and
LangGraph handles "how many of those units, in what order, with what
branching."

## Side-by-side

| Concern | LangChain | LangGraph |
|---|---|---|
| Single prompt -> model -> response | Natural fit | Overkill |
| Input/output validation on one call | Natural fit | Can host it, but adds ceremony |
| Multi-step retries with a cap | Awkward to express cleanly | Natural fit |
| Branching on accumulated state | Not really its job | Natural fit |
| Pausing for human approval | Not built for this | Natural fit |
| Agent tool-calling loops with limits | Possible, but state tracking is manual | Natural fit |

## A rule of thumb

If you can draw your guardrail logic as a straight line with maybe one
"reject and stop" exit, LangChain alone is enough (see Example 12 in
`examples/langchain/`). If you find yourself drawing arrows that loop back,
branch into more than two paths, or wait on an external decision, you are
describing a graph - and LangGraph will make that graph explicit and
testable rather than living inside nested `if` statements.

## How this repository composes them

`examples/langgraph/*.py` build LangGraph workflows whose individual
*nodes* call straight back into the LangChain-layer guardrail functions
(`langchain_guardrails/*.py`). LangGraph is not a replacement for those
functions - it is the orchestration layer that decides when to call them,
how many times, and what to do with a failure.
