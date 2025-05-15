import json

def output_dual(data: dict):
    # Output JSON estructurado
    output_json = json.dumps(data, ensure_ascii=False, indent=2)
    # Output Markdown amigable para humanos
    output_md = f"""
### Respuesta directa
{data.get('respuesta', '')}

**Clasificación:** {data.get('clasificacion', '')}  
**Justificación:** {data.get('justificacion', '')}  

**Base legal:**  
{data.get('base_legal', '')}  

**Derecho comparado:**  
{data.get('derecho_comparado', '')}  

**Contradicciones:**  
{data.get('contradicciones', '')}  

**Estándares internacionales:**  
{data.get('estandares_internacionales', '')}  

**Esquema visual:**  
{data.get('esquema_visual', '')}  

**Síntesis para audio:**  
{data.get('sintesis_audio', '')}  

**Fuentes:**  
{data.get('fuentes', '')}  

---
**Logs internos:**  
{data.get('logs', '')}
"""
    return {"json": output_json, "markdown": output_md}
