from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter()


class InterpretacionInput(BaseModel):
    contexto: str | None = None
    pregunta: str | None = None
    mensaje: str | None = None


@router.post("/interpretar")
def interpretarLegal(data: InterpretacionInput):
    """Interpret a legal question or statement."""
    prompt = data.contexto or data.pregunta or data.mensaje or ""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    content = resp.choices[0].message["content"]
    return {"respuesta": content}
