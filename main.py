from fastapi import FastAPI
from modules import root, reflexion, vision_forense, prediccion_bayesiana

app = FastAPI(
    title="GPT Legal Backend",
    description="API for Resolver IA - Legal & Forensic Cognition 4.1",
    version="4.1.0"
)

# Endpoint raíz simple
@app.get("/")
def health_check():
    return {"status": "alive", "version": "4.1.0"}

# Montar módulos individuales si definen routers
app.include_router(root.router)
app.include_router(reflexion.router)
app.include_router(vision_forense.router)
app.include_router(prediccion_bayesiana.router)
