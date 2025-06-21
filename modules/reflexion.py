from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils_output import output_dual
from modules.interprete import generar_reflexion_juridica

router = APIRouter()

@router.post("/reflexion")
async def reflexion(request: Request):
    try:
        payload = await request.json()
        texto = payload.get("texto") or payload.get("input")
        if not texto:
            raise ValueError("Falta el campo obligatorio 'texto' o 'input'.")
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error al procesar JSON: {str(e)}"})

    reflexion_generada = generar_reflexion_juridica(texto)

    resultado = {
        "respuesta": reflexion_generada,
        "clasificacion": "Reflexión avanzada",
        "justificacion": "Reflexión jurídica generada correctamente.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": reflexion_generada,
        "fuentes": [],
        "logs": {
            "input": texto,
            "output": "Reflexión generada correctamente"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
