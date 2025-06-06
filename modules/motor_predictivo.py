def clasificar_consulta(consulta: str) -> str:
    if not consulta:
        return "No clasificada"
    if "civil" in consulta.lower():
        return "Derecho Civil"
    elif "penal" in consulta.lower():
        return "Derecho Penal"
    return "General"
