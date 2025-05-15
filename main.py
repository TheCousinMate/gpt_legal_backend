from fastapi import FastAPI
from modules.reflexion import router as reflexion_router
from modules.vision_forense import router as vision_router
from modules.prediccion_bayesiana import router as prediccion_router
from modules.bcn_parser import router as bcn_router
from modules.legislacion_bcn import router as legislacion_router
from modules.bcn_text_search_parser import router as text_search_router
from modules.forensics_proxy import router as forensics_router
from modules.root import router as root_router

app = FastAPI(title="GPT Legal Forensic API", version="1.0")

# Ruta raíz para respuesta básica
@app.get("/", tags=["Raíz"])
async def read_root():
    return {"message": "Backend GPT Legal Forensic funcionando correctamente"}

# Inclusión de rutas organizadas
app.include_router(reflexion_router, prefix="/reflexion", tags=["Reflexión"])
app.include_router(vision_router, prefix="/vision", tags=["Visión Forense"])
app.include_router(prediccion_router, prefix="/prediccion", tags=["Predicción Bayesiana"])
app.include_router(bcn_router, prefix="/bcn", tags=["BCN Parser"])
app.include_router(legislacion_router, prefix="/legislacion", tags=["Legislación BCN"])
app.include_router(text_search_router, prefix="/bcn", tags=["BCN Text Search"])
app.include_router(forensics_router, prefix="/forensics", tags=["Forensics GAFI"])
app.include_router(root_router, prefix="/status", tags=["Estado del Sistema"])
