from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
import openai
import os

router = APIRouter(prefix="/forensics")

openai.api_key = os.getenv("OPENAI_API_KEY")

@router.get("/search")
async def buscar_forensics(pregunta: str = Query(...)):
    try:
        if not pregunta or len(pregunta.strip()) < 10:
            raise HTTPException(status_code=400, detail="La pregunta es demasiado corta.")

        prompt = (
            "Eres un jurista chileno con especialidad en análisis forense legal. "
            "Responde de forma estructurada, considerando normas chilenas, contradicciones legales, jurisprudencia y estándares internacionales si aplican."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": pregunta}
            ],
            temperature=0.2,
            max_tokens=900
        )

        contenido = completion.choices[0].message["content"]

        return JSONResponse(content={
            "respuesta": contenido.strip(),
            "fuente": "GPT-4o (IA jurídica forense real)",
            "pregunta": pregunta
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis forense: {str(e)}")