# backend/api/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import importlib

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 256

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Try to call llm_client.generate if available
    try:
        lc = importlib.import_module("llm_client")
        if hasattr(lc, "generate"):
            out = lc.generate(request.prompt, max_tokens=request.max_tokens)
            return {"reply": out}
    except Exception:
        pass
    # fallback
    return {"reply": f"[LLM not configured] Echo: {request.prompt}"}
