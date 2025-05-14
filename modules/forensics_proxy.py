import requests
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

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
        return JSONResponse(content=validar_respuesta(response.json()))
    except Exception as e:
        return JSONResponse(content={"error": f"No se pudo conectar con Legal Forensics: {e}"})