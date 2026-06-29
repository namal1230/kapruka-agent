from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from agent import chat
import uvicorn
import os

app = FastAPI(
    title="Kapru — Kapruka Shopping Agent",
    description="AI-powered shopping assistant for Kapruka.com",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        messages = [
            {"role": m.role, "content": m.content}
            for m in request.messages
        ]
        response = await chat(messages)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "Kapru Backend",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    return {
        "message": "Kapru — Kapruka AI Shopping Assistant",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )