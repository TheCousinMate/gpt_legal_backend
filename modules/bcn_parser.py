# modules/bcn_parser.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/bcn/norma/{norma_id}")
def norma_bcn(norma_id: int):
    # Aquí va la lógica simulada
    if norma_id == 1234:
        return {"id": norma_id, "titulo": "Ley Chile - Biblioteca del Congreso Nacional", "fecha_publicacion": "2001-05-21"}
    elif norma_id == 5678:
        return {"id": norma_id, "titulo": "Ley Chile - Biblioteca del Congreso Nacional", "fecha_publicacion": "2010-11-10"}
    return JSONResponse(content={"error": f"No se encontró norma con ID {norma_id}"}, status_code=404)
