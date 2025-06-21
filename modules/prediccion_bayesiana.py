from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from modules.motor_predictivo import prediccion_bayesiana
from utils_output import output_dual

router = APIRouter()

@router.post("/predict/bayes")
async def predict_bayes(request: Request):
    try:
        payload = await request.json()
        texto = payload.get("texto") or payload.get("input")
        if not texto:
            raise ValueError("Falta el campo obligatorio 'texto' o 'input'.")
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error al leer JSON: {str(e)}"})

    resultado_modelo = prediccion_bayesiana(texto)

    resultado = {
        "respuesta": resultado_modelo,
        "clasificacion": "Predicción Bayesiana",
        "justificacion": "Modelo probabilístico ejecutado correctamente.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": resultado_modelo,
        "fuentes": [],
        "logs": {
            "input": texto,
            "output": "Predicción generada"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
