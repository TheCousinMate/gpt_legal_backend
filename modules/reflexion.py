from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ReflexionInput(BaseModel):
    mensaje: str

@router.post("/")
def reflexionar(data: ReflexionInput):
    # Lógica de reflexión aquí
    return {"respuesta": f"Reflexión sobre: {data.mensaje}"}
