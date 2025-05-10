from fastapi import FastAPI
from modules import reflexion, vision_forense, prediccion_bayesiana, legislacion_bcn

app = FastAPI(title="Global AI Legal & Forensic Expert", version="1.0.0")

# Registrar rutas de módulos
app.include_router(reflexion.router, prefix="/reflexion")
app.include_router(vision_forense.router, prefix="/vision")
app.include_router(prediccion_bayesiana.router, prefix="/prediccion")
app.include_router(legislacion_bcn.router, prefix="/bcn")
