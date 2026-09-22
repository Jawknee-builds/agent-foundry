from agent_foundry.contracts import RunRequest, RunState, ToolCall
from agent_foundry.policy import PolicyError, validate_tool_call
from agent_foundry.runtime import AgentRuntime


def test_dry_run_never_executes_side_effect():
    result = AgentRuntime().run(RunRequest(task="Follow up with Acme", dry_run=True))

    assert result.state == RunState.SUCCEEDED
    assert result.output["dry_run"] is True
    assert result.output["planned_tool"]["name"] == "create_follow_up"


def test_policy_rejects_unknown_tools():
    try:
        validate_tool_call(ToolCall(name="delete_everything"))
    except PolicyError as error:
        assert "not allowed" in str(error)
    else:
        raise AssertionError("unknown tool was accepted")
