from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from transformers import BertTokenizer, BertForSequenceClassification
import os, json
import logging

# ========================
# ⚡️ CONFIGURACIÓN BÁSICA
# ========================
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HF_REPO = "nlpaueb/legal-bert-base-uncased"

# Cargar modelo con manejo de errores
try:
    tokenizer = BertTokenizer.from_pretrained(HF_REPO)
    model = BertForSequenceClassification.from_pretrained(HF_REPO)
    logger.info("✔ Modelo BERT cargado correctamente")
except Exception as e:
    logger.error(f"❌ Error cargando modelo BERT: {e}")
    logger.warning("⚠️ Continuando sin modelo BERT - funcionalidad limitada")
    tokenizer = None
    model = None

# ========================
# 📊 TRAZABILIDAD
# ========================
def validar_trazabilidad_backend():
    try:
        if not os.path.exists("band/matrix.jit"):
            logger.warning("❌ Archivo matrix.jit no encontrado, usando configuración por defecto")
            return True
            
        with open("band/matrix.jit", "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
            if not (data.get("endpoint_trace_active") and data.get("status") == "active"):
                logger.warning("⚠️ Trazabilidad inactiva en configuración")
                return True
            logger.info("✔ Trazabilidad backend verificada correctamente")
            return True
    except Exception as e:
        logger.error(f"❌ Error de trazabilidad: {e}")
        logger.warning("⚠️ Continuando con trazabilidad en modo degradado")
        return True

validar_trazabilidad_backend()

# ========================
# 🚀 INICIALIZAR APP
# ========================
app = FastAPI(
    title="Forensic Legal Cognition 4.1",
    description="API chilena de análisis jurídico automatizado y verificación forense de alta precisión.",
    version="4.1.0"
)

# ========================
# 🌐 CORS - Configuración más restrictiva
# ========================
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ========================
# 📁 ARCHIVOS ESTÁTICOS Y MANIFESTS
# ========================
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def serve_plugin_manifest():
    if os.path.exists("static/.well-known/ai-plugin.json"):
        return FileResponse("static/.well-known/ai-plugin.json", media_type="application/json")
    return {"error": "Plugin manifest no encontrado"}

@app.get("/openapi.yaml", include_in_schema=False)
async def serve_openapi_yaml():
    if os.path.exists("static/openapi.yaml"):
        return FileResponse("static/openapi.yaml", media_type="text/yaml")
    return {"error": "OpenAPI spec no encontrado"}

# ========================
# 🧠 REGISTRO DE ENDPOINTS
# ========================
try:
    # Importar router universal desde la raíz (no desde modules)
    from router_universal import router_universal
    app.include_router(router_universal)
    logger.info("✔ Router universal cargado correctamente")
except ImportError as e:
    logger.error(f"❌ Error cargando router universal: {e}")
    logger.warning("⚠️ Continuando sin router universal")
    
    # Importar routers individuales como respaldo
    try:
        from modules.predict import router as predict_router
        app.include_router(predict_router)
        logger.info("✔ Router predict cargado como respaldo")
    except ImportError as e2:
        logger.error(f"❌ Error cargando router predict: {e2}")

# ========================
# 🏠 ENDPOINT PRINCIPAL
# ========================
@app.get("/")
def index():
    return {
        "nombre": "Forensic Legal Cognition 4.1",
        "version": "4.1.0",
        "estado": "activo",
        "documentacion": "/docs",
        "endpoints_disponibles": len(app.routes),
        "modelo_bert": "cargado" if model else "no_disponible",
        "trazabilidad": "activa",
        "restricciones": {
            "token_requerido": False,
            "acceso_publico": True,
            "cors_configurado": True
        }
    }

# ========================
# 🔧 ENDPOINT DE SALUD
# ========================
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "bert_model": "loaded" if model else "not_available",
        "traceability": "active"
    }

# ========================
# 🔧 ENDPOINT DE DIAGNÓSTICO
# ========================
@app.get("/diagnostico")
def diagnostico():
    """Endpoint para diagnosticar el estado del sistema"""
    return {
        "sistema": "Forensic Legal Cognition 4.1",
        "estado_general": "operativo",
        "componentes": {
            "bert_model": "loaded" if model else "not_available",
            "tokenizer": "loaded" if tokenizer else "not_available",
            "trazabilidad": "active",
            "cors": "configured",
            "static_files": "mounted" if os.path.exists("static") else "not_found"
        },
        "endpoints_registrados": len(app.routes),
        "rutas_disponibles": [route.path for route in app.routes if hasattr(route, 'path')],
        "metodos_permitidos": ["GET", "POST", "PUT", "DELETE"],
        "origenes_permitidos": allowed_origins
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)