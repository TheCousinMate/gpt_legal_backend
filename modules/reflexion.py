from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
import openai

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ConsultaDoctrinal(BaseModel):
    consulta: str

@router.post("/reflexion")
async def reflexionar(data: ConsultaDoctrinal, request: Request):
    if not data.consulta or len(data.consulta.strip()) < 10:
        raise HTTPException(status_code=400, detail="Consulta demasiado corta.")

    prompt_sistema = (
        "Eres un jurista chileno experto en derecho constitucional, civil y penal. "
        "Responde a la siguiente consulta doctrinal con claridad, citando autores, principios legales y jurisprudencia chilena si aplica."
    )

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": data.consulta}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        respuesta = completion.choices[0].message["content"]

        return {
            "respuesta_doctrinal": respuesta.strip(),
            "estatus": "real",
            "modelo": "gpt-4o"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis doctrinal: {str(e)}")