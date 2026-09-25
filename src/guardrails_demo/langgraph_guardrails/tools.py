"""Mock tools used only to demonstrate guardrails around tool-calling.

None of these tools touch a real external system: send_email and
create_ticket just print what they *would* do. That keeps the examples
safe to run for anyone, anywhere, without configuration.
"""
from __future__ import annotations

from guardrails_demo.schemas import CalculatorArguments, TicketArguments, WeatherArguments

ALLOWED_TOOLS = ["calculator", "weather_lookup"]
SENSITIVE_TOOLS = ["create_ticket", "send_email"]


def run_calculator(args: CalculatorArguments) -> str:
    ops = {
        "add": args.left + args.right,
        "subtract": args.left - args.right,
        "multiply": args.left * args.right,
        "divide": args.left / args.right if args.right != 0 else float("nan"),
    }
    return str(ops[args.operation])


def run_weather_lookup(args: WeatherArguments) -> str:
    # Deterministic mock instead of a real API call.
    return f"Weather lookup for {args.city}: 24C, clear skies (mock data)."


def run_create_ticket(args: TicketArguments) -> str:
    return f"[mock] Ticket created: '{args.title}' (priority={args.priority})"
