from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/legislacion/buscar")
def buscar_norma(palabra: str):
    try:
        url = f"https://www.bcn.cl/leychile/search?q={palabra}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        resultados = []
        enlaces = soup.select("h3.resultado-titulo a")

        for e in enlaces[:5]:
            resultados.append({
                "titulo": e.text.strip(),
                "url": e['href']
            })

        if not resultados:
            raise ValueError("No se encontraron normas.")

        return {
            "palabra": palabra,
            "resultados": resultados,
            "fuente": "https://www.bcn.cl/leychile"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en scraping de BCN: {str(e)}")