from fastapi import APIRouter
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Crear el router universal
router_universal = APIRouter()

# Función para importar router con manejo de errores
def importar_router_seguro(module_path: str, router_name: str, description: str):
    """
    Importa un router de forma segura con manejo de errores
    """
    try:
        module = __import__(module_path, fromlist=[router_name])
        router = getattr(module, router_name)
        router_universal.include_router(router)
        logger.info(f"✔ {description} cargado correctamente")
        return True
    except ImportError as e:
        logger.warning(f"⚠️ {description} no encontrado: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error cargando {description}: {e}")
        return False

# Lista de routers a importar
routers_config = [
    ("modules.root", "router", "Router Root"),
    ("modules.predict", "router", "Router Predict"),
    ("modules.reflexion", "router", "Router Reflexión"),
    ("modules.vision_forense", "router", "Router Visión Forense"),
    ("modules.legislacion_bcn", "router", "Router Legislación BCN"),
    ("modules.corpus_legal", "router", "Router Corpus Legal"),
    ("modules.prediccion_bayesiana", "router", "Router Predicción Bayesiana"),
    ("modules.status", "router", "Router Status"),
    ("modules.interprete", "router", "Router Intérprete"),
]

# Importar routers disponibles
routers_cargados = 0
for module_path, router_name, description in routers_config:
    if importar_router_seguro(module_path, router_name, description):
        routers_cargados += 1

# Agregar endpoints básicos si no hay routers cargados
if routers_cargados == 0:
    logger.warning("⚠️ No se pudieron cargar routers específicos, agregando endpoints básicos")
    
    @router_universal.get("/status")
    async def status_basico():
        """Endpoint básico de status"""
        return {
            "status": "active",
            "message": "Router universal funcionando con endpoints básicos",
            "routers_cargados": routers_cargados
        }
    
    @router_universal.get("/info")
    async def info_basica():
        """Información básica del sistema"""
        return {
            "sistema": "Forensic Legal Cognition 4.1",
            "estado": "operativo",
            "routers_disponibles": routers_cargados,
            "modo": "básico"
        }

# Agregar endpoint de diagnóstico del router universal
@router_universal.get("/router-diagnostico")
async def diagnostico_router():
    """Diagnóstico del router universal"""
    return {
        "router_universal": "activo",
        "routers_cargados": routers_cargados,
        "routers_intentados": len(routers_config),
        "estado": "operativo" if routers_cargados > 0 else "modo_basico",
        "endpoints_registrados": len(router_universal.routes)
    }

logger.info(f"✔ Router universal inicializado con {routers_cargados}/{len(routers_config)} routers")
