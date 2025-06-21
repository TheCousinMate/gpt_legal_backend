import re
from typing import Dict

def analizar_input_legal(texto: str) -> str:
    if not texto or len(texto.strip()) == 0:
        return "Texto vacío. Por favor, provea contenido jurídico para análisis."
    
    texto_lower = texto.lower()

    patrones_riesgo = {
        "alto": [
            (r"fraude|estafa|malversación", "Riesgo penal alto - posible delito económico"),
            (r"despido\s+injustificado|término\s+sin\s+causa", "Riesgo laboral alto - despido improcedente"),
            (r"discriminación|acoso\s+sexual|mobbing", "Riesgo laboral alto - vulneración de derechos fundamentales"),
            (r"incumplimiento\s+contractual\s+grave", "Riesgo civil alto - posible resolución de contrato"),
            (r"responsabilidad\s+penal|dolo\s+directo", "Riesgo penal alto - responsabilidad criminal"),
            (r"nulidad\s+absoluta|objeto\s+ilícito", "Riesgo civil alto - nulidad contractual")
        ],
        "moderado": [
            (r"trabajador.*contrato.*informal", "Riesgo laboral moderado - formalización requerida"),
            (r"pago.*sin\s+contrato", "Riesgo fiscal moderado - documentación insuficiente"),
            (r"negligencia|imprudencia\s+grave", "Riesgo civil moderado - responsabilidad extracontractual"),
            (r"falta\s+de\s+competencia|delegación", "Riesgo administrativo moderado - vicio de procedimiento"),
            (r"plazo\s+vencido|prescripción", "Riesgo procesal moderado - pérdida de acción legal"),
            (r"ambigüedad\s+contractual", "Riesgo interpretativo moderado - cláusulas poco claras")
        ],
        "bajo": [
            (r"consulta\s+preventiva", "Riesgo bajo - consulta precautoria"),
            (r"revisión\s+de\s+contrato", "Riesgo bajo - análisis preventivo"),
            (r"asesoría\s+jurídica", "Riesgo bajo - orientación legal"),
            (r"cumplimiento\s+normativo", "Riesgo bajo - verificación de compliance")
        ]
    }

    areas_legales = {
        "laboral": r"trabajador|empleador|sueldo|contrato\s+de\s+trabajo|despido|finiquito|indemnización",
        "civil": r"contrato|responsabilidad\s+civil|daños|perjuicios|incumplimiento|nulidad",
        "penal": r"delito|dolo|culpa|responsabilidad\s+penal|querella|denuncia",
        "administrativo": r"procedimiento\s+administrativo|autoridad|competencia|recurso\s+de\s+protección",
        "tributario": r"impuesto|tributo|sii|evasión\s+tributaria|facturación",
        "comercial": r"empresa|sociedad|comercio|marca|patente|competencia\s+desleal"
    }

    area_detectada = "general"
    for area, patron in areas_legales.items():
        if re.search(patron, texto_lower):
            area_detectada = area
            break

    nivel_riesgo = "bajo"
    explicacion_riesgo = ""

    for nivel, patrones in patrones_riesgo.items():
        for patron, explicacion in patrones:
            if re.search(patron, texto_lower):
                nivel_riesgo = nivel
                explicacion_riesgo = explicacion
                break
        if explicacion_riesgo:
            break

    recomendaciones = generar_recomendaciones(area_detectada, nivel_riesgo)
    analisis_area = get_analisis_area(area_detectada, texto_lower)
    marco = get_marco_legal(area_detectada)

    return f"""
📊 ANÁLISIS LEGAL AUTOMATIZADO

🎯 Área detectada: {area_detectada.upper()}
⚠️ Nivel de riesgo: {nivel_riesgo.upper()}

📋 Evaluación:
{explicacion_riesgo}

🔍 Análisis específico del área {area_detectada}:
{analisis_area}

💡 Recomendaciones:
{recomendaciones}

⚖️ Marco legal aplicable:
{marco}
""".strip()

def generar_recomendaciones(area: str, riesgo: str) -> str:
    recomendaciones_base = {
        "laboral": {
            "alto": "• Consulta urgente con abogado laboralista\n• Documentar comunicaciones\n• Revisar contrato y reglamento interno",
            "moderado": "• Formalizar contrato por escrito\n• Verificar pagos previsionales\n• Establecer protocolos internos",
            "bajo": "• Mantener documentación laboral\n• Revisión anual de contratos\n• Capacitación básica en normativa"
        },
        "civil": {
            "alto": "• Preservar evidencia\n• Evaluar medidas cautelares\n• Consulta legal inmediata",
            "moderado": "• Revisión contractual\n• Negociación extrajudicial\n• Asesoría especializada",
            "bajo": "• Revisión preventiva\n• Clarificar términos\n• Mantener respaldo documental"
        },
        "penal": {
            "alto": "• No declarar sin abogado\n• Preservar evidencia\n• Asesoría penal inmediata",
            "moderado": "• Revisión de protocolos internos\n• Capacitación en compliance\n• Consultoría externa",
            "bajo": "• Auditoría preventiva\n• Programas de cumplimiento\n• Capacitaciones legales"
        }
    }
    return recomendaciones_base.get(area, {}).get(riesgo, "• Consulta con abogado especializado\n• Revisión del caso\n• Análisis de alternativas legales")

def get_analisis_area(area: str, texto: str) -> str:
    analisis = {
        "laboral": "Revisar cumplimiento del Código del Trabajo, derechos fundamentales y obligaciones contractuales.",
        "civil": "Verificar buena fe contractual, obligaciones, daños y vicios del consentimiento.",
        "penal": "Evaluar tipo penal, dolo o culpa, y elementos del delito conforme al Código Penal.",
        "administrativo": "Examinar legitimidad del procedimiento, competencia de la autoridad y posibles vicios formales.",
        "tributario": "Revisar cumplimiento tributario, obligaciones ante el SII y normativa del Código Tributario.",
        "comercial": "Revisar estructuras societarias, actos de comercio y regulación del consumidor.",
    }
    return analisis.get(area, "No se detectó un área específica. Se requiere mayor información.")

def get_marco_legal(area: str) -> str:
    marcos = {
        "laboral": "• Código del Trabajo\n• Ley 20.940\n• Ley 16.744",
        "civil": "• Código Civil\n• Código de Procedimiento Civil",
        "penal": "• Código Penal\n• Código Procesal Penal\n• Ley 20.393",
        "administrativo": "• Ley 19.880\n• Ley 18.575\n• Constitución (Art. 6 y 7)",
        "tributario": "• Código Tributario\n• Ley de IVA\n• Ley sobre Impuesto a la Renta",
        "comercial": "• Código de Comercio\n• Ley 18.046\n• Ley 19.496",
    }
    return marcos.get(area, "• Constitución Política\n• Código Civil (norma general)")
