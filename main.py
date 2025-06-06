from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de routers
from modules.router_universal import router as universal_router
from modules.reflexion import router as reflexion_router
from modules.vision_forense import router as vision_router
from modules.predict import router as predict_router
from modules.forensics_proxy import router as forensics_router
from modules.legislacion_bcn import router as legislacion_router
from modules.bcn_parser import router as bcn_parser_router
from modules.bcn_text_search_parser import router as text_search_router
from modules.prediccion_bayesiana import router as prediccion_router
from modules.root import router as root_router
from modules.interprete import router as interpretar_router

app = FastAPI(
    title="Forensic Legal Cognition 4.1",
    version="4.1.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de rutas
app.include_router(root_router)
app.include_router(universal_router)
app.include_router(reflexion_router)
app.include_router(vision_router)
app.include_router(predict_router)
app.include_router(forensics_router)
app.include_router(legislacion_router)
app.include_router(bcn_parser_router)
app.include_router(text_search_router)
app.include_router(prediccion_router)
app.include_router(interpretar_router)
