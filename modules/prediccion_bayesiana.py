from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual
from modules.motor_predictivo import analizar_input_legal

router = APIRouter()

class PrediccionInput(BaseModel):
    contexto: str

@router.post("/api/prediccion/")
def predecir_riesgo(datos: PrediccionInput):
    if not datos.contexto or len(datos.contexto.strip()) < 50:
        raise HTTPException(status_code=422, detail="Contexto legal insuficiente para análisis de riesgo.")

    analisis = analizar_input_legal(datos.contexto)

    resultado = {
        "respuesta": analisis,
        "clasificacion": "Fuerte",
        "justificacion": "El análisis fue generado mediante reglas jurídicas programadas.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Resultado de riesgo legal generado.",
        "fuentes": [],
        "logs": {
            "input": datos.dict(),
            "output": analisis
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
