import os
import openai
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()

# Configurar la API Key de OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("🛑 Falta la variable de entorno OPENAI_API_KEY")
openai.api_key = api_key

class EntradaTexto(BaseModel):
    texto: str

@router.post("/interpretar")
def interpretar_mensaje(data: EntradaTexto):
    return interpretar_input(data.texto)

@router.get("/interpretar")
def interpretar_get(texto: str = Query(..., min_length=3)):
    return interpretar_input(texto)

def interpretar_input(mensaje: str) -> dict:
    mensaje = mensaje.strip()

    if not mensaje or len(mensaje) < 10:
        raise HTTPException(status_code=400, detail="Mensaje demasiado corto para interpretar.")

    try:
        system_prompt = (
            "Eres un modelo jurídico chileno. Clasifica el mensaje en una de estas categorías:\n"
            "- 'predict': caso o problema legal concreto\n"
            "- 'reflexion': consulta doctrinal o interpretativa\n"
            "- 'vision': documento escaneado o evidencia visual\n"
            "Responde SOLO con una de estas tres palabras."
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
                "input_json": {"texto": mensaje},
                "interpretacion": "Clasificado como análisis de riesgo jurídico concreto."
            }
        elif decision == "reflexion":
            return {
                "endpoint": "/reflexion",
                "input_json": {"texto": mensaje},
                "interpretacion": "Clasificado como reflexión o consulta doctrinal."
            }
        elif decision == "vision":
            return {
                "endpoint": "/vision-forense",
                "input_json": {"mensaje": mensaje},
                "interpretacion": "Clasificado como contenido visual o escaneado."
            }
        else:
            raise ValueError("Respuesta IA fuera de rango")

    except Exception as e:
        mensaje_lower = mensaje.lower()
        if any(p in mensaje_lower for p in ["despido", "finiquito", "contrato", "demanda", "juicio", "causa"]):
            return {
                "endpoint": "/predict",
                "input_json": {"texto": mensaje},
                "interpretacion": "Fallback por palabra clave: caso legal concreto."
            }
        elif any(p in mensaje_lower for p in ["nulidad", "jurisprudencia", "constitucional", "derechos", "norma"]):
            return {
                "endpoint": "/reflexion",
                "input_json": {"texto": mensaje},
                "interpretacion": "Fallback por palabra clave: reflexión jurídica."
            }
        elif any(p in mensaje_lower for p in ["imagen", "documento", "foto", "escaneado"]):
            return {
                "endpoint": "/vision-forense",
                "input_json": {"mensaje": mensaje},
                "interpretacion": "Fallback por palabra clave: documento visual."
            }
        raise HTTPException(status_code=500, detail=f"Error interpretando mensaje: {str(e)}")

# 🔧 Función requerida por router_universal → reflexion.py
def generar_reflexion_juridica(texto: str) -> str:
    resultado = interpretar_input(texto)
    return resultado.get("interpretacion", "Sin interpretación")
