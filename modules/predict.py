from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class PrediccionInput(BaseModel):
    contexto: str

@router.post("/predict")
def predecir_riesgo(data: PrediccionInput):
    texto = data.contexto.strip().lower()
    if not texto:
        raise HTTPException(status_code=400, detail="Debe ingresar un contexto jurídico para evaluación.")

    riesgo = "Bajo"
    justificacion = "No se detectaron patrones críticos en el texto proporcionado."
    alertas = []

    if any(palabra in texto for palabra in ["fraude", "inconstitucional", "incumplimiento", "nulidad", "arbitrariedad"]):
        riesgo = "Alto"
        justificacion = "Se detectaron términos indicativos de riesgo legal significativo."
        alertas.append("Conflicto potencial con principios fundamentales.")

    elif any(palabra in texto for palabra in ["ambigüedad", "falta de competencia", "vacío legal"]):
        riesgo = "Moderado"
        justificacion = "Se identifican riesgos interpretativos o de competencia normativa."
        alertas.append("Necesidad de revisión doctrinal y jurisprudencial.")

    resultado = {
        "respuesta": f"Nivel de riesgo normativo: {riesgo}",
        "clasificacion": riesgo,
        "justificacion": justificacion,
        "base_legal": {
            "Ley 19880": "Sobre procedimientos administrativos. Principios de juridicidad y motivación.",
            "Corte Suprema Rol 8632-2021": "Invalidez por infracción de principios esenciales del procedimiento."
        } if riesgo != "Bajo" else {},
        "derecho_comparado": {
            "España - STS 298/2013": "La ambigüedad normativa genera inseguridad jurídica.",
            "Colombia - C-084/2018": "El vacío legal requiere interpretación conforme a la Constitución."
        } if riesgo != "Bajo" else {},
        "contradicciones": alertas,
        "estandares_internacionales": ["Convención Americana art. 8 y 25"],
        "esquema_visual": f"Riesgo: {riesgo}",
        "sintesis_audio": f"Evaluación de riesgo legal resultó en nivel {riesgo}.",
        "fuentes": [],
        "logs": {
            "input": data.dict(),
            "output": "Predicción legal realizada con reglas probabilísticas básicas."
        }
    }

    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
