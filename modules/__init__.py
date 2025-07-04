"""
Módulos del sistema Forensic Legal Cognition 4.1
"""

__version__ = "4.1.0"
__author__ = "Forensic Legal Cognition Team"

# Importaciones principales
from .predict import router as predict_router

# Módulos disponibles
AVAILABLE_MODULES = [
    "predict",
    "root", 
    "reflexion",
    "vision_forense",
    "legislacion_bcn",
    "corpus_legal",
    "prediccion_bayesiana",
    "status",
    "interprete"
]

# Configuración de módulos
MODULE_CONFIG = {
    "predict": {"active": True, "priority": 1},
    "root": {"active": True, "priority": 2},
    "reflexion": {"active": True, "priority": 3},
    "vision_forense": {"active": True, "priority": 4},
    "legislacion_bcn": {"active": True, "priority": 5},
    "corpus_legal": {"active": True, "priority": 6},
    "prediccion_bayesiana": {"active": True, "priority": 7},
    "status": {"active": True, "priority": 8},
    "interprete": {"active": True, "priority": 9}
}

def get_module_info():
    """Retorna información de los módulos disponibles"""
    return {
        "version": __version__,
        "modules": AVAILABLE_MODULES,
        "config": MODULE_CONFIG
    }