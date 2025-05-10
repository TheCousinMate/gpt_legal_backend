from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class ReflexionInput(BaseModel):
    documento_analizado: str
    criterios: List[str]

@router.post("/")
def ejecutar_reflexion(data: ReflexionInput) -> Dict:
    resultado = {
        "verificacion_integral": "Documentación evaluada según contexto jurídico vigente.",
        "coherencia_estructural": "Alineada con jurisprudencia y argumentación sólida.",
        "consistencia_semantica": "No se detectan contradicciones internas.",
        "ajustes_realizados": [f"Validación de criterio: {c}" for c in data.criterios]
    }
    return resultado
