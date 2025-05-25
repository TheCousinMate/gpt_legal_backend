import re
from typing import Dict, List, Tuple

def analizar_input_legal(texto: str) -> str:
    """
    Motor de análisis legal mejorado con patrones específicos del derecho chileno
    """
    if not texto or len(texto.strip()) == 0:
        return "Texto vacío. Por favor, provea contenido jurídico para análisis."
    
    texto_lower = texto.lower()
    
    # Patrones de riesgo legal específicos
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
    
    # Análisis por área legal
    areas_legales = {
        "laboral": r"trabajador|empleador|sueldo|contrato\s+de\s+trabajo|despido|finiquito|indemnización",
        "civil": r"contrato|responsabilidad\s+civil|daños|perjuicios|incumplimiento|nulidad",
        "penal": r"delito|dolo|culpa|responsabilidad\s+penal|querella|denuncia",
        "administrativo": r"procedimiento\s+administrativo|autoridad|competencia|recurso\s+de\s+protección",
        "tributario": r"impuesto|tributo|sii|evasión\s+tributaria|facturación",
        "comercial": r"empresa|sociedad|comercio|marca|patente|competencia\s+desleal"
    }
    
    # Detectar área legal
    area_detectada = "general"
    for area, patron in areas_legales.items():
        if re.search(patron, texto_lower):
            area_detectada = area
            break
    
    # Detectar nivel de riesgo
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
    
    # Generar recomendaciones específicas
    recomendaciones = generar_recomendaciones(area_detectada, nivel_riesgo, texto_lower)
    
    # Construir respuesta final
    respuesta = f"""
📊 ANÁLISIS LEGAL AUTOMATIZADO

🎯 Área detectada: {area_detectada.upper()}
⚠️ Nivel de riesgo: {nivel_riesgo.upper()}

📋 Evaluación:
{explicacion_riesgo}

🔍 Análisis específico del área {area_detectada}:
{get_analisis_area(area_detectada, texto_lower)}

💡 Recomendaciones:
{recomendaciones}

⚖️ Marco legal aplicable:
{get_marco_legal(area_detectada)}
"""
    
    return respuesta.strip()

def generar_recomendaciones(area: str, riesgo: str, texto: str) -> str:
    """Genera recomendaciones específicas según área y riesgo"""
    
    recomendaciones_base = {
        "laboral": {
            "alto": "• Consulta urgente con abogado laboralista\n• Documentar todas las comunicaciones\n• Revisar contrato de trabajo y reglamento interno",
            "moderado": "• Formalizar relación laboral por escrito\n• Verificar cumplimiento de obligaciones previsionales\n• Establecer procedimientos claros",
            "bajo": "• Mantener documentación al día\n• Capacitación en normativa laboral\n• Revisión periódica de contratos"
        },
        "civil": {
            "alto": "• Asesoría legal inmediata\n• Preservar evidencia documental\n• Evaluar medidas cautelares",
            "moderado": "• Revisión detallada de obligaciones contractuales\n• Negociación extrajudicial\n• Análisis de garantías",
            "bajo": "• Revisión preventiva de contratos\n• Clarificación de términos ambiguos\n• Documentación adecuada"
        },
        "penal": {
            "alto": "• Consulta inmediata con abogado penalista\n• No realizar declaraciones sin asesoría\n• Preservar evidencia",
            "moderado": "• Asesoría preventiva especializada\n• Revisión de protocolos internos\n• Capacitación en compliance penal",
            "bajo": "• Implementar programas de compliance\n• Capacitación preventiva\n• Auditorías internas"
        }
    }
    
    return recomendaciones_base.get(area, {}).get(riesgo, "• Consulta con abogado especializado\n• Revisión detallada del caso\n• Análisis de alternativas legales")

def get_analisis_area(area: str, texto: str) -> str:
    """Análisis específico por área legal"""
    
    analisis = {
        "laboral": "Se detectan elementos relacionados con derecho del trabajo. Es fundamental verificar el cumplimiento del Código del Trabajo, especialmente en materias de formalización contractual, jornada laboral, y derechos fundamentales del trabajador.",
        
        "civil": "Se identifican aspectos de derecho civil patrimonial. Revisar principios de autonomía de la voluntad, buena fe contractual, y teoría del riesgo según el Código Civil chileno.",
        
        "penal": "Se observan elementos que podrían configurar responsabilidad penal. Analizar tipo penal, elementos objetivos y subjetivos, y posibles eximentes de responsabilidad según el Código Penal.",
        
        "administrativo": "Se detectan aspectos de derecho público. Verificar competencia del órgano, procedimiento administrativo conforme a Ley 19.880, y principios de juridicidad.",
        
        "tributario": "Se identifican aspectos tributarios. Revisar obligaciones ante el SII, principios de legalidad tributaria, y posibles infracciones al Código Tributario.",
        
        "comercial": "Se observan elementos de derecho comercial. Analizar normativa de sociedades, competencia leal, y protección al consumidor según Ley 19.496."
    }
    
    return analisis.get(area, "Análisis general del caso requiere mayor especificación del área legal involucrada.")

def get_marco_legal(area: str) -> str:
    """Marco legal aplicable por área"""
    
    marcos = {
        "laboral": "• Código del Trabajo\n• Ley 16.744 (Accidentes del Trabajo)\n• Ley 20.940 (Reforma Laboral)\n• D.L. 3.500 (Sistema de Pensiones)",
        
        "civil": "• Código Civil\n• Código de Procedimiento Civil\n• Ley 19.947 (Matrimonio Civil)\n• Ley 19.537 (Copropiedad Inmobiliaria)",
        
        "penal": "• Código Penal\n• Código Procesal Penal\n• Ley 20.393 (Responsabilidad Penal de Personas Jurídicas)\n• Ley 19.913 (Lavado de Dinero)",
        
        "administrativo": "• Ley 19.880 (Procedimiento Administrativo)\n• Ley 18.575 (Bases de la Administración del Estado)\n• Ley 20.285 (Transparencia)\n• Constitución Política (arts. 6° y 7°)",
        
        "tributario": "• Código Tributario\n• Ley de Impuesto a la Renta\n• Ley de IVA\n• D.L. 824 (Impuesto a la Renta)",
        
        "comercial": "• Código de Comercio\n• Ley 18.046 (Sociedades Anónimas)\n• Ley 3.918 (Sociedades de Responsabilidad Limitada)\n• Ley 19.496 (Protección del Consumidor)"
    }
    
    return marcos.get(area, "• Código Civil (normas supletorias)\n• Constitución Política\n• Tratados Internacionales ratificados")