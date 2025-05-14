from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()

class PrediccionInput(BaseModel):
    contexto: str

@router.post("/api/prediccion/")
def predecir_riesgo(datos: PrediccionInput):
    # TODO: Integrar modelo bayesiano real
    contexto = datos.contexto
    resultado = {
        "riesgo_probable": "ALTO",
        "motivacion_detectada": "Posible implicancia directa",
        "contexto": contexto
    }
    return JSONResponse(content=resultado)