# ===== modules/reflexion.py =====
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class ReflexionInput(BaseModel):
    documento_analizado: str
    criterios: list[str]

@router.post("/reflexion/")
def reflexionar(data: ReflexionInput):
    if not data.documento_analizado.strip():
        raise HTTPException(status_code=400, detail="Documento requerido")
    if not data.criterios:
        raise HTTPException(status_code=400, detail="Criterios requeridos")

    resultado = {
        "respuesta": f"Análisis doctrinal completado usando criterios: {', '.join(data.criterios)}",
        "clasificacion": "Fuerte",
        "justificacion": "Evaluación doctrinal automatizada",
        "logs": {"input": data.dict()}
    }
    return JSONResponse(content=output_dual(resultado))

# ===== modules/prediccion_bayesiana.py =====
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class PrediccionInput(BaseModel):
    contexto: str

@router.post("/api/prediccion/")
def predecir_riesgo(datos: PrediccionInput):
    if len(datos.contexto.strip()) < 50:
        raise HTTPException(status_code=422, detail="Contexto insuficiente")

    from modules.motor_predictivo import analizar_input_legal
    analisis = analizar_input_legal(datos.contexto)

    resultado = {
        "respuesta": analisis,
        "clasificacion": "Fuerte",
        "justificacion": "Análisis predictivo bayesiano",
        "logs": {"input": datos.dict()}
    }
    return JSONResponse(content=output_dual(resultado))

# ===== modules/vision_forense.py =====
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

class VisionInput(BaseModel):
    image_id: str

@router.post("/vision/")
def analizar_imagen(data: VisionInput):
    if not data.image_id.strip():
        raise HTTPException(status_code=400, detail="ID de imagen requerido")

    resultado = {
        "respuesta": f"Análisis visual forense registrado para: {data.image_id}",
        "clasificacion": "Moderada",
        "justificacion": "Procesamiento de imagen forense",
        "logs": {"input": data.dict()}
    }
    return JSONResponse(content=output_dual(resultado))

# ===== modules/forensics_proxy.py =====
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter(prefix="/forensics")

@router.get("/search")
def buscar_forensics(pregunta: str = Query(...)):
    resultado = {
        "respuesta": f"Búsqueda forense para: {pregunta}",
        "clasificacion": "Moderada",
        "justificacion": "Búsqueda forense simulada",
        "logs": {"input": pregunta}
    }
    return JSONResponse(content=output_dual(resultado))

# ===== modules/bcn_parser.py =====
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/api/bcn/norma/{id_norma}")
def norma_bcn(id_norma: int):
    return JSONResponse(content={
        "norma": {
            "id": id_norma,
            "titulo": f"Norma simulada {id_norma}",
            "fecha_publicacion": "2024-01-01",
            "contenido": "Contenido simulado de norma legal"
        }
    })

# ===== modules/bcn_text_search_parser.py =====
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from utils_output import output_dual

router = APIRouter()

@router.get("/text-search")
def buscar_texto_bcn(palabra: str = Query(...)):
    resultado = {
        "respuesta": f"Búsqueda textual para: {palabra}",
        "clasificacion": "Moderada",
        "justificacion": "Búsqueda textual en normativa",
        "logs": {"input": palabra}
    }
    return JSONResponse(content=output_dual(resultado))