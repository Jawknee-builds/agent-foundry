from fastapi import FastAPI

from .contracts import RunRequest, RunResult
from .runtime import AgentRuntime

app = FastAPI(title="Agent Foundry", version="0.1.0")
runtime = AgentRuntime()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/runs", response_model=RunResult)
def create_run(request: RunRequest) -> RunResult:
    return runtime.run(request)
