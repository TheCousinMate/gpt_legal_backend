# ✅ PARCHE DIRECTO PARA forensics_proxy.py SI /search NO FUNCIONA

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter(prefix="/forensics")

@router.get("/search")
def buscar_forensics(pregunta: str = Query(...)):
    try:
        # Simulación de lógica (puede integrarse llamada real aquí si se desea)
        resultado = {
            "respuesta": f"Simulación de búsqueda jurídica sobre: {pregunta}",
            "clasificacion": "Moderada",
            "justificacion": "Este es un resultado de prueba para confirmar la funcionalidad del endpoint.",
            "logs": {"input": pregunta, "output": "simulado"},
            "fuentes": []
        }
        dual = output_dual(resultado)
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
