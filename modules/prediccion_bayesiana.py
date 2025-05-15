from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class PrediccionInput(BaseModel):
    contexto: str

@router.post("/api/prediccion/")
def predecir_riesgo(datos: PrediccionInput):
    contexto = datos.contexto
    resultado = {
        "respuesta": "Riesgo probable calculado mediante modelo bayesiano simulado.",
        "clasificacion": "Moderada",
        "justificacion": "Modelo bayesiano real pendiente de integrar.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Riesgo probable: alto.",
        "fuentes": [],
        "logs": {
            "input": contexto,
            "output": "ALTO"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
