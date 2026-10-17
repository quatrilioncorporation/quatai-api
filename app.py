
import os
import secrets

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="QuatAI API")

API_KEY = os.environ.get("QUATAI_API_KEY")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)

@app.get("/")
def home():
    return {"name": "QuatAI", "status": "online"}

@app.post("/v1/chat")
def chat(
    body: ChatRequest,
    authorization: str | None = Header(default=None),
):
    if not API_KEY:
        raise HTTPException(503, "API key serverde qurulmayib")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "API key teleb olunur")

    supplied_key = authorization.removeprefix("Bearer ").strip()

    if not secrets.compare_digest(supplied_key, API_KEY):
        raise HTTPException(401, "Yanlis API key")

    return {
        "model": "QuatAI",
        "response": "QuatAI API işləyir! Model bağlantısı hələ qurulmayıb."
    }
