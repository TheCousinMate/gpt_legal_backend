# modules/forensics_proxy.py

import os
import openai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/proxy")

openai.api_key = os.getenv("OPENAI_API_KEY")

class ProxyInput(BaseModel):
    input: str

@router.post("/")
async def analizar_proxy(data: ProxyInput):
    """
    Realiza un análisis forense legal a partir de la entrada proporcionada.
    """
    try:
        if not data.input or len(data.input.strip()) < 10:
            raise HTTPException(status_code=400, detail="La entrada es demasiado corta para análisis forense.")

        prompt = (
            "Eres un jurista chileno con especialidad en análisis forense legal. "
            "Responde de forma estructurada, considerando normas chilenas, contradicciones legales, jurisprudencia y estándares internacionales si aplican."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": data.input}
            ],
            temperature=0.2,
            max_tokens=900
        )

        contenido = completion.choices[0].message["content"]

        return JSONResponse(content={
            "resultado": contenido.strip(),
            "fuente": "GPT-4o (IA jurídica forense real)",
            "entrada": data.input
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis forense: {str(e)}")
