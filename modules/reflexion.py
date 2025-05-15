from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class ReflexionInput(BaseModel):
    documento_analizado: str
    criterios: list[str]

@router.post("/reflexion/")
def reflexionar(data: ReflexionInput):
    resultado = {
        "respuesta": "Texto formalmente adecuado.",
        "clasificacion": "Fuerte",
        "justificacion": "Cumple criterios de coherencia y adecuación legal.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Resumen breve.",
        "fuentes": [],
        "logs": {
            "input": data.dict(),
            "output": "...",
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
