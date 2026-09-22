from collections.abc import Callable
from typing import Any

from .contracts import ToolCall
from .policy import validate_tool_call

ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


def create_follow_up(arguments: dict[str, Any]) -> dict[str, Any]:
    title = str(arguments.get("title", "")).strip()
    if not title:
        raise ValueError("title is required")
    return {"created": True, "title": title}


HANDLERS: dict[str, ToolHandler] = {"create_follow_up": create_follow_up}


def execute_tool(call: ToolCall) -> dict[str, Any]:
    validate_tool_call(call)
    return HANDLERS[call.name](call.arguments)
