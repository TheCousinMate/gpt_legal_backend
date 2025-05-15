import requests
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

FORENSICS_API_URL = "https://api.legalforensics.ai/hybridLegalSearch"

def validar_respuesta(data):
    if "answer" in data and "references" in data:
        return data
    return {"error": "Respuesta no válida de Forensics API."}

@router.get("/api/forensics/search")
def buscar_forensics(pregunta: str = Query(...)):
    payload = {
        "question": pregunta,
        "language": "es",
        "realTimeSearch": True
    }
    try:
        response = requests.post(FORENSICS_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        valid = validar_respuesta(response.json())
        dual = output_dual({
            "respuesta": valid.get("answer", "Sin respuesta"),
            "clasificacion": "Fuerte" if "answer" in valid else "Débil",
            "justificacion": "Respuesta directa del proxy forense.",
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": valid.get("answer", "Sin respuesta"),
            "fuentes": valid.get("references", []),
            "logs": {
                "input": pregunta,
                "output": valid,
            }
        })
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
    except Exception as e:
        dual = output_dual({
            "respuesta": "No se pudo conectar con Legal Forensics.",
            "clasificacion": "Errónea",
            "justificacion": str(e),
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": "Error de conexión",
            "fuentes": [],
            "logs": {
                "input": pregunta,
                "output": str(e),
            }
        })
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
