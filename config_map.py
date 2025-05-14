CONFIG_MAP = {
    "modules/bcn_parser.py": {
        "model": "none",
        "keywords": ["ley", "norma", "bcn", "boletín"]
    },
    "modules/legislacion_bcn.py": {
        "model": "none",
        "keywords": ["consulta", "legislación", "palabra clave", "búsqueda"]
    },
    "modules/bcn_text_search_parser.py": {
        "model": "none",
        "keywords": ["buscador", "html", "resultados", "búsqueda textual"]
    },
    "modules/reflexion.py": {
        "model": "gpt-4o",
        "temperature": 0.4,
        "top_p": 0.85,
        "max_tokens": 1500,
        "keywords": ["reflexiona", "estructura", "argumento", "coherencia"]
    },
    "modules/vision_forense.py": {
        "model": "gpt-4o",
        "temperature": 0.3,
        "top_p": 0.85,
        "max_tokens": 1000,
        "keywords": ["imagen", "visual", "simbología", "documento"]
    },
    "modules/prediccion_bayesiana.py": {
        "model": "gpt-4o",
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 2048,
        "keywords": ["predecir", "probabilidad", "riesgo", "modelo bayesiano"]
    },
    "modules/forensics_proxy.py": {
        "model": "none",
        "keywords": ["gafi", "beneficiario", "transparencia", "forensics"]
    }
}