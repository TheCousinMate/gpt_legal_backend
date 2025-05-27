from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ContextoInput(BaseModel):
    contexto: str

@router.post("/reflexion/")
def reflexionar(data: ContextoInput):
    contexto = data.contexto.strip().lower()
    if not contexto:
        raise HTTPException(status_code=400, detail="Debe proporcionar un contexto.")
    return {
        "respuesta": "Análisis doctrinal completado",
        "clasificacion": "Exitoso",
        "justificacion": "Operación completada correctamente"
    }
