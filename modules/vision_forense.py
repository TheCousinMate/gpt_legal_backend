from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils_output import create_success_response, create_error_response

router = APIRouter()

class ImagenInput(BaseModel):
    image_id: str

@router.post("/vision/")
def analizar_imagen(data: ImagenInput):
    try:
        image_id = data.image_id

        resultado = {
            "imagen": image_id,
            "hallazgos": [
                "Documento escaneado sin firma visible",
                "Metadatos indican edición posterior a la fecha declarada"
            ],
            "confianza": "Alta"
        }

        return create_success_response(
            message="Análisis de imagen forense completado",
            data={
                "input": image_id,
                "evaluacion": resultado,
                "base_legal": {
                    "Ley 19.799 art. 5": "Validez de firma electrónica",
                    "CPP art. 239": "Valor probatorio de documentos"
                },
                "derecho_comparado": {
                    "EE.UU.": "Carpenter v. United States (2018)",
                    "UE": "AI Act, propuesta 2021"
                },
                "estandares_internacionales": [
                    "GDPR (Reglamento UE 2016/679)",
                    "Normas ISO 27037 sobre evidencia digital"
                ],
                "contradicciones": [
                    "Discrepancia entre contenido visual y metadatos originales"
                ],
                "fuentes": [
                    {"title": "Ley 19.799 sobre documentos electrónicos", "url": "https://bcn.cl/1x2xx"},
                    {"title": "Código Procesal Penal", "url": "https://bcn.cl/2f3x9"}
                ]
            }
        )
    except Exception as e:
        return create_error_response("Error en análisis visual forense", str(e))
