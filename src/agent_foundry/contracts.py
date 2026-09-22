from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RunState(str, Enum):
    RECEIVED = "received"
    PLANNED = "planned"
    AWAITING_APPROVAL = "awaiting_approval"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ToolCall(BaseModel):
    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class RunRequest(BaseModel):
    task: str = Field(min_length=1, max_length=2_000)
    dry_run: bool = True
    idempotency_key: str | None = Field(default=None, min_length=1, max_length=128)


class RunResult(BaseModel):
    run_id: str
    state: RunState
    output: dict[str, Any] = Field(default_factory=dict)
    events: list[dict[str, Any]] = Field(default_factory=list)
