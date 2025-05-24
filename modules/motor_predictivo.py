# motor_predictivo.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils_output import output_dual

router = APIRouter()

class PredictInput(BaseModel):
    texto: str

def analizar_input_legal(texto: str) -> str:
    texto = texto.lower()

    if not texto or len(texto.strip()) == 0:
        return "Texto vacío. Por favor, provea contenido jurídico para análisis."

    if "trabajador" in texto and "contrato" in texto and "informal" in texto:
        return (
            "Existe un riesgo legal elevado. Según el Código del Trabajo chileno, toda relación laboral "
            "requiere contrato por escrito. La falta de formalización puede acarrear multas, pérdida de defensas "
            "legales del empleador, y reconocimiento forzoso de vínculo laboral por parte de la Inspección del Trabajo."
        )
    elif "pago" in texto and "sin contrato" in texto:
        return (
            "Existe riesgo probatorio y fiscal. Aunque haya pago regular, la ausencia de contrato escrito "
            "impide acreditar condiciones pactadas, y expone a la empresa a sanciones por evasión previsional o tributaria."
        )
    elif "falta de delegacion" in texto or "firma no autorizada" in texto or "sin atribucion legal" in texto:
        return (
            "Existe riesgo de nulidad del acto administrativo conforme al artículo 7° de la Constitución Política de la República. "
            "Los actos emitidos sin competencia o delegación formal son jurídicamente inexistentes y pueden ser objeto de control de legalidad."
        )
    elif "riesgo legal" in texto:
        return (
            "Cualquier relación contractual no formalizada correctamente representa riesgo legal. "
            "Es fundamental contar con respaldo documental válido para evitar conflictos o sanciones."
        )
    else:
        return "No se detectó riesgo legal específico, pero se recomienda revisión con asesoría jurídica especializada."

@router.post("/predict")
def predict_riesgo(input_data: PredictInput):
    resultado_texto = analizar_input_legal(input_data.texto)
    resultado = {
        "respuesta": resultado_texto,
        "clasificacion": "Fuerte",
        "justificacion": "El endpoint predict fue alcanzado exitosamente.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": resultado_texto,
        "fuentes": [],
        "logs": {
            "input": input_data.texto,
            "output": "Respuesta generada correctamente"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
