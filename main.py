from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx
import os

app = FastAPI(title="Carlo Health Chatbot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a knowledgeable, empathetic Health Assistant. Your role is to:
- Provide clear, accurate, evidence-based general health information
- Help users understand symptoms, conditions, medications, nutrition, and wellness
- Always remind users that your responses are informational only and not a substitute for professional medical advice
- Recommend consulting a qualified healthcare professional for personal diagnosis or treatment
- Be warm, calm, and reassuring in tone — never alarmist
- Keep responses concise and easy to understand

You must never:
- Diagnose a specific condition for the user
- Prescribe or recommend specific medications or dosages
- Provide emergency medical advice — always direct to emergency services if urgent"""


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = MODEL
    max_tokens: int = 1024


class ChatResponse(BaseModel):
    choices: List[dict]


@app.get("/")
def root():
    return {"status": "Carlo Health Backend is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in request.messages]

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GROQ_ENDPOINT,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": request.model,
                "messages": messages,
                "max_tokens": request.max_tokens,
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Groq error: {response.text}")

    return response.json()
