from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class VisionInput(BaseModel):
    image_id: str

@router.post("/vision/")
def analizar_imagen(data: VisionInput):
    if not data.image_id or len(data.image_id.strip()) == 0:
        raise HTTPException(status_code=400, detail="Debe proporcionar un identificador de imagen válido.")

    resultado = {
        "respuesta": f"Se recibió la imagen con identificador '{data.image_id}'. Análisis visual forense registrado.",
        "clasificacion": "Moderada",
        "justificacion": "Identificador procesado. Procesamiento visual profundo aún en expansión.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Imagen recibida para análisis forense.",
        "fuentes": [],
        "logs": {
            "input": data.dict(),
            "output": "Recepción y registro confirmados."
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
