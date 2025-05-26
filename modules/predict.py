from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from utils_output import output_dual
from modules.motor_predictivo import analizar_input_legal

router = APIRouter()

class PrediccionInput(BaseModel):
    contexto: Optional[str] = None
    input: Optional[str] = None
    texto: Optional[str] = None

@router.post("/predict")
def predecir_riesgo(data: PrediccionInput):
    contenido = (data.contexto or data.input or data.texto or "").strip()
    if not contenido:
        raise HTTPException(status_code=400, detail="Debe ingresar al menos un campo: contexto, input o texto.")

    analisis = analizar_input_legal(contenido)

    resultado = {
        "respuesta": analisis,
        "clasificacion": "Fuerte",
        "justificacion": "Generado con motor predictivo jurídico especializado",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Predicción jurídica completada",
        "fuentes": [],
        "logs": {
            "input": data.dict(),
            "output": analisis
        }
    }

    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
