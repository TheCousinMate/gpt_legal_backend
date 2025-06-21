from fastapi import APIRouter, Request
from datetime import datetime

router = APIRouter()

@router.get("/status")
@router.get("/status/json")
async def estado_backend(request: Request):
    timestamp = datetime.utcnow().isoformat()
    return {
        "json": {
            "respuesta": "El backend está operativo y responde en JSON y Markdown.",
            "clasificacion": "Fuerte",
            "justificacion": "Sistema activo.",
            "base_legal": {},
            "derecho_comparado": {},
            "contradicciones": [],
            "estandares_internacionales": [],
            "esquema_visual": "",
            "sintesis_audio": "Sistema activo.",
            "fuentes": [],
            "logs": {
                "input": None,
                "output": "ok"
            },
            "timestamp": timestamp,
            "version": "4.1.0"
        },
        "markdown": f"""# 📋 Análisis Jurídico Automatizado

## 🎯 Respuesta Principal
El backend está operativo y responde en JSON y Markdown.

---

## 📊 Clasificación del Caso
**Nivel:** Fuerte  
**Justificación:** Sistema activo.

---

## ⚖️ Marco Legal Aplicable
*No se identificó marco legal específico.*

---

## 🌍 Derecho Comparado
*No se aplicó análisis de derecho comparado.*

---

## ⚠️ Contradicciones Detectadas
*No se detectaron contradicciones normativas.*

---

## 🏛️ Estándares Internacionales
*No se aplicaron estándares internacionales.*

---

## 📈 Esquema Visual
No disponible

---

## 🎵 Síntesis para Audio
Sistema activo.

---

## 📚 Fuentes Consultadas
*No se registraron fuentes específicas.*

---

## 🔍 Información Técnica
**Timestamp:** {timestamp}  
**Versión:** 4.1.0  
**Logs:** ```json
{{ "input": null, "output": "ok" }}
```"""
    }
