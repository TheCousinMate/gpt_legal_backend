from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from modules.reflexion import router as reflexion_router
from modules.prediccion_bayesiana import router as prediccion_router
from modules.motor_predictivo import router as motor_router
from modules.vision_forense import router as vision_router
from modules.legislacion_bcn import router as legislacion_router
from modules.root import router as root_router

app = FastAPI(
    title="Forensic Legal Cognition 4.1",
    description="API chilena de análisis jurídico automatizado, evaluación doctrinal y verificación forense de alta precisión.",
    version="4.1.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de routers
app.include_router(reflexion_router)
app.include_router(prediccion_router)
app.include_router(motor_router)
app.include_router(vision_router)
app.include_router(legislacion_router)
app.include_router(root_router)

# Health Check para GET y HEAD
@app.get("/")
@app.head("/")
def health_check(request: Request):
    return {"status": "alive", "version": app.version}
