# Best Practices and Guardrail Ordering

## Order checks from cheap to expensive

1. **Type / length / emptiness** - pure Python, no dependencies.
2. **Pattern matching** (regex for PII, keyword lists for topic/safety) -
   still no model call, slightly more logic.
3. **Semantic / LLM-based classification** - a model call, used only when
   the cheaper checks are inconclusive (see
   `langchain_guardrails/topic_guard.py::topic_guard`, which escalates to
   `llm_topic_guard` only when the keyword check is unsure).
4. **The agent/model call itself.**
5. **Tool authorization, then tool argument validation, then execution.**
6. **Output validation** on whatever comes back, before it reaches the user.

## Guardrail chaining, concretely

`examples/langchain/12_combined_langchain_guardrails.py` and
`langgraph_guardrails/workflows.py::build_multi_guardrail_pipeline_graph`
both chain input validation -> PII handling -> topic check -> safety
check -> model call -> output validation, stopping at the first failure.
Chaining, rather than running every check regardless of outcome, avoids
paying for checks that no longer matter once a request is already
rejected.

## Keep guardrail results uniform

Every guardrail in this repository returns the same `GuardrailResult`
shape (`common/result.py`): `allowed`, `reason`, `category`, `confidence`,
`modified_input`, `metadata`. A LangGraph node can wrap any LangChain
guardrail function without a translation layer, because the return shape
never changes.

## Don't let retries loop forever

Every retry loop in this repository (`build_output_guardrail_graph`,
`build_retry_and_repair_graph`, `build_escalation_workflow_graph`) has a
hard `MAX_RETRIES` ceiling, and every tool loop
(`build_agent_loop_protection_graph`) has a hard `MAX_TOOL_CALLS` ceiling.
An unbounded retry or tool loop is a guardrail gap, not a convenience.

## Fail closed, not open

`check_tool_allowlist` rejects any tool not explicitly listed, rather than
allowing anything not explicitly blocked. Every guardrail in this
repository follows the same deny-by-default posture: an inconclusive or
unknown case is treated as a reason to escalate or reject, not to proceed.

## Test guardrails without a live model

Every test in `tests/` runs against the deterministic guardrail functions
directly, or against LangGraph flows using the offline `StubChatModel`
(see `guardrails_demo/models.py`). None of them require network access or
an API key - mock or stub the model boundary so your guardrail logic can
be tested on its own.
