from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from modules.bcn_parser import obtener_leyes_chilenas
from utils_output import output_dual

router = APIRouter()

@router.post("/legislacion-bcn")
async def legislacion_bcn(request: Request):
    try:
        payload = await request.json()
        termino = payload.get("termino") or payload.get("texto") or payload.get("input")
        if not termino:
            raise ValueError("Falta el campo obligatorio 'termino'.")
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error en JSON recibido: {str(e)}"})

    resultado_bcn = obtener_leyes_chilenas(termino)

    resultado = {
        "respuesta": resultado_bcn,
        "clasificacion": "Legislación chilena",
        "justificacion": "Búsqueda realizada en la base del BCN.",
        "base_legal": resultado_bcn,
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": resultado_bcn,
        "fuentes": ["https://www.bcn.cl/"],
        "logs": {
            "input": termino,
            "output": "Consulta legislativa realizada"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
