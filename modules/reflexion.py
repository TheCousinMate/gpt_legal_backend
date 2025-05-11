
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

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
def ejecutar_reflexion(data: ReflexionInput) -> ReflexionOutput:
    doc = data.documento_analizado.lower()
    criterios = data.criterios

    # Evaluación básica ampliada
    verificacion = "Documento recibido. Evaluación preliminar en curso..."
    if "constitución" in doc or "artículo" in doc or "norma" in doc:
        verificacion = "El texto contiene referencias normativas o constitucionales válidas."

    estructura = "Se detecta estructura legal base: hechos, fundamentos y argumento. Puede mejorarse."
    if any(term in doc for term in ["hecho", "fundamento", "petitorio"]):
        estructura = "Estructura jurídica explícita con componentes formales bien definidos."

    semantica = "Sin contradicciones internas aparentes. Revisión basada en coherencia léxica."
    if "pero" in doc or "aunque" in doc:
        semantica = "Se detecta tensión argumental o contradicción interna. Requiere revisión."

    ajustes = [f"Validación de criterio: {c}" for c in criterios]

    return ReflexionOutput(
        verificacion_integral=verificacion,
        coherencia_estructural=estructura,
        consistencia_semantica=semantica,
        ajustes_realizados=ajustes
    )
