
# motor_predictivo.py

def analizar_input_legal(texto: str) -> str:
    texto = texto.lower()

    if "trabajador" in texto and "contrato" in texto and "informal" in texto:
        return (
            "Existe un riesgo legal elevado. Según el Código del Trabajo chileno, toda relación laboral "
            "requiere contrato por escrito. La falta de formalización puede acarrear multas, pérdida de defensas "
            "legales del empleador, y reconocimiento forzoso de vínculo laboral por parte de la Inspección del Trabajo."
        )
    elif "pago" in texto and "sin contrato" in texto:
        return (
            "Existe riesgo probatorio y fiscal. Aunque haya pago regular, la ausencia de contrato escrito "
            "impide acreditar condiciones pactadas, y expone a la empresa a sanciones por evasión previsional o tributaria."
        )
    elif "riesgo legal" in texto:
        return (
            "Cualquier relación contractual no formalizada correctamente representa riesgo legal. "
            "Es fundamental contar con respaldo documental válido para evitar conflictos o sanciones."
        )
    else:
        return "No se detectó riesgo legal específico, pero se recomienda revisión con asesoría jurídica especializada."
