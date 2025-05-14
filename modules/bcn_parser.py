import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/bcn/norma/{id_norma}")
def norma_bcn(id_norma: int):
    try:
        url = f"https://www.bcn.cl/leychile/Navegar?idNorma={id_norma}"
        headers = {"User-Agent": "ForensicLegalBot/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            titulo = soup.find("h1") or soup.find("title")
            titulo_text = titulo.get_text(strip=True) if titulo else "Sin título"
        except Exception:
            titulo_text = "Error al extraer título"

        try:
            resumen = soup.find("div", class_="resumen")
            if resumen:
                resumen_text = resumen.get_text(strip=True)
            else:
                parrafos = soup.find_all("p")
                resumen_text = parrafos[0].get_text(strip=True) if parrafos else "Sin resumen"
        except Exception:
            resumen_text = "Error al extraer resumen"

        return JSONResponse(content={
            "id_norma": id_norma,
            "titulo": titulo_text,
            "resumen": resumen_text,
            "url": url
        })
    except Exception as e:
        return JSONResponse(content={"error": f"No se pudo obtener la norma BCN: {e}"})
