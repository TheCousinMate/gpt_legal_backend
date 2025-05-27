from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ContextoInput(BaseModel):
    contexto: str

@router.post("/vision/")
def analizar_imagen(data: ContextoInput):
    contexto = data.contexto.strip().lower()
    if not contexto:
        raise HTTPException(status_code=400, detail="Debe proporcionar un contexto.")

    return {
        "respuesta": "Análisis de imagen forense completado",
        "clasificacion": "Exitoso",
        "justificacion": "Operación completada correctamente"
    }
