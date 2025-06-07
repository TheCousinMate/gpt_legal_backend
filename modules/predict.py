from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter()


class PredictInput(BaseModel):
    contexto: str | None = None
    texto: str | None = None
    entrada: str | None = None


@router.post("/predict")
def predecir(data: PredictInput):
    """Invoke the language model and return the result."""
    prompt = data.contexto or data.texto or data.entrada or ""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    content = resp.choices[0].message["content"]
    return {"resultado": content}
