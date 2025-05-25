import json
from typing import Dict, Any
from datetime import datetime

def output_dual(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Genera output dual: JSON estructurado y Markdown legible
    """
    
    # Asegurar campos por defecto
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
    
    # Combinar datos con defaults
    complete_data = {**defaults, **data}
    
    # Output JSON estructurado
    output_json = json.dumps(complete_data, ensure_ascii=False, indent=2)
    
    # Output Markdown mejorado
    output_md = f"""# 📋 Análisis Jurídico Automatizado

## 🎯 Respuesta Principal
{complete_data.get('respuesta', 'No disponible')}

---

## 📊 Clasificación del Caso
**Nivel:** {complete_data.get('clasificacion', 'No clasificado')}  
**Justificación:** {complete_data.get('justificacion', 'Sin justificación')}

---

## ⚖️ Marco Legal Aplicable
{format_legal_framework(complete_data.get('base_legal', {}))}

---

## 🌍 Derecho Comparado
{format_comparative_law(complete_data.get('derecho_comparado', {}))}

---

## ⚠️ Contradicciones Detectadas
{format_contradictions(complete_data.get('contradicciones', []))}

---

## 🏛️ Estándares Internacionales
{format_international_standards(complete_data.get('estandares_internacionales', []))}

---

## 📈 Esquema Visual
{complete_data.get('esquema_visual', 'No disponible')}

---

## 🎵 Síntesis para Audio
{complete_data.get('sintesis_audio', 'No disponible')}

---

## 📚 Fuentes Consultadas
{format_sources(complete_data.get('fuentes', []))}

---

## 🔍 Información Técnica
**Timestamp:** {complete_data.get('timestamp', 'No disponible')}  
**Versión:** {complete_data.get('version', '4.1.0')}  
**Logs:** ```json
{json.dumps(complete_data.get('logs', {}), ensure_ascii=False, indent=2)}
```
"""
    
    return {
        "json": output_json, 
        "markdown": output_md.strip()
    }

def format_legal_framework(base_legal: Dict[str, str]) -> str:
    """Formatea el marco legal en Markdown"""
    if not base_legal:
        return "*No se identificó marco legal específico.*"
    
    formatted = []
    for norm, description in base_legal.items():
        formatted.append(f"- **{norm}:** {description}")
    
    return "\n".join(formatted)

def format_comparative_law(derecho_comparado: Dict[str, str]) -> str:
    """Formatea el derecho comparado en Markdown"""
    if not derecho_comparado:
        return "*No se aplicó análisis de derecho comparado.*"
    
    formatted = []
    for case, description in derecho_comparado.items():
        formatted.append(f"- **{case}:** {description}")
    
    return "\n".join(formatted)

def format_contradictions(contradicciones: list) -> str:
    """Formatea las contradicciones en Markdown"""
    if not contradicciones:
        return "*No se detectaron contradicciones normativas.*"
    
    formatted = []
    for i, contradiccion in enumerate(contradicciones, 1):
        formatted.append(f"{i}. {contradiccion}")
    
    return "\n".join(formatted)

def format_international_standards(estandares: list) -> str:
    """Formatea los estándares internacionales en Markdown"""
    if not estandares:
        return "*No se aplicaron estándares internacionales.*"
    
    formatted = []
    for estandar in estandares:
        formatted.append(f"- {estandar}")
    
    return "\n".join(formatted)

def format_sources(fuentes: list) -> str:
    """Formatea las fuentes en Markdown"""
    if not fuentes:
        return "*No se registraron fuentes específicas.*"
    
    formatted = []
    for i, fuente in enumerate(fuentes, 1):
        if isinstance(fuente, str):
            formatted.append(f"{i}. {fuente}")
        elif isinstance(fuente, dict):
            title = fuente.get('title', 'Fuente sin título')
            url = fuente.get('url', '#')
            formatted.append(f"{i}. [{title}]({url})")
        else:
            formatted.append(f"{i}. {str(fuente)}")
    
    return "\n".join(formatted)

def create_error_response(error_msg: str, details: str = "") -> Dict[str, str]:
    """Crea una respuesta de error formateada"""
    error_data = {
        'respuesta': f"Error: {error_msg}",
        'clasificacion': 'Error',
        'justificacion': details or "Se produjo un error durante el procesamiento",
        'logs': {
            'error': error_msg,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    }
    
    return output_dual(error_data)

def create_success_response(message: str, data: Dict[str, Any] = None) -> Dict[str, str]:
    """Crea una respuesta de éxito formateada"""
    success_data = {
        'respuesta': message,
        'clasificacion': 'Exitoso',
        'justificacion': 'Operación completada correctamente',
        'logs': {
            'status': 'success',
            'data': data or {},
            'timestamp': datetime.now().isoformat()
        }
    }
    
    return output_dual(success_data)