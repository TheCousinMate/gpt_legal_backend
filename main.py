from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from modules import (
    root,
    reflexion,
    vision_forense,
    prediccion_bayesiana,
    legislacion_bcn,
    bcn_parser
)

app = FastAPI(
    title="Forensic Legal Cognition 4.1",
    description="API chilena de análisis jurídico automatizado, evaluación doctrinal y verificación forense de alta precisión.",
    version="4.1.0",
    contact={
        "name": "Kabir K. Hazbún Crovetto",
        "email": "kharzun@gmail.com",
        "url": "https://github.com/TheCousinMate/gpt_legal_backend"
    },
    terms_of_service="https://github.com/TheCousinMate/gpt_legal_backend#terms",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_url="/static/openapi.yaml"  # Reemplaza la auto-generación por el archivo externo
)

# 📁 Servir carpeta estática
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Endpoint básico
@app.get("/")
def health_check():
    return {"status": "alive", "version": "4.1.0"}

# 🔗 Routers del sistema
app.include_router(root.router)
app.include_router(reflexion.router, prefix="/reflexion")
app.include_router(vision_forense.router, prefix="/vision")
app.include_router(prediccion_bayesiana.router, prefix="/prediccion")
app.include_router(legislacion_bcn.router, prefix="/legislacion")
app.include_router(bcn_parser.router, prefix="/bcn")

# 🔍 Endpoint para acceder al OpenAPI
@app.get("/static/openapi.yaml", include_in_schema=False)
def get_openapi_file():
    filepath = os.path.join("static", "openapi.yaml")
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="text/yaml")
    return {"detail": "File not found"}
