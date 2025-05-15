
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

# Importa routers desde tu carpeta modules
from modules.reflexion import router as reflexion_router
from modules.vision_forense import router as vision_router
from modules.prediccion_bayesiana import router as prediccion_router
from modules.bcn_parser import router as bcn_router
from modules.legislacion_bcn import router as legislacion_router
from modules.bcn_text_search_parser import router as text_search_router
from modules.forensics_proxy import router as forensics_router
from modules.root import router as root_router

# Instancia principal de FastAPI
app = FastAPI(
    title="GPT Legal Forensic API",
    version="1.0",
    description="API para análisis legal automatizado con módulos: reflexión, visión, predicción bayesiana y BCN."
)

# Middleware CORS para uso desde frontend o GPTs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta directa para exportar el OpenAPI YAML
@app.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    file_path = Path(__file__).resolve().parent / "openapi.yaml"
    return FileResponse(path=file_path, media_type="application/yaml")

# Ruta raíz para estado del sistema
@app.get("/", tags=["Raíz"])
async def read_root():
    return {"message": "Backend GPT Legal Forensic funcionando correctamente"}

# Registro modular de rutas
app.include_router(reflexion_router, prefix="/reflexion", tags=["Reflexión"])
app.include_router(vision_router, prefix="/vision", tags=["Visión Forense"])
app.include_router(prediccion_router, prefix="/prediccion", tags=["Predicción Bayesiana"])
app.include_router(bcn_router, prefix="/bcn", tags=["BCN Parser"])
app.include_router(legislacion_router, prefix="/legislacion", tags=["Legislación BCN"])
app.include_router(text_search_router, prefix="/bcn", tags=["BCN Text Search"])
app.include_router(forensics_router, prefix="/forensics", tags=["Forensics GAFI"])
app.include_router(root_router, prefix="/status", tags=["Estado del Sistema"])
