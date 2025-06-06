from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class InterpretacionInput(BaseModel):
    mensaje: str

@router.post("/")
def interpretarLegal(data: InterpretacionInput):
    # Lógica de interpretación aquí
    return {"interpretacion": f"Interpretación legal de: {data.mensaje}"}
