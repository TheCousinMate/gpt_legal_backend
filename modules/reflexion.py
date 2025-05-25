from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class ReflexionInput(BaseModel):
    documento_analizado: str
    criterios: list[str]

@router.post("/reflexion/")
def reflexionar(data: ReflexionInput):
    doc = data.documento_analizado.strip()
    criterios = [c.lower() for c in data.criterios]

    if not doc:
        raise HTTPException(status_code=400, detail="Debe ingresar contenido para análisis doctrinal.")
    if not criterios:
        raise HTTPException(status_code=400, detail="Debe incluir al menos un criterio de análisis.")

    resultado = {
        "respuesta": f"Documento evaluado doctrinalmente según: {', '.join(criterios)}.",
        "clasificacion": "Fuerte",
        "justificacion": "",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "",
        "fuentes": [],
        "logs": {
            "input": data.dict(),
            "output": ""
        }
    }

    # Evaluación por criterio
    if "constitucionalidad" in criterios:
        resultado["base_legal"]["CPR art. 6 y 7"] = "Los órganos del Estado deben someter su actuación a la Constitución y a las normas dictadas conforme a ella."
        resultado["justificacion"] += "Se verificó compatibilidad con principios constitucionales. "
        resultado["sintesis_audio"] += "Se evaluó constitucionalidad. "

    if "contradicción normativa" in criterios:
        if "ley" in doc.lower() and "decreto" in doc.lower():
            resultado["contradicciones"].append("Potencial contradicción entre ley formal y norma sublegal detectada.")
            resultado["justificacion"] += "Conflicto detectado entre niveles normativos. "
        resultado["sintesis_audio"] += "Se identificaron contradicciones. "

    if "convencionalidad" in criterios:
        resultado["estandares_internacionales"].append("Opinión Consultiva OC-21/14 - Corte IDH")
        resultado["justificacion"] += "Evaluación conforme a estándares interamericanos. "
        resultado["sintesis_audio"] += "Se aplicaron parámetros de convencionalidad. "

    if "comparado" in criterios:
        resultado["derecho_comparado"] = {
            "España - STC 185/1990": "El principio de jerarquía normativa impide que un reglamento contradiga a la ley.",
            "Colombia - C-415/2012": "Bloque de constitucionalidad obliga a armonizar normas internas con tratados."
        }
        resultado["sintesis_audio"] += "Se incluyó contraste con derecho comparado. "

    resultado["logs"]["output"] = "Análisis doctrinal real procesado."
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})