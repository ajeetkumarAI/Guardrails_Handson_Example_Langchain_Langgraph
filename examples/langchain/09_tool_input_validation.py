"""
Example 09 - Tool Input Validation (LangChain layer)

Objective:
    Validate tool arguments before a tool ever executes.
Concept:
    User -> LLM -> tool arguments -> validation -> tool.
    Reject malformed or unauthorized arguments up front; never let a tool
    run on unchecked input.
"""
from guardrails_demo.common.utils import print_guardrail_report
from guardrails_demo.langchain_guardrails.tool_guard import validate_tool_arguments
from guardrails_demo.schemas import CalculatorArguments

if __name__ == "__main__":
    good_args = {"operation": "add", "left": 4, "right": 5}
    print("Input:", good_args)
    result = validate_tool_arguments(CalculatorArguments, good_args)
    print_guardrail_report("tool_input_validation", result.allowed, result.reason)

    bad_args = {"operation": "divide", "left": 4, "right": 0}
    print("\nInput:", bad_args)
    result = validate_tool_arguments(CalculatorArguments, bad_args)
    print_guardrail_report("tool_input_validation", result.allowed, result.reason)

    malformed_args = {"operation": "power", "left": "four", "right": 2}
    print("\nInput:", malformed_args)
    result = validate_tool_arguments(CalculatorArguments, malformed_args)
    print_guardrail_report("tool_input_validation", result.allowed, result.reason)
