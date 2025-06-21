from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from modules.motor_predictivo import analizar_input_legal
from utils_output import output_dual

router = APIRouter()

@router.post("/predict")
async def predict(request: Request):
    try:
        payload = await request.json()
        texto = payload.get("texto") or payload.get("input")
        if not texto:
            raise ValueError("Falta el campo obligatorio 'texto' o 'input'.")
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error al procesar JSON: {str(e)}"})

    respuesta_generada = analizar_input_legal(texto)

    resultado = {
        "respuesta": respuesta_generada,
        "clasificacion": "Fuerte",
        "justificacion": "El endpoint predict fue alcanzado exitosamente.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": respuesta_generada,
        "fuentes": [],
        "logs": {
            "input": texto,
            "output": "Respuesta generada correctamente"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
