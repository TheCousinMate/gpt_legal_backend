from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils_output import output_dual

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
    payload = await request.json()
    user_input = payload.get("input", "")
    resultado = {
        "respuesta": f"Entrada procesada: {user_input}",
        "clasificacion": "Fuerte",
        "justificacion": "El endpoint predict fue alcanzado exitosamente.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": user_input,
        "fuentes": [],
        "logs": {
            "input": user_input,
            "output": "Respuesta generada correctamente"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
