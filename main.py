from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from modules import reflexion, vision_forense, prediccion_bayesiana, legislacion_bcn

# Inicialización básica de la app
app = FastAPI(
    title="Global AI Legal & Forensic Expert",
    version="1.0.0"
)

# Registro de routers
app.include_router(reflexion.router, prefix="/reflexion")
app.include_router(vision_forense.router, prefix="/vision")
app.include_router(prediccion_bayesiana.router, prefix="/prediccion")
app.include_router(legislacion_bcn.router, prefix="/bcn")

# ✅ Reemplazo del OpenAPI para incluir manualmente el campo 'servers'
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {
            "url": "https://gpt-legal-backend.onrender.com",
            "description": "Render Production Server"
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
