from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

@router.get("/text-search")
def buscar_texto_bcn(palabra: str = Query(..., description="Término a buscar en el texto legal")):
    resultados = [
        {"norma_id": 12345, "extracto": f"Resultado relacionado con '{palabra}'."},
        {"norma_id": 67890, "extracto": f"Otro resultado con el término '{palabra}'."}
    ]
    resultado = {
        "respuesta": f"Resultados simulados de búsqueda para '{palabra}'.",
        "clasificacion": "Moderada",
        "justificacion": "Búsqueda textual simulada en normativa.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": f"Búsqueda para {palabra}",
        "fuentes": [],
        "logs": {
            "input": palabra,
            "output": resultados
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
