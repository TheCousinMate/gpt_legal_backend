from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/")
async def analizarOCR(file: UploadFile = File(...)):
    # Lógica OCR aquí
    contenido = await file.read()
    return {"textoExtraido": f"Texto extraído (simulado): {len(contenido)} bytes procesados"}
