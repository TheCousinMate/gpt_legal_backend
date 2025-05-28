from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
import openai

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

class MensajeInput(BaseModel):
    mensaje: str

# --- Ruta API principal ---
@router.post("/interpretar/")
def interpretar_mensaje(data: MensajeInput):
    return interpretar_input(data.mensaje)

# --- Clasificador IA con fallback lógico ---
def interpretar_input(mensaje: str) -> dict:
    mensaje = mensaje.strip()

    if not mensaje or len(mensaje) < 10:
        raise HTTPException(status_code=400, detail="Mensaje demasiado corto para interpretar.")

    try:
        system_prompt = (
            "Eres un modelo jurídico chileno. Dado un mensaje, clasifícalo en una de estas tres categorías:\n"
            "- 'predict' si describe un caso o problema legal concreto\n"
            "- 'reflexion' si es una consulta doctrinal, constitucional o interpretativa\n"
            "- 'vision' si hace referencia a un documento escaneado, imagen o evidencia visual.\n"
            "Responde SOLO con una de estas palabras: predict, reflexion, vision."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje}
            ],
            temperature=0,
            max_tokens=5
        )

        decision = completion.choices[0].message["content"].strip().lower()

        if decision == "predict":
            return {
                "endpoint": "/predict",
                "input_json": {"contexto": mensaje},
                "interpretacion": "Clasificado como análisis de riesgo jurídico concreto."
            }

        elif decision == "reflexion":
            return {
                "endpoint": "/reflexion",
                "input_json": {"consulta": mensaje},
                "interpretacion": "Clasificado como reflexión o consulta doctrinal."
            }

        elif decision == "vision":
            return {
                "endpoint": "/vision",
                "input_json": {"mensaje": mensaje},
                "interpretacion": "Clasificado como contenido visual o documento escaneado."
            }

        else:
            raise ValueError("Respuesta fuera de rango")

    except Exception as e:
        # Fallback: método por palabras clave
        mensaje_lower = mensaje.lower()
        if any(p in mensaje_lower for p in ["despido", "finiquito", "contrato"]):
            return {
                "endpoint": "/predict",
                "input_json": {"contexto": mensaje},
                "interpretacion": "Fallback: clasificación básica por palabra clave (riesgo jurídico)."
            }
        elif any(p in mensaje_lower for p in ["nulidad", "jurisprudencia", "constitucional"]):
            return {
                "endpoint": "/reflexion",
                "input_json": {"consulta": mensaje},
                "interpretacion": "Fallback: clasificación básica por palabra clave (doctrina)."
            }
        elif any(p in mensaje_lower for p in ["imagen", "documento", "foto"]):
            return {
                "endpoint": "/vision",
                "input_json": {"mensaje": mensaje},
                "interpretacion": "Fallback: clasificación básica por palabra clave (visual)."
            }
        raise HTTPException(status_code=500, detail=f"Error interpretando mensaje: {str(e)}")