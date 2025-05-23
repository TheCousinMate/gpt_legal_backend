# ✅ BCN Parser actualizado: extracción más robusta desde leychile

import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

@router.get("/bcn/api/bcn/norma/{id_norma}")
def obtener_norma_bcn(id_norma: int):
    try:
        url = f"https://www.bcn.cl/leychile/Navegar?idNorma={id_norma}"
        headers = {"User-Agent": "ResolverIA/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Intentar obtener el titulo desde <h1> o <title>
        titulo_tag = soup.find("h1") or soup.find("title")
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título no disponible"

        # Buscar contenido relevante en resumen o párrafos
        resumen_tag = soup.find("div", class_="resumen")
        if resumen_tag:
            contenido = resumen_tag.get_text(strip=True)
        else:
            parrafos = soup.find_all("p")
            contenido = parrafos[0].get_text(strip=True) if parrafos else "Resumen no disponible"

        # Si todo está vacío, fallback: intentar desde iframe export
        if titulo == "Título no disponible" and contenido == "Resumen no disponible":
            export_url = f"https://www.bcn.cl/leychile/export?idNorma={id_norma}"
            export_resp = requests.get(export_url, headers=headers, timeout=10)
            export_resp.raise_for_status()
            export_soup = BeautifulSoup(export_resp.text, "html.parser")
            texto_completo = export_soup.get_text(" ", strip=True)
            contenido = texto_completo[:500] + "..." if texto_completo else contenido

        resultado = {
            "norma": {
                "id": id_norma,
                "titulo": titulo,
                "contenido": contenido
            }
        }
        return JSONResponse(content=resultado)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Fallo al obtener norma BCN",
                "id": id_norma,
                "detalle": str(e)
            }
        )
