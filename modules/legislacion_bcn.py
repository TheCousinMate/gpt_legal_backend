from fastapi import APIRouter
import requests

router = APIRouter()

@router.get("/buscar")
def buscar_norma(palabra: str):
    url = f"https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service?palabra={palabra}"
    response = requests.get(url)
    return {"resultado": response.text}

@router.get("/norma/{id_norma}")
def obtener_norma(id_norma: int):
    url = f"https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service?norma={id_norma}"
    response = requests.get(url)
    return {"norma": response.text}
