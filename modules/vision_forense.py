from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from modules.forensics_proxy import procesar_imagen_forense
from utils_output import output_dual

router = APIRouter()

@router.post("/vision-forense")
async def vision_forense(file: UploadFile = File(...)):
    try:
        contenido = await file.read()
        resultado_ocr = procesar_imagen_forense(contenido)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Error en procesamiento de imagen: {str(e)}"})

    resultado = {
        "respuesta": resultado_ocr,
        "clasificacion": "OCR y análisis forense",
        "justificacion": "La imagen fue procesada con éxito.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": resultado_ocr,
        "fuentes": [],
        "logs": {
            "input": file.filename,
            "output": "OCR exitoso"
        }
    }
    dual = output_dual(resultado)
    return JSONResponse(content={"json": dual["json"], "markdown": dual["markdown"]})
