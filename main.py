from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import uvicorn

# Importar routers
from modules.reflexion import router as reflexion_router
from modules.prediccion_bayesiana import router as prediccion_router
from modules.vision_forense import router as vision_router
from modules.legislacion_bcn import router as legislacion_router
from modules.forensics_proxy import router as forensics_router
from modules.bcn_parser import router as bcn_router
from modules.bcn_text_search_parser import router as text_search_router
from modules.predict import router as predict_router
from modules.interprete import interpretar_input
from pydantic import BaseModel

app = FastAPI(
    title="Forensic Legal Cognition 4.1",
    description="API chilena de análisis jurídico automatizado, evaluación doctrinal y verificación forense de alta precisión.",
    version="4.1.0",
    contact={
        "name": "Kabir K. Hazbún Crovetto",
        "email": "khazbun@gmail.com",
        "url": "https://github.com/TheCousinMate/gpt_legal_backend"
    },
    license_info={
        "name": "SafeCreative",
        "url": "https://www.safecreative.org/work/2405266632445"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reflexion_router)
app.include_router(prediccion_router)
app.include_router(vision_router)
app.include_router(legislacion_router)
app.include_router(forensics_router)
app.include_router(bcn_router)
app.include_router(text_search_router)
app.include_router(predict_router)

class InterpretarInput(BaseModel):
    mensaje: str

@app.post("/interpretar/")
def interpretar(data: InterpretarInput):
    return interpretar_input(data.mensaje)

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
@app.head("/")
def health_check():
    return {
        "status": "alive",
        "version": app.version,
        "title": app.title,
        "endpoints": [route.path for route in app.routes if route.path != "/openapi.json"]
    }

@app.get("/status/json")
def status_json():
    return {
        "status": "operational",
        "version": app.version,
        "title": app.title,
        "description": app.description,
        "total_endpoints": len(app.routes)
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detail": str(exc),
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)