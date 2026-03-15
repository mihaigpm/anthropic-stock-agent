import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI(title="Anthropic Product Sprint - Gateway")

# 1. Structured Data Models
class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str

class ChatRequest(BaseModel):
    model: str = "claude-3-5-sonnet-20240620"
    messages: List[Message]
    max_tokens: Optional[int] = 1024
    temperature: float = Field(default=0.7, ge=0, le=1)

# 2. Health Check (Standard for Kubernetes Liveness Probes)
@app.get("/health")
def health_check():
    return {"status": "healthy", "cluster": "local-orbstack"}

# 3. The Core Endpoint
@app.post("/v1/chat")
async def chat_endpoint(request: ChatRequest):
    # TODO involve the real Anthropic SDK.
    return {
        "id": "mock_123",
        "role": "assistant",
        "content": f"Received {len(request.messages)} messages. Ready for Claude integration."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)