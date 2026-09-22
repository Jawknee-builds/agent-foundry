from collections.abc import Mapping
from typing import Any

from .contracts import ToolCall


class PolicyError(ValueError):
    """Raised when a proposed tool call violates the execution policy."""


ALLOWED_TOOLS = {"create_follow_up"}


def validate_tool_call(call: ToolCall) -> None:
    if call.name not in ALLOWED_TOOLS:
        raise PolicyError(f"Tool is not allowed: {call.name}")
    if not isinstance(call.arguments, Mapping):
        raise PolicyError("Tool arguments must be an object")
    if len(call.arguments) > 8:
        raise PolicyError("Tool arguments exceed the maximum field count")
