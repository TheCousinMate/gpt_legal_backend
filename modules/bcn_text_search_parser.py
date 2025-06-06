# modules/bcn_text_search_parser.py
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/legislacion/buscar")
def buscar_texto(palabra: str = Query(...)):
    if not palabra.strip():
        return {"error": "Palabra clave vacía"}
    return {
        "palabra": palabra,
        "resultados": [],
        "mensaje": "No se encontraron normas relevantes"
    }
