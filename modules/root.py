from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

@router.get("/status/json")
def status_json():
    resultado = {
        "respuesta": "El backend está operativo y responde en JSON y Markdown.",
        "clasificacion": "Fuerte",
        "justificacion": "Sistema activo.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Sistema activo.",
        "fuentes": [],
        "logs": {
            "input": None,
            "output": "ok"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
