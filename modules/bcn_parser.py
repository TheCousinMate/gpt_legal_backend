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

        resultado = {
            "respuesta": f"Título: {titulo_text}",
            "clasificacion": "Fuerte",
            "justificacion": "Consulta directa a BCN.",
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": titulo_text,
            "fuentes": [url],
            "logs": {
                "input": id_norma,
                "output": {"titulo": titulo_text, "resumen": resumen_text}
            }
        }
        dual = output_dual(resultado)
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
    except Exception as e:
        dual = output_dual({
            "respuesta": "No se pudo obtener la norma BCN.",
            "clasificacion": "Errónea",
            "justificacion": str(e),
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": "Error.",
            "fuentes": [],
            "logs": {
                "input": id_norma,
                "output": str(e)
            }
        })
        return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
