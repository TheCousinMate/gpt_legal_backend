# modules/bcn_parser.py

import requests
from bs4 import BeautifulSoup

def obtener_leyes_chilenas(busqueda: str) -> list:
    """
    Realiza scraping simple en la BCN para buscar leyes relacionadas a un término.
    """
    url = f"https://www.bcn.cl/leychile/busqueda?query={busqueda}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError("No se pudo acceder a la BCN.")

    soup = BeautifulSoup(response.text, "html.parser")
    resultados = []

    for item in soup.select("div.resultado"):
        titulo = item.select_one("h3")
        link = item.select_one("a[href]")

        if titulo and link:
            resultados.append({
                "titulo": titulo.text.strip(),
                "url": link["href"]
            })

    if not resultados:
        return [{"mensaje": "No se encontraron leyes asociadas a esta búsqueda."}]
    
    return resultados
