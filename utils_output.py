
import json
from typing import Dict, Any
from datetime import datetime

def output_dual(data: Dict[str, Any]) -> Dict[str, str]:
    defaults = {
        'respuesta': 'Sin respuesta generada',
        'clasificacion': 'No clasificado',
        'justificacion': 'Sin justificación',
        'base_legal': {},
        'derecho_comparado': {},
        'contradicciones': [],
        'estandares_internacionales': [],
        'esquema_visual': '',
        'sintesis_audio': '',
        'fuentes': [],
        'logs': {},
        'timestamp': datetime.now().isoformat(),
        'version': '4.1.0'
    }
    complete_data = {**defaults, **data}
    output_json = json.dumps(complete_data, ensure_ascii=False, indent=2)
    output_md = f"""# 📋 Análisis Jurídico Automatizado

## 🎯 Respuesta Principal
{complete_data['respuesta']}

---

## 📊 Clasificación del Caso
**Nivel:** {complete_data['clasificacion']}  
**Justificación:** {complete_data['justificacion']}

---

## ⚖️ Marco Legal Aplicable
{format_legal_framework(complete_data['base_legal'])}

---

## 🌍 Derecho Comparado
{format_comparative_law(complete_data['derecho_comparado'])}

---

## ⚠️ Contradicciones Detectadas
{format_contradictions(complete_data['contradicciones'])}

---

## 🏛️ Estándares Internacionales
{format_international_standards(complete_data['estandares_internacionales'])}

---

## 📈 Esquema Visual
{complete_data['esquema_visual'] or 'No disponible'}

---

## 🎵 Síntesis para Audio
{complete_data['sintesis_audio'] or 'No disponible'}

---

## 📚 Fuentes Consultadas
{format_sources(complete_data['fuentes'])}

---

## 🔍 Información Técnica
**Timestamp:** {complete_data['timestamp']}  
**Versión:** {complete_data['version']}  
**Logs:** ```json
{json.dumps(complete_data['logs'], ensure_ascii=False, indent=2)}
```"""
    return {"json": output_json, "markdown": output_md.strip()}

def format_legal_framework(base_legal: Dict[str, str]) -> str:
    return "\n".join(f"- **{k}:** {v}" for k, v in base_legal.items()) or "*No se identificó marco legal específico.*"

def format_comparative_law(dc: Dict[str, str]) -> str:
    return "\n".join(f"- **{k}:** {v}" for k, v in dc.items()) or "*No se aplicó análisis de derecho comparado.*"

def format_contradictions(lista: list) -> str:
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(lista)) or "*No se detectaron contradicciones normativas.*"

def format_international_standards(estandares: list) -> str:
    return "\n".join(f"- {s}" for s in estandares) or "*No se aplicaron estándares internacionales.*"

def format_sources(fuentes: list) -> str:
    formatted = []
    for i, fuente in enumerate(fuentes, 1):
        if isinstance(fuente, str):
            formatted.append(f"{i}. {fuente}")
        elif isinstance(fuente, dict):
            formatted.append(f"{i}. [{fuente.get('title', 'Sin título')}]({fuente.get('url', '#')})")
        else:
            formatted.append(f"{i}. {str(fuente)}")
    return "\n".join(formatted) or "*No se registraron fuentes específicas.*"

def create_error_response(msg: str, details: str = "") -> Dict[str, str]:
    return output_dual({
        'respuesta': f"Error: {msg}",
        'clasificacion': 'Error',
        'justificacion': details or "Se produjo un error durante el procesamiento",
        'logs': {'error': msg, 'details': details, 'timestamp': datetime.now().isoformat()}
    })

def create_success_response(message: str, data: Dict[str, Any] = None) -> Dict[str, str]:
    return output_dual({
        'respuesta': message,
        'clasificacion': 'Exitoso',
        'justificacion': 'Operación completada correctamente',
        'logs': {'status': 'success', 'data': data or {}, 'timestamp': datetime.now().isoformat()}
    })
