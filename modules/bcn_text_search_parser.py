# modules/bcn_text_search_parser.py

import requests
from bs4 import BeautifulSoup

def buscar_texto_en_leyes(texto: str, max_resultados: int = 10) -> list:
    """
    Realiza una búsqueda de texto dentro de las leyes chilenas usando scraping de la BCN.
    """
    url = f"https://www.bcn.cl/leychile/busqueda_avanzada?query={texto}"
    response = requests.get(url)
    if response.status_code != 200:
        return [{"error": "No se pudo acceder a la BCN."}]

    soup = BeautifulSoup(response.text, "html.parser")
    leyes = []

    for item in soup.select("div.resultado")[:max_resultados]:
        titulo = item.select_one("h3")
        link = item.select_one("a[href]")
        if titulo and link:
            leyes.append({
                "titulo": titulo.text.strip(),
                "url": link["href"]
            })

    return leyes if leyes else [{"mensaje": "No se encontraron coincidencias en las leyes."}]
