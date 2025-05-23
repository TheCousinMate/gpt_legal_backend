import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

@router.get("/api/bcn/norma/{id_norma}")
def norma_bcn(id_norma: int):
    try:
        url = f"https://www.bcn.cl/leychile/Navegar?idNorma={id_norma}"
        headers = {"User-Agent": "ForensicLegalBot/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        titulo_tag = soup.find("h1") or soup.find("title")
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título no disponible"

        fecha_tag = soup.find(class_="fecha-publicacion")
        fecha = fecha_tag.get_text(strip=True) if fecha_tag else "Fecha no disponible"

        resumen_tag = soup.find("div", class_="resumen")
        if resumen_tag:
            resumen = resumen_tag.get_text(strip=True)
        else:
            primer_p = soup.find("p")
            resumen = primer_p.get_text(strip=True) if primer_p else "Resumen no disponible"

        resultado = {
            "norma": {
                "id": id_norma,
                "titulo": titulo,
                "fecha_publicacion": fecha,
                "contenido": resumen
            }
        }
        return JSONResponse(content=resultado)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": "No se pudo extraer la norma desde BCN.",
            "detalle": str(e)
        })
