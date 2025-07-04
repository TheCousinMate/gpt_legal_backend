"""
Utilidades para formateo de salida dual (JSON y Markdown)
"""
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def output_dual(resultado: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte un resultado en formato dual: JSON y Markdown
    
    Args:
        resultado: Diccionario con los datos del resultado
        
    Returns:
        Dict con claves 'json' y 'markdown'
    """
    try:
        # Formatear como JSON limpio
        json_output = {
            "respuesta": resultado.get("respuesta", ""),
            "clasificacion": resultado.get("clasificacion", ""),
            "justificacion": resultado.get("justificacion", ""),
            "base_legal": resultado.get("base_legal", {}),
            "derecho_comparado": resultado.get("derecho_comparado", {}),
            "contradicciones": resultado.get("contradicciones", []),
            "estandares_internacionales": resultado.get("estandares_internacionales", []),
            "esquema_visual": resultado.get("esquema_visual", ""),
            "sintesis_audio": resultado.get("sintesis_audio", ""),
            "fuentes": resultado.get("fuentes", []),
            "logs": resultado.get("logs", {})
        }
        
        # Formatear como Markdown estructurado
        markdown_output = generar_markdown(resultado)
        
        return {
            "json": json_output,
            "markdown": markdown_output
        }
        
    except Exception as e:
        logger.error(f"Error en output_dual: {e}")
        return {
            "json": {"error": f"Error en formateo: {str(e)}"},
            "markdown": f"# Error\n\nError en formateo: {str(e)}"
        }

def generar_markdown(resultado: Dict[str, Any]) -> str:
    """
    Genera formato Markdown estructurado a partir del resultado
    """
    try:
        respuesta = resultado.get("respuesta", "")
        clasificacion = resultado.get("clasificacion", "")
        justificacion = resultado.get("justificacion", "")
        base_legal = resultado.get("base_legal", {})
        derecho_comparado = resultado.get("derecho_comparado", {})
        contradicciones = resultado.get("contradicciones", [])
        estandares = resultado.get("estandares_internacionales", [])
        fuentes = resultado.get("fuentes", [])
        logs = resultado.get("logs", {})
        
        markdown = f"""# 📋 Análisis Legal Automatizado

## 🎯 Respuesta Principal
{respuesta}

## 🏷️ Clasificación
**Nivel:** {clasificacion}

## 💭 Justificación
{justificacion}

"""
        
        # Agregar base legal si existe
        if base_legal:
            markdown += "## ⚖️ Base Legal\n"
            for key, value in base_legal.items():
                markdown += f"- **{key}:** {value}\n"
            markdown += "\n"
        
        # Agregar derecho comparado si existe
        if derecho_comparado:
            markdown += "## 🌐 Derecho Comparado\n"
            for key, value in derecho_comparado.items():
                markdown += f"- **{key}:** {value}\n"
            markdown += "\n"
        
        # Agregar contradicciones si existen
        if contradicciones:
            markdown += "## ⚠️ Contradicciones Detectadas\n"
            for i, contradiccion in enumerate(contradicciones, 1):
                markdown += f"{i}. {contradiccion}\n"
            markdown += "\n"
        
        # Agregar estándares internacionales si existen
        if estandares:
            markdown += "## 🌍 Estándares Internacionales\n"
            for i, estandar in enumerate(estandares, 1):
                markdown += f"{i}. {estandar}\n"
            markdown += "\n"
        
        # Agregar fuentes si existen
        if fuentes:
            markdown += "## 📚 Fuentes Consultadas\n"
            for i, fuente in enumerate(fuentes, 1):
                markdown += f"{i}. {fuente}\n"
            markdown += "\n"
        
        # Agregar logs si existen
        if logs:
            markdown += "## 📝 Información de Procesamiento\n"
            if logs.get("input"):
                markdown += f"- **Input procesado:** {len(str(logs['input']))} caracteres\n"
            if logs.get("output"):
                markdown += f"- **Status:** {logs['output']}\n"
            markdown += "\n"
        
        markdown += "---\n*Generado por Forensic Legal Cognition 4.1*"
        
        return markdown
        
    except Exception as e:
        logger.error(f"Error generando markdown: {e}")
        return f"# Error\n\nError generando formato markdown: {str(e)}"

def formatear_respuesta_simple(texto: str, clasificacion: str = "Análisis") -> Dict[str, Any]:
    """
    Formatea una respuesta simple en el formato estándar
    """
    resultado = {
        "respuesta": texto,
        "clasificacion": clasificacion,
        "justificacion": "Análisis completado exitosamente.",
        "base_legal": {},
        "derecho_comparado": {},
        "contradicciones": [],
        "estandares_internacionales": [],
        "esquema_visual": "",
        "sintesis_audio": texto,
        "fuentes": [],
        "logs": {
            "input": "Texto procesado",
            "output": "Respuesta generada correctamente"
        }
    }
    
    return output_dual(resultado)

def limpiar_texto_respuesta(texto: str) -> str:
    """
    Limpia y normaliza texto de respuesta
    """
    if not texto:
        return ""
    
    # Eliminar espacios excesivos
    texto = " ".join(texto.split())
    
    # Limpiar saltos de línea excesivos
    texto = texto.replace("\n\n\n", "\n\n")
    
    return texto.strip()
