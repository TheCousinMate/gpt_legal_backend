
from fastapi import FastAPI
from modules import reflexion, vision_forense, prediccion_bayesiana, legislacion_bcn

app = FastAPI(
    title="Global AI Legal & Forensic Expert",
    version="1.0.0",
    servers=[
        {"url": "https://gpt-legal-backend.onrender.com", "description": "Render Production Server"}
    ]
)

@app.get("/")
def root():
    return {"message": "Forensic Legal Backend is running."}

# Registro de routers
app.include_router(reflexion.router, prefix="/reflexion")
app.include_router(vision_forense.router, prefix="/vision")
app.include_router(prediccion_bayesiana.router, prefix="/prediccion")
app.include_router(legislacion_bcn.router, prefix="/bcn")
