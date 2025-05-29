from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io

router = APIRouter()

@router.post("/vision")
async def analizar_imagen(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Debe subir una imagen.")

    try:
        contenido = await file.read()
        imagen = Image.open(io.BytesIO(contenido))
        texto_extraido = pytesseract.image_to_string(imagen, lang="spa")

        if not texto_extraido.strip():
            raise HTTPException(status_code=422, detail="No se detectó texto legible en la imagen.")

        return {
            "texto_extraido": texto_extraido.strip(),
            "estatus": "OCR completado",
            "formato": file.content_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando imagen: {str(e)}")