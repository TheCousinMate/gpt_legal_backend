from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
import openai

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

class PredictInput(BaseModel):
    contexto: str

@router.post("/predict")
async def predecir_riesgo(input_data: PredictInput, request: Request):
    try:
        if not input_data.contexto or len(input_data.contexto.strip()) < 10:
            raise HTTPException(status_code=400, detail="Contexto insuficiente para predicción.")

        prompt_sistema = (
            "Eres un jurista chileno con experiencia forense. A partir del siguiente caso, "
            "evalúa el riesgo jurídico, ofrece una recomendación, menciona contradicciones legales, "
            "y cita normativa chilena, derecho comparado y estándares internacionales relevantes. "
            "Responde en formato estructurado JSON."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": input_data.contexto}
            ],
            temperature=0.25,
            max_tokens=1000
        )

        contenido = completion.choices[0].message["content"]

        return {
            "modelo": "gpt-4o",
            "resultado": contenido.strip(),
            "estatus": "predicción jurídica real"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción jurídica: {str(e)}")