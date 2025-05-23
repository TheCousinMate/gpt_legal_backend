from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils_output import output_dual
from modules.motor_predictivo import analizar_input_legal

router = APIRouter()

@router.get("/status/json")
def status_json():
    resultado = {
        "respuesta": "El backend está operativo y responde en JSON y Markdown.",
        "clasificacion": "Fuerte",
        "justificacion": "Sistema activo.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": "Sistema activo.",
        "fuentes": [],
        "logs": {
            "input": None,
            "output": "ok"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})

@router.post("/predict")
async def predict(request: Request):
    try:
        payload = await request.json()
        user_input = payload.get("input", "")
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error al procesar JSON: {str(e)}"})

    respuesta_generada = analizar_input_legal(user_input)

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
            "input": user_input,
            "output": "Respuesta generada correctamente"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
