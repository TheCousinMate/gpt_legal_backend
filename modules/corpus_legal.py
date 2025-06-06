from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def obtenerCorpus():
    # Simulación corpus legal
    return {"corpus": ["Ley 1 simulada", "Ley 2 simulada"]}
