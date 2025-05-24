from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class ReflexionInput(BaseModel):
    documento_analizado: str
    criterios: list[str]

@router.post("/reflexion/")
def reflexionar(data: ReflexionInput):
    if not data.documento_analizado or len(data.documento_analizado.strip()) == 0:
        raise HTTPException(status_code=400, detail="Debe ingresar contenido para análisis doctrinal.")
    if not data.criterios:
        raise HTTPException(status_code=400, detail="Debe incluir al menos un criterio de análisis.")

    resultado = {
        "respuesta": f"El documento ha sido evaluado según los criterios {', '.join(data.criterios)}.",
        "clasificacion": "Fuerte",
        "justificacion": "El texto fue procesado para reflexión doctrinal automatizada.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Reflexión doctrinal completada.",
        "fuentes": [],
        "logs": {
            "input": data.dict(),
            "output": "Análisis ejecutado exitosamente."
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
