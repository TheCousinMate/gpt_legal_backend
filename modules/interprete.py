from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class MensajeInput(BaseModel):
    mensaje: str

# --- API Route ---
@router.post("/interpretar/")
def interpretar_mensaje(data: MensajeInput):
    return interpretar_input(data.mensaje)


# --- Función exportable (para main.py y pruebas automáticas) ---
def interpretar_input(mensaje: str) -> dict:
    mensaje = mensaje.lower().strip()

    if not mensaje or len(mensaje) < 10:
        raise HTTPException(status_code=400, detail="Mensaje demasiado corto para interpretar.")

    prediccion_keys = ["despido", "fraude", "finiquito", "contrato", "cotizaciones", "afp", "trabajo informal", "indemnización"]
    reflexion_keys = ["constitucionalidad", "normativa", "nulidad", "vacío legal", "arbitrariedad", "proceso judicial", "jurisprudencia"]
    vision_keys = ["imagen", "visual", "foto", "documento escaneado", "evidencia digital", "firma"]

    if any(p in mensaje for p in prediccion_keys):
        return {
            "endpoint": "/predict",
            "input_json": {"contexto": mensaje},
            "interpretacion": "Se detectó intención de análisis de riesgo jurídico-laboral. Redirigido a endpoint de predicción avanzada."
        }

    elif any(p in mensaje for p in reflexion_keys):
        return {
            "endpoint": "/reflexion/",
            "input_json": {"contexto": mensaje},
            "interpretacion": "Se identificó interés en análisis doctrinal. Redirigido a reflexión jurídica estructurada."
        }

    elif any(p in mensaje for p in vision_keys):
        return {
            "endpoint": "/vision/",
            "input_json": {"contexto": mensaje},
            "interpretacion": "Contenido visual detectado. Redirigido a análisis forense de imagen."
        }

    raise HTTPException(status_code=400, detail="No se pudo interpretar el mensaje. Use términos jurídicos o más contexto.")