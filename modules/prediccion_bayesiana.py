from fastapi import APIRouter
from pydantic import BaseModel
import requests
import os

router = APIRouter()

class BayesInput(BaseModel):
    contexto: str

@router.post("/")
def predecir(data: BayesInput):
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Eres un modelo legal basado en probabilidad condicional."},
            {"role": "user", "content": data.contexto}
        ],
        "temperature": 0.1,
        "max_tokens": 300
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    return r.json()
