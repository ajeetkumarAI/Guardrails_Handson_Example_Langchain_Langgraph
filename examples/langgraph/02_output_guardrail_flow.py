"""
Example 02 - Output Guardrail (LangGraph layer)

Flow:
    START -> agent -> validate_output -> END
    Invalid output -> retry -> agent (bounded by MAX_RETRIES)
"""
from guardrails_demo.langgraph_guardrails.state import new_state
from guardrails_demo.langgraph_guardrails.workflows import build_output_guardrail_graph

if __name__ == "__main__":
    graph = build_output_guardrail_graph()
    text = "What is a Python list?"
    print("Input:", text)
    result = graph.invoke(new_state(text))
    print("Guardrail status:", result["guardrail_status"])
    print("Model calls made:", result["model_call_count"])
    print("Output:", result["output"])
