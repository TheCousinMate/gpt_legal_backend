from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter()


class ReflexionInput(BaseModel):
    contexto: str | None = None
    texto: str | None = None
    mensaje: str | None = None


@router.post("/reflexion")
def reflexionar(data: ReflexionInput):
    """Generate a reflection for the provided text."""
    prompt = data.contexto or data.texto or data.mensaje or ""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    content = resp.choices[0].message["content"]
    return {"reflexion": content}
