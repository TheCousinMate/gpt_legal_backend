from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter()


class VisionInput(BaseModel):
    contexto: str | None = None
    image_url: str | None = None


@router.post("/vision")
async def analizarOCR(data: VisionInput):
    """Process an image reference and return a description."""
    prompt = data.contexto or data.image_url or ""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    content = resp.choices[0].message["content"]
    return {"descripcion": content}
