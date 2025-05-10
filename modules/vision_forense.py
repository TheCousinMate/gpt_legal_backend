from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
import requests
import os

router = APIRouter()

class VisionInput(BaseModel):
    image_url: HttpUrl
    prompt: str

@router.post("/")
def analizar_imagen(input: VisionInput):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": input.image_url},
                    input.prompt
                ]
            }
        ],
        "max_tokens": 400
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    return response.json()
