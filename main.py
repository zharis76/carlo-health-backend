from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Carlo Health Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a knowledgeable, empathetic Health Assistant.
Provide clear, accurate general health information.
Always remind users your responses are informational only — not a substitute for professional medical advice.
Never diagnose or prescribe medications."""

@app.get("/")
def root():
    return {"status": "Carlo Health Backend is running"}

@app.post("/chat")
async def chat(request: dict):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m["role"], "content": m["content"]} for m in request.get("messages", [])]

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            GROQ_ENDPOINT,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": request.get("model", MODEL),
                "messages": messages,
                "max_tokens": request.get("max_tokens", 1024),
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Groq error: {response.text}")

    return response.json()