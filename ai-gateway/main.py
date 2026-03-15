import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import json
import asyncio
import uvicorn

load_dotenv()

CURRENT_MODEL = "claude-sonnet-4-6"

@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not found")
    
    app.state.anthropic_client = AsyncAnthropic(api_key=api_key)
    yield
    await app.state.anthropic_client.close()

app = FastAPI(title="Anthropic Product Sprint - Gateway", lifespan=lifespan)

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str

class ChatRequest(BaseModel):
    model: str = CURRENT_MODEL
    messages: List[Message]
    max_tokens: Optional[int] = 4096
    temperature: float = Field(default=0.7, ge=0, le=1)

@app.post("/v1/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = await app.state.anthropic_client.messages.create(
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            messages=[msg.model_dump() for msg in request.messages]
        )
        
        return {
            "id": response.id,
            "content": response.content[0].text,
            "usage": response.usage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/v1/chat/stream")
async def chat_stream(request: ChatRequest):
    # The event generator handles the persistent connection
    async def event_generator():
        try:
            # In 2026, the .stream() helper is highly optimized for Claude 4.6
            async with app.state.anthropic_client.messages.stream(
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                messages=[msg.model_dump() for msg in request.messages]
            ) as stream:
                # Loop through the stream as tokens are generated
                async for text in stream.text_stream:
                    # SSE standard format: "data: <JSON>\n\n"
                    # Sending as JSON allows the client to parse metadata easily
                    yield f"data: {json.dumps({'text': text})}\n\n"
                    
                # Send a final signal so the client knows to close the connection
                yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
