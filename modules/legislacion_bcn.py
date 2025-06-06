from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def obtenerBCN():
    # Simulación obtención BCN
    return {"resultados": [{"articulo": "Artículo simulado BCN"}]}
