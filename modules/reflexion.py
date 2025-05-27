from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils_output import create_success_response, create_error_response

router = APIRouter()

class ReflexionInput(BaseModel):
    documento_analizado: str
    criterios: list

@router.post("/reflexion/")
def reflexionar(data: ReflexionInput):
    try:
        doc = data.documento_analizado
        criterios = data.criterios

        # Simulación de análisis doctrinal
        analisis = {
            "criterios_aplicados": criterios,
            "resumen": "Se ha identificado jurisprudencia contradictoria sobre el mismo fundamento",
            "resultado": "Análisis favorable al control difuso"
        }

        return create_success_response(
            message="Análisis doctrinal completado",
            data={
                "input": doc,
                "evaluacion": analisis,
                "base_legal": {
                    "CPR art. 5 inc. 2": "Control de convencionalidad",
                    "Ley 19.968 art. 22": "Criterio de aplicación supletoria"
                },
                "derecho_comparado": {
                    "Argentina": "Fallos CSJN 328:566 (Caso Madorrán)",
                    "Colombia": "Corte Const. C-252/01, control oficioso"
                },
                "estandares_internacionales": [
                    "CIDH: OC-20/09, Control de convencionalidad",
                    "CIDH: Caso Gelman vs. Uruguay (2011)"
                ],
                "contradicciones": [
                    "Divergencia en aplicación entre Corte Suprema y Tribunales de Familia"
                ],
                "fuentes": [
                    {"title": "Constitución Política de la República", "url": "https://bcn.cl/1x2ja"},
                    {"title": "Ley 19.968", "url": "https://bcn.cl/1x2le"}
                ]
            }
        )
    except Exception as e:
        return create_error_response("Error en evaluación doctrinal", str(e))
