
from fastapi import FastAPI
from modules import (
    root,
    reflexion,
    vision_forense,
    prediccion_bayesiana,
    legislacion_bcn,
    bcn_parser
)

app = FastAPI(
    title="GPT Legal Backend",
    description="API for Resolver IA - Legal & Forensic Cognition 4.1",
    version="4.1.0",
    contact={
        "name": "Kabir K. Hazbún Crovetto",
        "email": "kharzun@gmail.com",
        "url": "https://github.com/TheCousinMate/gpt_legal_backend"
    }
)

@app.get("/")
def health_check():
    return {"status": "alive", "version": "4.1.0"}

# Montar routers con o sin prefijos según estructura
app.include_router(root.router)
app.include_router(reflexion.router, prefix="/reflexion")
app.include_router(vision_forense.router, prefix="/vision")
app.include_router(prediccion_bayesiana.router)
app.include_router(legislacion_bcn.router, prefix="/legislacion")
app.include_router(bcn_parser.router, prefix="/bcn")

