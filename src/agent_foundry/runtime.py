from datetime import datetime, timezone
from uuid import uuid4

from .contracts import RunRequest, RunResult, RunState, ToolCall
from .tools import execute_tool


class AgentRuntime:
    """Deterministic runtime seam; a model planner can be added without changing policy/execution."""

    def run(self, request: RunRequest) -> RunResult:
        run_id = str(uuid4())
        events: list[dict[str, str]] = []

        def record(state: RunState) -> None:
            events.append(
                {"state": state.value, "at": datetime.now(timezone.utc).isoformat()}
            )

        record(RunState.RECEIVED)
        call = ToolCall(name="create_follow_up", arguments={"title": request.task})
        record(RunState.PLANNED)

        if request.dry_run:
            record(RunState.SUCCEEDED)
            return RunResult(
                run_id=run_id,
                state=RunState.SUCCEEDED,
                output={"dry_run": True, "planned_tool": call.model_dump()},
                events=events,
            )

        try:
            record(RunState.RUNNING)
            output = execute_tool(call)
            record(RunState.SUCCEEDED)
            return RunResult(run_id=run_id, state=RunState.SUCCEEDED, output=output, events=events)
        except (ValueError, KeyError) as error:
            record(RunState.FAILED)
            return RunResult(
                run_id=run_id,
                state=RunState.FAILED,
                output={"error": str(error)},
                events=events,
            )
