from fastapi import APIRouter, Query, HTTPException
import requests
from bs4 import BeautifulSoup

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
        return {"termino": palabra, "fuente": "BCN", "contenido": contenido}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/norma/{id_norma}")
def obtener_norma(id_norma: int):
    try:
        url = f"https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service?norma={id_norma}"
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error de conexión con BCN.")
        contenido = parse_html_bcn(response.text)
        return {"id_norma": id_norma, "fuente": "BCN", "contenido": contenido}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))