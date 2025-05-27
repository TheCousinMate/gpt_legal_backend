from fastapi import HTTPException
import json

def interpretar_input(mensaje: str):
    mensaje_lower = mensaje.lower().strip()

    # Ejemplo simple de interpretación
    if "despido" in mensaje_lower or "fraude" in mensaje_lower:
        return {
            "endpoint": "/api/prediccion/",
            "input_json": {
                "contexto": mensaje
            },
            "interpretacion": "Se detectó intención de análisis de riesgo jurídico-laboral. Redirigido a endpoint de predicción avanzada."
        }

    elif "constitucionalidad" in mensaje_lower or "normativa" in mensaje_lower:
        return {
            "endpoint": "/reflexion/",
            "input_json": {
                "documento_analizado": "Documento detectado automáticamente",
                "criterios": ["constitucionalidad", "contradicción normativa"]
            },
            "interpretacion": "Evaluación doctrinal solicitada. Se aplican criterios constitucionales y de coherencia normativa."
        }

    elif "imagen" in mensaje_lower or "visual" in mensaje_lower:
        return {
            "endpoint": "/vision/",
            "input_json": {
                "image_id": "imagen_generica"
            },
            "interpretacion": "Solicitud de análisis visual legal detectada. Redirigido a motor visual forense."
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="No se pudo interpretar el mensaje. Use términos jurídicos o más contexto."
        )
