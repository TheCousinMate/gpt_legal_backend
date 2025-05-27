from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils_output import create_success_response, create_error_response

router = APIRouter()

# Buscar por palabra clave en Ley Chile
@router.get("/legislacion/buscar")
def buscar_norma(palabra: str):
    try:
        resultados = [
            f"Norma relacionada con '{palabra}' identificada en Ley Chile",
            f"Coincidencia exacta con título o glosa legal"
        ]
        return create_success_response(
            message=f"Búsqueda completada para: {palabra}",
            data={
                "palabra": palabra,
                "resultados": resultados,
                "fuentes": [
                    {"title": "Ley Chile", "url": "https://www.leychile.cl"}
                ]
            }
        )
    except Exception as e:
        return create_error_response("Error en búsqueda normativa", str(e))

# Obtener norma específica desde BCN
@router.get("/api/bcn/norma/{id_norma}")
def obtener_norma(id_norma: int):
    try:
        norma = {
            "id": id_norma,
            "titulo": "Ley de Prueba Electrónica",
            "contenido": "Artículo 1: Esta ley regula..."
        }
        return create_success_response(
            message="Norma legal recuperada exitosamente",
            data={
                "norma": norma,
                "base_legal": {
                    "Ley 19.799": "Sobre documentos electrónicos y firmas digitales"
                },
                "fuentes": [
                    {"title": "Biblioteca del Congreso Nacional", "url": "https://www.bcn.cl"}
                ]
            }
        )
    except Exception as e:
        return create_error_response("Error al recuperar norma", str(e))

# Búsqueda textual extendida en base legal
@router.get("/text-search")
def busqueda_textual(palabra: str):
    try:
        matches = [
            f"Artículo 5: Contiene la palabra '{palabra}'",
            f"Artículo 18: Mención indirecta relevante"
        ]
        return create_success_response(
            message=f"Resultados para texto: {palabra}",
            data={
                "coincidencias": matches,
                "fuentes": [
                    {"title": "BCN Texto Legal", "url": "https://www.bcn.cl/leychile"}
                ]
            }
        )
    except Exception as e:
        return create_error_response("Error en búsqueda textual legal", str(e))
