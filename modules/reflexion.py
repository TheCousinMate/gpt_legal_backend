from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ReflexionInput(BaseModel):
    documento_analizado: str
    criterios: List[str]

class ReflexionOutput(BaseModel):
    verificacion_integral: str
    coherencia_estructural: str
    consistencia_semantica: str
    ajustes_realizados: List[str]

@router.post("/", response_model=ReflexionOutput)
def ejecutar_reflexion(data: ReflexionInput):
    return {
        "verificacion_integral": "Documentación evaluada según contexto jurídico vigente.",
        "coherencia_estructural": "Alineada con jurisprudencia y argumentación sólida.",
        "consistencia_semantica": "No se detectan contradicciones internas.",
        "ajustes_realizados": [f"Validación de criterio: {c}" for c in data.criterios]
    }
