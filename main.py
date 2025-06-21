from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from transformers import BertTokenizer, BertForSequenceClassification
import os, json

# ========================
# ⚡️ CONFIGURACIÓN BÁSICA
# ========================
load_dotenv()
HF_REPO = "nlpaueb/legal-bert-base-uncased"

tokenizer = BertTokenizer.from_pretrained(HF_REPO)
model = BertForSequenceClassification.from_pretrained(HF_REPO)

# ========================
# 📊 TRAZABILIDAD
# ========================
def validar_trazabilidad_backend():
    try:
        with open("band/matrix.jit", "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
            if not (data.get("endpoint_trace_active") and data.get("status") == "active"):
                raise Exception("Trazabilidad inactiva.")
            print("✔ Trazabilidad backend verificada correctamente.")
    except Exception as e:
        print(f"❌ Error de trazabilidad: {e}")
        raise SystemExit("🚫 Abortando inicio por fallo en trazabilidad activa.")

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
# 🌐 CORS
# ========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# 📁 ARCHIVOS ESTÁTICOS Y MANIFESTS
# ========================
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def serve_plugin_manifest():
    return FileResponse("static/.well-known/ai-plugin.json", media_type="application/json")

@app.get("/openapi.yaml", include_in_schema=False)
async def serve_openapi_yaml():
    return FileResponse("static/openapi.yaml", media_type="text/yaml")

# ========================
# 🧠 REGISTRO DE ENDPOINTS
# ========================
from modules.router_universal import router_universal
app.include_router(router_universal)

@app.get("/")
def index():
    return {
        "nombre": "Forensic Legal Cognition 4.1",
        "version": "4.1.0",
        "estado": "activo",
        "documentacion": "/docs",
        "endpoints_totales": 9,
        "restringido_por_token": False,
        "interpretar_publico": True
    }
