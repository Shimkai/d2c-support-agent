import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agent import AgentError, run_agent
from app.config import OLLAMA_MODEL, OLLAMA_URL, REQUEST_TIMEOUT_SECONDS

app = FastAPI(title="D2C Support Agent", version="1.0.0", description="Fictional local-first customer support agent powered by Ollama.")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str | None = Field(default=None, max_length=100)


class ChatResponse(BaseModel):
    answer: str
    handoff: bool
    tool_calls: list[dict]
    latency_ms: int
    usage: dict[str, int]
    model: str
    session_id: str | None


@app.get("/health")
def health() -> dict:
    try:
        response = requests.get(f"{OLLAMA_URL.rstrip('/')}/api/tags", timeout=min(REQUEST_TIMEOUT_SECONDS, 5))
        response.raise_for_status()
        models = [item.get("name", "") for item in response.json().get("models", [])]
        available = any(name == OLLAMA_MODEL or name.startswith(f"{OLLAMA_MODEL}:") for name in models)
        return {"status": "ok" if available else "model_missing", "ollama_reachable": True, "model": OLLAMA_MODEL, "available_models": models}
    except requests.RequestException:
        return {"status": "ollama_unreachable", "ollama_reachable": False, "model": OLLAMA_MODEL}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        return ChatResponse(**run_agent(request.message.strip(), request.session_id))
    except AgentError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
