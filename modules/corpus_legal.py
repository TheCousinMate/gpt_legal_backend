from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from modules.bcn_text_search_parser import buscar_texto_en_leyes
from utils_output import output_dual

router = APIRouter()

@router.post("/corpus-legal")
async def corpus_legal(request: Request):
    try:
        payload = await request.json()
        texto = payload.get("texto") or payload.get("input")
        if not texto:
            raise ValueError("Falta el campo obligatorio 'texto' o 'input'.")
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error al leer input: {str(e)}"})

    resultado = buscar_texto_en_leyes(texto)

    estructura = {
        "respuesta": resultado,
        "clasificacion": "Consulta corpus legal chileno",
        "justificacion": "Se aplicó búsqueda textual sobre leyes.",
        "base_legal": resultado,
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": resultado,
        "fuentes": [],
        "logs": {
            "input": texto,
            "output": "Consulta realizada"
        }
    }
    dual = output_dual(estructura)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
