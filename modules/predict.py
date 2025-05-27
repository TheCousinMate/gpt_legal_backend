from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils_output import create_success_response, create_error_response

router = APIRouter()

class PredictInput(BaseModel):
    contexto: str

@router.post("/predict")
def predecir_riesgo(input_data: PredictInput):
    try:
        contexto = input_data.contexto

        # Simulación de lógica predictiva
        resultado = {
            "riesgo": "Moderado",
            "recomendacion": "Solicitar audiencia preparatoria antes del 15 de junio"
        }

        return create_success_response(
            message="Predicción jurídica completada",
            data={
                "input": contexto,
                "evaluacion": resultado,
                "base_legal": {
                    "CPC art. 254": "Requisitos de la demanda",
                    "Ley 19.968 art. 3": "Competencia del Juzgado de Familia"
                },
                "derecho_comparado": {
                    "España": "Ley de Enjuiciamiento Civil, art. 399",
                    "México": "Código Federal de Procedimientos Civiles, art. 322"
                },
                "estandares_internacionales": [
                    "CIDH: Caso Baena Ricardo y otros vs. Panamá, 2001",
                    "ONU: Reglas de Brasilia sobre Acceso a la Justicia"
                ],
                "contradicciones": [
                    "Conflicto entre CPC y ley especial en tramitación",
                    "Interpretación divergente en jurisprudencia reciente"
                ],
                "fuentes": [
                    {"title": "Código Procesal Civil", "url": "https://bcn.cl/2f4rs"},
                    {"title": "Ley 19.968", "url": "https://bcn.cl/1x2le"}
                ]
            }
        )
    except Exception as e:
        return create_error_response("Error en predicción jurídica", str(e))
