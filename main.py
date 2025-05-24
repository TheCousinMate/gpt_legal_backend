from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

load_dotenv()

from modules import (
    root,
    reflexion,
    vision_forense,
    prediccion_bayesiana,
    legislacion_bcn,
    bcn_parser,
    forensics_proxy
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
    openapi_url="/static/openapi.json"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def health_check():
    return {"status": "alive", "version": app.version}

app.include_router(root.router)
app.include_router(reflexion.router)
app.include_router(vision_forense.router)
app.include_router(prediccion_bayesiana.router)
app.include_router(legislacion_bcn.router)
app.include_router(bcn_parser.router)
app.include_router(forensics_proxy.router)

@app.get("/static/openapi.json", include_in_schema=False)
def get_openapi_file():
    filepath = os.path.join("static", "openapi.json")
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="application/json")
    return {"detail": "openapi.json not found"}
