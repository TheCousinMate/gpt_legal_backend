from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/text-search")
def buscar_texto_bcn(palabra: str = Query(..., description="Término a buscar en el texto legal")):
    # Simulación de búsqueda textual
    resultados = [
        {"norma_id": 12345, "extracto": f"Resultado relacionado con '{palabra}'."},
        {"norma_id": 67890, "extracto": f"Otro resultado con el término '{palabra}'."}
    ]
    return JSONResponse(content={"palabra": palabra, "resultados": resultados})
