from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import uvicorn
import os
import yaml

# Routers
from modules.reflexion import router as reflexion_router
from modules.predict import router as predict_router
from modules.vision_forense import router as vision_router
from modules.legislacion_bcn import router as legislacion_router
from modules.forensics_proxy import router as forensics_router
from modules.bcn_parser import router as bcn_router
from modules.interprete import interpretar_input

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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(reflexion_router)
app.include_router(predict_router)
app.include_router(vision_router)
app.include_router(legislacion_router)
app.include_router(forensics_router)
app.include_router(bcn_router)

# Input interpretación
class InterpretarInput(BaseModel):
    mensaje: str

@app.post("/interpretar/")
def interpretar(data: InterpretarInput):
    return interpretar_input(data.mensaje)

# Health check
@app.get("/")
@app.head("/")
def health_check():
    return {
        "status": "alive",
        "version": app.version,
        "title": app.title,
        "endpoints": [route.path for route in app.routes if route.path != "/openapi.json"]
    }

# Estado API
@app.get("/status/json")
def status_json():
    return {
        "status": "operational",
        "version": app.version,
        "title": app.title,
        "description": app.description,
        "total_endpoints": len(app.routes)
    }

# YAML endpoint
@app.get("/openapi.yaml", include_in_schema=False)
def serve_openapi_yaml():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    yaml_data = yaml.dump(openapi_schema, allow_unicode=True)
    return Response(content=yaml_data, media_type="application/x-yaml")

# Verificación
@app.get("/verify-openapi", include_in_schema=False)
def verify_openapi():
    try:
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        return {"status": "ok", "endpoints": list(openapi_schema["paths"].keys())}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Excepciones globales
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

# Ejecutar
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
