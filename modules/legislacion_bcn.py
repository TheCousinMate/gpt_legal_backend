from fastapi import APIRouter, Query, HTTPException
import requests
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

DEFAULT_HEADERS = {"User-Agent": "ForensicLegalBot/1.0"}
DEFAULT_TIMEOUT = 12

def parse_html_bcn(html: str):
    try:
        soup = BeautifulSoup(html, "html.parser")
        titulo = soup.find("h1")
        titulo = titulo.get_text(strip=True) if titulo else "Sin título"
        fecha_tag = soup.find(class_="fecha-publicacion")
        fecha = fecha_tag.get_text(strip=True) if fecha_tag else "Fecha no disponible"
        resumen_tag = soup.find("div", class_="resumen")
        resumen = resumen_tag.get_text(strip=True) if resumen_tag else "Resumen no disponible"
        return {
            "titulo": titulo,
            "fecha_publicacion": fecha,
            "resumen": resumen
        }
    except Exception as e:
        return {"error": f"No se pudo analizar HTML: {e}"}

@router.get("/buscar")
def buscar_norma(palabra: str = Query(..., description="Palabra clave legal a buscar en Ley Chile")):
    try:
        url = f"https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service?palabra={palabra}"
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error de conexión con BCN.")
        contenido = parse_html_bcn(response.text)
        resultado = {
            "respuesta": f"Resultado de búsqueda para '{palabra}' en BCN.",
            "clasificacion": "Fuerte" if contenido else "Débil",
            "justificacion": "Resultado directo desde BCN.",
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": f"Resultado para {palabra}",
            "fuentes": [url],
            "logs": {
                "input": palabra,
                "output": contenido
            }
        }
        dual = output_dual(resultado)
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
    except Exception as e:
        dual = output_dual({
            "respuesta": "Error de conexión con BCN.",
            "clasificacion": "Errónea",
            "justificacion": str(e),
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": "Error de conexión",
            "fuentes": [],
            "logs": {
                "input": palabra,
                "output": str(e),
            }
        })
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})

@router.get("/norma/{id_norma}")
def obtener_norma(id_norma: int):
    try:
        url = f"https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service?norma={id_norma}"
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error de conexión con BCN.")
        contenido = parse_html_bcn(response.text)
        resultado = {
            "respuesta": f"Detalle de la norma BCN ID {id_norma}.",
            "clasificacion": "Fuerte" if contenido else "Débil",
            "justificacion": "Norma consultada directamente en BCN.",
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": f"Norma {id_norma} consultada.",
            "fuentes": [url],
            "logs": {
                "input": id_norma,
                "output": contenido
            }
        }
        dual = output_dual(resultado)
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
    except Exception as e:
        dual = output_dual({
            "respuesta": "Error de conexión con BCN.",
            "clasificacion": "Errónea",
            "justificacion": str(e),
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": "Error de conexión",
            "fuentes": [],
            "logs": {
                "input": id_norma,
                "output": str(e),
            }
        })
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
