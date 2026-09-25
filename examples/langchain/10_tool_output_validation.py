"""
Example 10 - Tool Output Validation (LangChain layer)

Objective:
    Validate a tool's response before it goes back to the model.
Concept:
    tool -> output validator -> LLM.
    Reject malformed or unexpectedly-typed/empty tool output.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.tool_guard import validate_tool_output

if __name__ == "__main__":
    print("Tool output:", "24C, clear skies")
    result = validate_tool_output("24C, clear skies")
    print_guardrail_report("tool_output_validation", result.allowed, result.reason)

    print("\nTool output:", "")
    result = validate_tool_output("")
    print_guardrail_report("tool_output_validation", result.allowed, result.reason)

    print("\nTool output:", 42, "(wrong type, expected str)")
    result = validate_tool_output(42, expected_type=str)
    print_guardrail_report("tool_output_validation", result.allowed, result.reason)
