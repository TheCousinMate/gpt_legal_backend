from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PredictInput(BaseModel):
    entrada: str

@router.post("/")
def predecir(data: PredictInput):
    # Lógica de predicción aquí
    return {"prediccion": f"Predicción generada desde: {data.entrada}"}
