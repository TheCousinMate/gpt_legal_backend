from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class VisionInput(BaseModel):
    image_id: str

@router.post("/vision/")
def analizar_imagen(data: VisionInput):
    resultado = {
        "respuesta": f"Se recibió la imagen con identificador '{data.image_id}'. Análisis visual simulado.",
        "clasificacion": "Moderada",
        "justificacion": "Procesamiento real de imágenes pendiente de integración.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Imagen recibida.",
        "fuentes": [],
        "logs": {
            "input": data.dict(),
            "output": "Simulación"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
