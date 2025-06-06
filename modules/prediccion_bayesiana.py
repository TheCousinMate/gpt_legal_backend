from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import os
import re

router = APIRouter()

# Cargar modelo entrenado
modelo_path = os.path.join("modules", "modelo_bayesiano.joblib")
if not os.path.isfile(modelo_path):
    raise FileNotFoundError(f"Modelo no encontrado en {modelo_path}")
modelo = joblib.load(modelo_path)

# Clase de entrada
class TextoEntrada(BaseModel):
    texto: str

# Preprocesamiento mínimo
stopwords = {"de", "la", "que", "el", "en", "y", "a", "los", "del", "se"}  # puedes ampliar

def limpiar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-zñáéíóú\s]", "", texto)
    palabras = texto.split()
    palabras_filtradas = [p for p in palabras if p not in stopwords]
    return " ".join(palabras_filtradas)

# Ruta del API
@router.post("/prediccion-bayesiana")
def predecir(texto_entrada: TextoEntrada):
    if not texto_entrada.texto.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío.")

    texto_limpio = limpiar_texto(texto_entrada.texto)
    prediccion = modelo.predict([texto_limpio])[0]
    probas = modelo.predict_proba([texto_limpio])[0]
    etiquetas = modelo.classes_

    return {
        "resultado": prediccion,
        "probabilidades": dict(zip(etiquetas, probas))
    }
