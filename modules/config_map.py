CONFIG_MAP = {
    "modules/legislacion_bcn.py": {
        "model": "none",
        "keywords": ["ley", "norma", "bcn", "constitución"]
    },
    "modules/prediccion_bayesiana.py": {
        "model": "gpt-4o",
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 2048,
        "keywords": ["predecir", "probabilidad", "riesgo"]
    },
    "modules/reflexion.py": {
        "model": "gpt-4o",
        "temperature": 0.4,
        "top_p": 0.85,
        "max_tokens": 1500,
        "keywords": ["reflexiona", "estructura", "argumento"]
    },
    "modules/vision_forense.py": {
        "model": "gpt-4o",
        "temperature": 0.3,
        "top_p": 0.85,
        "max_tokens": 1000,
        "keywords": ["imagen", "visual", "simbología"]
    }
}
