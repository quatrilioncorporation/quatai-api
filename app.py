
import os
import secrets
import requests
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="QuatAI API")

API_KEY = os.environ.get("QUATAI_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)

@app.get("/")
def home():
    return {"name": "QuatAI", "status": "online"}

@app.post("/v1/chat")
def chat(body: ChatRequest, authorization: str | None = Header(default=None)):
    if not API_KEY or not OPENROUTER_API_KEY or not MODEL_NAME:
        raise HTTPException(503, "Server ayarları tamamlanmayıb")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "API key tələb olunur")

    supplied_key = authorization.removeprefix("Bearer ").strip()

    if not secrets.compare_digest(supplied_key, API_KEY):
        raise HTTPException(401, "Yanlış API key")

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": body.message}],
            },
            timeout=90,
        )
        r.raise_for_status()
        data = r.json()
        return {
            "model": "QuatAI",
            "response": data["choices"][0]["message"]["content"],
        }
    except requests.RequestException:
        raise HTTPException(502, "AI xidmətinə qoşulmaq mümkün olmadı")
